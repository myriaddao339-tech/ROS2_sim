#!/usr/bin/env python3
"""
Execute a hardcoded mission step by step:
  1. Verify FCU connection
  2. Arm
  3. Switch to GUIDED, takeoff to 10 m (using COMMAND_LONG takeoffcur)
  4. Switch to AUTO and let the mission run
  5. Detect mission completion (last waypoint reached)
  6. Switch to RTL and exit

No external file required – the mission is defined directly in the script.
Altitude detection uses /mavros/local_position/pose (z field).
"""

import os
import sys
import json
import rclpy
from rclpy.node import Node
from rclpy.utilities import remove_ros_args
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from rclpy.qos import qos_profile_sensor_data

from mavros_msgs.msg import CommandCode, Waypoint, State, WaypointReached
from mavros_msgs.srv import WaypointPush, CommandBool, SetMode, CommandLong, CommandTOL


def _f(value, default=0.0):
    """QGC's JSON often has `null` for unused params - coerce to a float."""
    return float(value) if value is not None else default


def load_qgc_plan(path):
    """Parse a QGroundControl .plan (JSON) file into Waypoint messages."""
    with open(path, "r") as f:
        data = json.load(f)
 
    mission = data["mission"]
    home_lat, home_lon, home_alt = mission["plannedHomePosition"]
 
    # QGC stores home separately in the JSON, but ArduPilot expects it
    # as seq 0 of the pushed mission - the same slot the older .waypoints
    # format bakes directly into the file.
    waypoints = [
        Waypoint(
            frame=Waypoint.FRAME_GLOBAL,
            command=CommandCode.NAV_WAYPOINT,
            is_current=True,
            autocontinue=True,
            param1=0.0, param2=0.0, param3=0.0, param4=0.0,
            x_lat=_f(home_lat), y_long=_f(home_lon), z_alt=_f(home_alt),
        )
    ]
 
    for item in mission["items"]:
        if item.get("type") != "SimpleItem":
            raise ValueError(
                f"item type {item.get('type')!r} not handled here - this "
                "covers plain waypoints, not surveys/complex patterns"
            )
        p1, p2, p3, p4, lat, lon, alt = item["params"]
        waypoints.append(Waypoint(
            frame=item["frame"],
            command=item["command"],
            is_current=False,
            autocontinue=item["autoContinue"],
            param1=_f(p1), param2=_f(p2), param3=_f(p3), param4=_f(p4),
            x_lat=_f(lat), y_long=_f(lon), z_alt=_f(alt),
        ))
 
    return waypoints


def generate_waypoints():
    args = remove_ros_args(sys.argv)  # drops --ros-args and everything after it

    if len(args) == 2:
        plan_file = args[1]
    elif len(args) == 1:
        plan_file = "mission1.plan"
    else:
        print("Usage: ros2 run <pkg> <exe> [mission_file]")
        sys.exit(1)

    mission_path = os.path.join(get_package_share_directory("navigation_pkg"), "missions", plan_file)

    if not os.path.isfile(mission_path):
        print(f"Mission file not found: '{mission_path}'")
        sys.exit(1)

    return load_qgc_plan(mission_path)


