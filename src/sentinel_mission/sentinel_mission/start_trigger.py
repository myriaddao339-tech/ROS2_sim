#!/usr/bin/env python3
"""
start_trigger.py – Simple node that publishes the `start` trigger.

Waits for `drone_state` to be "standby", then publishes `start = True`
continuously until `drone_state` becomes "mission".

This simulates a ground-station "Go" command.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String


class StartTrigger(Node):
    def __init__(self):
        super().__init__("start_trigger")

        # --- Parameters ---
        self.declare_parameter("auto_start_delay", 3.0)  # seconds before firing
        self.declare_parameter("publish_rate", 2.0)       # Hz while active

        auto_delay = (
            self.get_parameter("auto_start_delay").get_parameter_value().double_value
        )
        publish_rate = (
            self.get_parameter("publish_rate").get_parameter_value().double_value
        )

        # --- Publisher ---
        self._start_pub = self.create_publisher(Bool, "~/start", 10)

        # --- Subscribe to drone_state ---
        self.drone_state = ""
        self.create_subscription(String, "/drone_node/drone_state", self._drone_state_cb, 10)

        # --- Internal state ---
        self._fired = False
        self._oneshot_pending = False  # guard against creating duplicate oneshot timers

        # Auto-start after a short delay
        pub_period = 1.0 / publish_rate
        self._publish_timer = self.create_timer(pub_period, self._republish_start)
        self._publish_timer.cancel()

        self.get_logger().info(
            f"Start trigger ready – will fire {auto_delay}s after detecting standby state"
        )

    def _drone_state_cb(self, msg: String):
        prev = self.drone_state
        self.drone_state = msg.data

        # Fire when we enter standby for the first time
        if self.drone_state == "standby" and not self._fired and not self._oneshot_pending:
            self.get_logger().info("Drone in standby — starting auto-start timer")
            self._oneshot_pending = True
            self._oneshot = self.create_timer(
                self.get_parameter("auto_start_delay").get_parameter_value().double_value,
                self._fire,
            )

        # Stop publishing once mission has started
        if self.drone_state == "mission" and self._fired:
            self._publish_timer.cancel()
            self.get_logger().info("Drone in mission state — stopping start trigger")
            self._fired = False  # reset to allow re-triggering on next standby

    def _fire(self):
        """Activate the start signal."""
        if self._fired:
            return
        self._fired = True
        self._oneshot_pending = False
        self._oneshot.cancel()
        self._publish_timer.reset()
        self.get_logger().info("START signal activated")

    def _republish_start(self):
        """Timer callback: republish start while active."""
        if not self._fired:
            self._publish_timer.cancel()
            return
        msg = Bool()
        msg.data = True
        self._start_pub.publish(msg)


def main():
    rclpy.init()
    node = StartTrigger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
