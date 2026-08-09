#!/usr/bin/env python3
"""
mock_obstacle_publisher.py – Stub node for the ODA package.

Subscribes to drone_state and, when in "mission" state, simulates an
obstacle detection by publishing `obstacle_detected = True` after a
configurable delay. Continuously republishes until drone_state
becomes "oda".

Intended for testing the Mission package's obstacle → ODA transition.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String


class MockObstaclePublisher(Node):
    def __init__(self):
        super().__init__("mock_obstacle_publisher")

        self.declare_parameter("trigger_delay", 20.0)   # seconds in mission before firing
        self.declare_parameter("publish_rate", 2.0)      # Hz

        trigger_delay = self.get_parameter("trigger_delay").value
        pub_rate = self.get_parameter("publish_rate").value

        self._pub = self.create_publisher(Bool, "/drone_node/obstacle_detected", 10)
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)

        self.drone_state = "standby"
        self._fired = False

        pub_period = 1.0 / pub_rate
        self._pub_timer = self.create_timer(pub_period, self._republish)
        self._pub_timer.cancel()

        self.get_logger().info(
            f"Mock ODA obstacle publisher ready – will fire {trigger_delay}s "
            "after entering mission state"
        )

    def _state_cb(self, msg: String):
        prev = self.drone_state
        self.drone_state = msg.data

        if prev != "mission" and self.drone_state == "mission" and not self._fired:
            delay = self.get_parameter("trigger_delay").value
            self.get_logger().info(f"Mission state detected — obstacle trigger in {delay}s")
            self._oneshot = self.create_timer(delay, self._trigger)

        if self.drone_state == "oda" and self._fired:
            self._pub_timer.cancel()
            self.get_logger().info("ODA state reached — stopping obstacle trigger")

    def _trigger(self):
        if self._fired:
            return
        self._fired = True
        self._pub_timer.reset()
        self.get_logger().warn("MOCK OBSTACLE DETECTED")

    def _republish(self):
        if not self._fired:
            self._pub_timer.cancel()
            return
        msg = Bool()
        msg.data = True
        self._pub.publish(msg)


def main():
    rclpy.init()
    node = MockObstaclePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