class SquareNode(Node):
    def __init__(self, waypoints):
        super().__init__("square_mission_node")
        self.waypoints = waypoints
        self.last_wp = len(waypoints) - 1   # last waypoint sequence number

        # --- Subscriptions ---
        self.state = State()
        self.create_subscription(State, "/mavros/state", self._state_cb, 10)

        self.reached_seq = None
        self.create_subscription(
            WaypointReached, "/mavros/mission/reached", self._reached_cb, 10
        )

        # Replaced altitude topic with local position (always available)
        self.local_pose = PoseStamped()
        self.create_subscription(PoseStamped,"/mavros/local_position/pose",self._local_pose_cb,qos_profile_sensor_data)

        # --- Service clients ---
        self._mission_push_cli = self.create_client(
            WaypointPush, "/mavros/mission/push"
        )
        self._arm_cli = self.create_client(CommandBool, "/mavros/cmd/arming")
        self._mode_cli = self.create_client(SetMode, "/mavros/set_mode")
        # Use the generic COMMAND_LONG service for takeoff (takeoffcur)
        self._cmd_long_cli = self.create_client(CommandTOL, "/mavros/cmd/takeoff")

    # ---- Callbacks ----
    def _state_cb(self, msg):
        self.state = msg

    def _reached_cb(self, msg):
        self.reached_seq = msg.wp_seq
        self.get_logger().info(f"Waypoint {msg.wp_seq} reached")

    def _local_pose_cb(self, msg):
        self.local_pose = msg

    # ---- Utility: wait for a condition while spinning ----
    def _wait_for(self, condition, timeout_sec, description="condition"):
        start = self.get_clock().now()
        while (self.get_clock().now() - start).nanoseconds / 1e9 < timeout_sec:
            rclpy.spin_once(self, timeout_sec=0.1)
            if condition():
                return True
        self.get_logger().error(f"Timeout waiting for: {description}")
        return False

    # ---- Execution steps ----
    def execute_mission_sequence(self):
        # 1. Wait for FCU connection
        self.get_logger().info("Waiting for FCU connection...")
        if not self._wait_for(
            lambda: self.state.connected, 20.0, "FCU connection"
        ):
            return False

        # 2. Push mission to FCU
        self.get_logger().info("Pushing mission...")
        if not self._mission_push_cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("Mission push service unavailable")
            return False

        req = WaypointPush.Request()
        req.start_index = 0
        req.waypoints = self.waypoints
        future = self._mission_push_cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)
        res = future.result()
        if res is None or not res.success:
            self.get_logger().error("Mission push failed")
            return False
        self.get_logger().info(f"Mission pushed: {res.wp_transfered}/{len(self.waypoints)} waypoints")

        # 3. Arm if not already armed
        if not self.state.armed:
            self.get_logger().info("Arming...")
            if not self._arm_cli.wait_for_service(timeout_sec=5.0):
                self.get_logger().error("Arming service unavailable")
                return False
            arm_req = CommandBool.Request()
            arm_req.value = True
            future = self._arm_cli.call_async(arm_req)
            rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
            res = future.result()
            if res is None or not res.success:
                self.get_logger().error("Arming command failed")
                return False
            # Wait until armed flag is set
            if not self._wait_for(lambda: self.state.armed, 10.0, "arming confirmation"):
                return False
        else:
            self.get_logger().info("Already armed")

        # 4. Switch to GUIDED mode
        self.get_logger().info("Switching to GUIDED mode...")
        if not self._mode_cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("SetMode service unavailable")
            return False
        mode_req = SetMode.Request()
        mode_req.base_mode = 0
        mode_req.custom_mode = "GUIDED"
        future = self._mode_cli.call_async(mode_req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.result().mode_sent:
            self.get_logger().error("Failed to send GUIDED mode command")
            return False
        if not self._wait_for(lambda: self.state.mode == "GUIDED", 10.0, "GUIDED mode"):
            return False

        # 5. Takeoff to 10 m using COMMAND_LONG (MAV_CMD_NAV_TAKEOFF)
        self.get_logger().info("Taking off to 10 m (takeoffcur)...")
        if not self._cmd_long_cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("CommandLong service unavailable")
            return False

        # CommandTOL request
        takeoff_req = CommandTOL.Request()
        takeoff_req.min_pitch = 0.0
        takeoff_req.yaw = 0.0
        takeoff_req.latitude = 0.0   # 0 = current position
        takeoff_req.longitude = 0.0
        takeoff_req.altitude = 15.0

        future = self._cmd_long_cli.call_async(takeoff_req)

        # takeoff_cmd = CommandLong.Request()
        # takeoff_cmd.command = 22  # MAV_CMD_NAV_TAKEOFF
        # takeoff_cmd.param1 = 0.0  # pitch (ignored)
        # takeoff_cmd.param2 = 0.0  # empty
        # takeoff_cmd.param3 = 0.0  # empty
        # takeoff_cmd.param4 = 0.0  # yaw (ignored)
        # takeoff_cmd.param5 = 0.0  # latitude (0 = current location)
        # takeoff_cmd.param6 = 0.0  # longitude (0 = current location)
        # takeoff_cmd.param7 = 10.0 # altitude (m)
        # takeoff_cmd.confirmation = 0

        # future = self._cmd_long_cli.call_async(takeoff_cmd)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        res = future.result()
        if res is None or not res.success:
            self.get_logger().error("Takeoff command failed")
            return False

        # Wait until altitude >= 9.5 m using local position Z (ENU, up positive)
        self.get_logger().info("Waiting for target altitude...")
        if not self._wait_for(
            lambda: self.local_pose.pose.position.z >= 9.5,
            30.0,
            "takeoff altitude"
        ):
            print("Current altitude:", self.local_pose.pose.position.z)
            return False
        self.get_logger().info("Target altitude reached")

        # 6. Switch to AUTO to start the mission
        self.get_logger().info("Switching to AUTO mode...")
        mode_req.custom_mode = "AUTO"
        future = self._mode_cli.call_async(mode_req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.result().mode_sent:
            self.get_logger().error("Failed to send AUTO mode command")
            return False
        if not self._wait_for(lambda: self.state.mode == "AUTO", 10.0, "AUTO mode"):
            return False
        self.get_logger().info("Mission started in AUTO mode")

        # 7. Wait for the last waypoint to be reached
        self.get_logger().info(f"Waiting for last waypoint (seq {self.last_wp})...")
        if not self._wait_for(
            lambda: self.reached_seq is not None and self.reached_seq >= self.last_wp,
            300.0,  # 5 minutes timeout – adjust as needed
            f"waypoint {self.last_wp}"
        ):
            return False
        self.get_logger().info("Mission complete – all waypoints visited")

        # 8. Switch to RTL
        self.get_logger().info("Switching to RTL mode...")
        mode_req.custom_mode = "RTL"
        future = self._mode_cli.call_async(mode_req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=5.0)
        if not future.result().mode_sent:
            self.get_logger().error("Failed to send RTL mode command")
            return False
        if not self._wait_for(lambda: self.state.mode == "RTL", 10.0, "RTL mode"):
            return False
        self.get_logger().info("RTL mode engaged – drone returning home")

        return True


def main():
    rclpy.init()

    waypoints = generate_waypoints()
    node = SquareNode(waypoints)

    # Run the sequence
    success = node.execute_mission_sequence()

    node.destroy_node()
    rclpy.shutdown()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()