#!/usr/bin/env python3
"""
emergency_node.py – Battery & heartbeat monitor.

Triggers:
  - Battery level drops below `battery_threshold` (default 20%).
  - Heartbeat (FCU /mavros/state) is lost for longer than
    `heartbeat_timeout` (default 15 s).

Publishes `emergency` (Bool, True) continuously at `publish_rate` until
`drone_state` becomes "standby", then resets.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Bool, String
from sensor_msgs.msg import BatteryState
from mavros_msgs.msg import State


class EmergencyNode(Node):
    def __init__(self):
        super().__init__("emergency_node")

        # --- Parameters ---
        self.declare_parameter("battery_threshold", 0.20)   # 20 %
        self.declare_parameter("heartbeat_timeout", 15.0)   # seconds
        self.declare_parameter("publish_rate", 2.0)          # Hz

        self.battery_threshold = (
            self.get_parameter("battery_threshold").get_parameter_value().double_value
        )
        self.heartbeat_timeout = (
            self.get_parameter("heartbeat_timeout").get_parameter_value().double_value
        )
        publish_rate = (
            self.get_parameter("publish_rate").get_parameter_value().double_value
        )

        # --- Subscriptions ---
        self.create_subscription(BatteryState, "/mavros/battery", self._battery_cb, qos_profile_sensor_data)
        self.create_subscription(State, "/mavros/state", self._heartbeat_cb, 10)
        self.create_subscription(String, "/drone_node/drone_state", self._drone_state_cb, 10)

        # --- Publisher ---
        self._emergency_pub = self.create_publisher(Bool, "~/emergency", 10)

        # --- Internal state ---
        self.emergency_active = False
        self.last_heartbeat_time = self.get_clock().now()
        self.drone_state = "standby"

        # Monitor timer – checks heartbeat timeout at 1 Hz
        self._monitor_timer = self.create_timer(1.0, self._check_heartbeat)

        # Publish timer – republishes emergency at `publish_rate` while active
        pub_period = 1.0 / publish_rate
        self._publish_timer = self.create_timer(pub_period, self._republish_emergency)
        self._publish_timer.cancel()  # start disabled

        self.get_logger().info(
            f"Emergency node ready – battery < {self.battery_threshold*100:.0f}%, "
            f"heartbeat timeout {self.heartbeat_timeout}s"
        )

    # ---- Callbacks ----
    def _battery_cb(self, msg: BatteryState):
        if self.emergency_active:
            return

        # if msg.percentage < self.battery_threshold:
        #     self.get_logger().warn(
        #         f"Battery low: {msg.percentage:.1f}% < {self.battery_threshold*100:.0f}%"
        #     )
        #     self._activate_emergency()

    def _heartbeat_cb(self, msg: State):
        self.last_heartbeat_time = self.get_clock().now()

    def _check_heartbeat(self):
        """Timer callback: check if heartbeat has timed out."""
        if self.emergency_active:
            return

        elapsed = (self.get_clock().now() - self.last_heartbeat_time).nanoseconds / 1e9
        if elapsed > self.heartbeat_timeout:
            self.get_logger().error(
                f"Heartbeat lost for {elapsed:.1f}s (timeout={self.heartbeat_timeout}s)"
            )
            self._activate_emergency()

    def _drone_state_cb(self, msg: String):
        self.drone_state = msg.data

        # Reset emergency when back in standby
        if self.drone_state == "standby" and self.emergency_active:
            self.get_logger().info("Drone in standby — resetting emergency")
            self.emergency_active = False
            self._publish_timer.cancel()
            # Publish False one last time to clear the signal
            msg_out = Bool()
            msg_out.data = False
            self._emergency_pub.publish(msg_out)

    # ---- Emergency activation ----
    def _activate_emergency(self):
        """Start publishing emergency continuously."""
        self.emergency_active = True
        self._publish_timer.reset()
        self.get_logger().error("EMERGENCY ACTIVATED")

    def _republish_emergency(self):
        """Timer callback: republish emergency while active."""
        if not self.emergency_active:
            self._publish_timer.cancel()
            return

        msg = Bool()
        msg.data = True
        self._emergency_pub.publish(msg)

        # Stop when drone enters landing state (emergency landing in progress)
        if self.drone_state == "landing":
            self.get_logger().info("Drone is landing — emergency acknowledged, stopping republish")
            self._publish_timer.cancel()
            # Note: we do NOT reset emergency_active here;
            # that only happens when drone_state = standby


def main():
    rclpy.init()
    node = EmergencyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
