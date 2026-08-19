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

import math
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Int32, String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import WaypointReached
from sentinel_mission_msgs.srv import GetMission

from sentinel_mission.mission_loader import load_qgc_plan


class MissionNode(Node):
    def __init__(self):
        super().__init__("mission_node")

        # --- Parameters ---
        self.declare_parameter("mission_file_path", "")
        self.declare_parameter("ekf_origin_lat", 0.0)   # deg, defaults to the plan home
        self.declare_parameter("ekf_origin_lon", 0.0)   # deg, defaults to the plan home
        self.declare_parameter("ekf_origin_alt", 0.0)   # m AMSL, defaults to the plan home
        mission_file = self.get_parameter("mission_file_path").get_parameter_value().string_value

        # --- Parse the mission file ---
        self.mission_waypoints = []
        self.total_waypoints = 0
        self._load_mission(mission_file)

        # --- EKF origin for local-NED conversion ---
        self._origin = self._resolve_origin()

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

        # --- Subscribe to waypoint_skip from Inner Map ---
        self._skip_prev = False
        self.create_subscription(Bool, "/inner_map/waypoint_skip", self._waypoint_skip_cb, 10)

        # --- Publishers ---
        self._wp_reached_pub = self.create_publisher(Int32, "~/waypoint_reached", 10)
        self._mission_finished_pub = self.create_publisher(Bool, "~/mission_finished", 10)
        self._target_wp_pub = self.create_publisher(PoseStamped, "~/target_waypoint", 10)

        # --- Internal state ---
        self.last_reached_index = -1
        self.target_index = 1        # first real waypoint (index 0 = home)
        self._publishing_mission_finished = False

        # Timer to republish mission_finished at 2 Hz while active
        self._mission_finished_timer = self.create_timer(0.5, self._republish_mission_finished)
        self._mission_finished_timer.cancel()  # start disabled

        self.get_logger().info(
            f"Mission node ready – {self.total_waypoints} waypoints loaded"
        )

        # Let Inner Map know the first real waypoint right away.
        self._publish_target_waypoint()

    # ---- Helpers ----
    def _resolve_origin(self):
        """EKF origin (lat, lon, alt) for the local-NED conversion.

        Defaults to the mission's planned home position (loaded as
        waypoint 0); explicit ekf_origin_* parameters override it when
        lat or lon is non-zero.
        """
        lat = float(self.get_parameter("ekf_origin_lat").value)
        lon = float(self.get_parameter("ekf_origin_lon").value)
        alt = float(self.get_parameter("ekf_origin_alt").value)
        if lat != 0.0 or lon != 0.0:
            return lat, lon, alt
        if self.mission_waypoints:
            home = self.mission_waypoints[0]
            return float(home.x_lat), float(home.y_long), float(home.z_alt)
        return 0.0, 0.0, 0.0

    def _wp_to_local_ned(self, wp):
        """Convert one waypoint to local NED metres (x=N, y=E, z=D).

        Flat-earth approximation around the EKF origin (accurate for the
        ~400 m grid this project flies in).
        """
        lat0, lon0, alt0 = self._origin
        d_north = (float(wp.x_lat) - lat0) * 111320.0
        d_east = (
            (float(wp.y_long) - lon0) * 111320.0 * math.cos(math.radians(lat0))
        )
        alt = float(wp.z_alt)
        if wp.frame == wp.FRAME_GLOBAL:
            z = -(alt - alt0)          # AMSL -> NED relative to home
        else:
            z = -alt                   # relative-altitude frames (AGL)
        return d_north, d_east, z

    def _publish_target_waypoint(self):
        """Publish the current target waypoint to Inner Map (local NED)."""
        if not self.mission_waypoints or self.target_index >= self.total_waypoints:
            return
        wp = self.mission_waypoints[self.target_index]
        x, y, z = self._wp_to_local_ned(wp)
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        self._target_wp_pub.publish(msg)
        self.get_logger().info(
            f"Published target_waypoint {self.target_index}: "
            f"NED ({x:.1f}, {y:.1f}, {z:.1f})"
        )

    def _waypoint_skip_cb(self, msg: Bool):
        """Inner Map asks to skip the current target (one skip per edge)."""
        rising = bool(msg.data) and not self._skip_prev
        self._skip_prev = bool(msg.data)
        if not rising:
            return

        self.get_logger().warn("Inner Map requested a waypoint skip")
        self.target_index += 1
        if self.target_index >= self.total_waypoints:
            self.get_logger().info(
                "Skipped past the last waypoint – publishing mission_finished"
            )
            self._publishing_mission_finished = True
            self._mission_finished_timer.reset()
            return
        self._publish_target_waypoint()

    def _load_mission(self, mission_file: str):
        """Load waypoints from the configured .plan file."""
        if not mission_file:
            # Fall back to default mission in the package share directory
            from ament_index_python.packages import get_package_share_directory
            mission_file = os.path.join(
                get_package_share_directory("sentinel_mission"),
                "missions", "obstacle_course.plan",
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

            # And let Inner Map know the new target waypoint.
            self.target_index = wp_seq + 1
            self._publish_target_waypoint()

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
        prev = self.drone_state
        self.drone_state = msg.data

        # New flight: point back at the first real waypoint and republish
        # it for Inner Map.  Reset the FCU reached index too so duplicate
        # wp_seq values on a second flight are not dropped as duplicates.
        if prev == "standby" and msg.data == "mission":
            self.last_reached_index = -1
            self.target_index = 1
            self._publish_target_waypoint()


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
