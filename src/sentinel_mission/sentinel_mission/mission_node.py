#!/usr/bin/env python3
"""
mission_node.py – Waypoint file parser & mission progress tracker.

Responsibilities:
  1. Parse a QGC .plan file at startup.
  2. Serve the waypoint list via the ~/get_mission service.
  3. Subscribe to /mavros/mission/reached and publish waypoint_reached
     (once per waypoint) or mission_finished (continuous at 2 Hz until
     drone_state becomes "landing").
  4. Subscribe to drone_state to know when to stop publishing triggers.
"""

import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int32, String
from mavros_msgs.msg import WaypointReached
from sentinel_mission_msgs.srv import GetMission

from sentinel_mission.mission_loader import load_qgc_plan


class MissionNode(Node):
    def __init__(self):
        super().__init__("mission_node")

        # --- Parameters ---
        self.declare_parameter("mission_file_path", "")
        mission_file = self.get_parameter("mission_file_path").get_parameter_value().string_value

        # --- Parse the mission file ---
        self.mission_waypoints = []
        self.total_waypoints = 0
        self._load_mission(mission_file)

        # --- Service: serve the waypoint list ---
        self._mission_srv = self.create_service(
            GetMission, "~/get_mission", self._handle_get_mission
        )

        # --- Subscribe to FCU waypoint feedback ---
        self.create_subscription(
            WaypointReached, "/mavros/mission/reached", self._wp_reached_cb, 10
        )

        # --- Subscribe to drone_state (to stop republishing) ---
        self.drone_state = "standby"
        self.create_subscription(String, "/drone_node/drone_state", self._drone_state_cb, 10)

        # --- Publishers ---
        self._wp_reached_pub = self.create_publisher(Int32, "~/waypoint_reached", 10)
        self._mission_finished_pub = self.create_publisher(Bool, "~/mission_finished", 10)

        # --- Internal state ---
        self.last_reached_index = -1
        self._publishing_mission_finished = False

        # Timer to republish mission_finished at 2 Hz while active
        self._mission_finished_timer = self.create_timer(0.5, self._republish_mission_finished)
        self._mission_finished_timer.cancel()  # start disabled

        self.get_logger().info(
            f"Mission node ready – {self.total_waypoints} waypoints loaded"
        )

    # ---- Helpers ----
    def _load_mission(self, mission_file: str):
        """Load waypoints from the configured .plan file."""
        if not mission_file:
            # Fall back to default mission in the package share directory
            from ament_index_python.packages import get_package_share_directory
            mission_file = os.path.join(
                get_package_share_directory("sentinel_mission"),
                "missions", "mission1.plan",
            )

        if not os.path.isfile(mission_file):
            self.get_logger().warn(
                f"Mission file not found: '{mission_file}' — "
                "waypoint list will be empty."
            )
            return

        try:
            self.mission_waypoints = load_qgc_plan(mission_file)
            self.total_waypoints = len(self.mission_waypoints)
            self.get_logger().info(f"Loaded {self.total_waypoints} waypoints from '{mission_file}'")
        except Exception as e:
            self.get_logger().error(f"Failed to parse mission file: {e}")

    # ---- Service callback ----
    def _handle_get_mission(self, request, response):
        """Return the parsed waypoint list to the caller."""
        # If the client provides a specific file path, reload from it.
        if request.mission_file:
            try:
                waypoints = load_qgc_plan(request.mission_file)
                response.success = True
                response.message = f"Loaded {len(waypoints)} waypoints"
                response.waypoints = waypoints
            except Exception as e:
                response.success = False
                response.message = str(e)
                response.waypoints = []
        else:
            response.success = len(self.mission_waypoints) > 0
            response.message = (
                f"Served {self.total_waypoints} waypoints from default mission"
            )
            response.waypoints = self.mission_waypoints

        self.get_logger().info(f"GetMission: {response.message}")
        return response

    # ---- FCU waypoint feedback ----
    def _wp_reached_cb(self, msg: WaypointReached):
        wp_seq = msg.wp_seq
        self.get_logger().info(f"FCU reports waypoint {wp_seq} reached")

        if wp_seq == self.last_reached_index:
            return  # duplicate
        self.last_reached_index = wp_seq

        if wp_seq >= self.total_waypoints - 1:
            # Last waypoint → publish mission_finished continuously
            self.get_logger().info("Last waypoint reached — publishing mission_finished")
            self._publishing_mission_finished = True
            self._mission_finished_timer.reset()
        else:
            # Intermediate waypoint → publish waypoint_reached once
            msg_out = Int32()
            msg_out.data = wp_seq
            self._wp_reached_pub.publish(msg_out)
            self.get_logger().info(f"Published waypoint_reached: {wp_seq}")

    def _republish_mission_finished(self):
        """Timer callback – continuously republishes mission_finished."""
        if not self._publishing_mission_finished:
            self._mission_finished_timer.cancel()
            return

        msg = Bool()
        msg.data = True
        self._mission_finished_pub.publish(msg)

        # Stop when drone enters landing state
        if self.drone_state == "landing":
            self._publishing_mission_finished = False
            self._mission_finished_timer.cancel()
            self.get_logger().info("Drone state is 'landing' — stopped publishing mission_finished")

    def _drone_state_cb(self, msg: String):
        self.drone_state = msg.data


def main():
    rclpy.init()
    node = MissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
