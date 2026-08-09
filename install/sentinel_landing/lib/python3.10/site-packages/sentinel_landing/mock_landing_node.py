#!/usr/bin/env python3
"""
mock_landing_node.py – Stub node for the Landing package.

Subscribes to drone_state. When the state becomes "landing", it simulates
a landing sequence: after a short delay it publishes `end = True`
continuously until drone_state becomes "standby".

Intended for testing the Mission package's landing → standby transition.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String


class MockLandingNode(Node):
    def __init__(self):
        super().__init__("mock_landing_node")

        self.declare_parameter("landing_duration", 5.0)    # seconds to simulate landing
        self.declare_parameter("publish_rate", 2.0)         # Hz

        landing_duration = self.get_parameter("landing_duration").value
        pub_rate = self.get_parameter("publish_rate").value

        self._end_pub = self.create_publisher(Bool, "/drone_node/end", 10)
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)

        self.drone_state = "standby"
        self._landing_complete = False

        pub_period = 1.0 / pub_rate
        self._pub_timer = self.create_timer(pub_period, self._republish_end)
        self._pub_timer.cancel()

        self.get_logger().info(
            f"Mock landing node ready – simulates {landing_duration}s landing"
        )

    def _state_cb(self, msg: String):
        prev = self.drone_state
        self.drone_state = msg.data

        if prev != "landing" and self.drone_state == "landing":
            duration = self.get_parameter("landing_duration").value
            self.get_logger().info(f"Landing state detected — will send 'end' in {duration}s")
            self._oneshot = self.create_timer(duration, self._finish_landing)

        if self.drone_state == "standby" and self._landing_complete:
            self._pub_timer.cancel()
            self._landing_complete = False
            self.get_logger().info("Standby reached — stopping end trigger")

    def _finish_landing(self):
        if self._landing_complete:
            return
        self._landing_complete = True
        self._pub_timer.reset()
        self.get_logger().info("MOCK LANDING COMPLETE — publishing 'end'")

    def _republish_end(self):
        if not self._landing_complete:
            self._pub_timer.cancel()
            return
        msg = Bool()
        msg.data = True
        self._end_pub.publish(msg)


def main():
    rclpy.init()
    node = MockLandingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
