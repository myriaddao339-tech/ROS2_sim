#!/usr/bin/env python3
"""
test_detection_cooldown.py – headless test of the post-sweep trigger cooldown.

Drives DetectionNode with a synthetic metric depth map (a close obstacle
right in front of the camera) and drives the sweeping / state callbacks
directly.  Verifies:
  A) during a sweep the trigger validates normally (harness sanity);
  B) sweep end -> latch cleared and the cooldown armed;
  C) while the cooldown runs the close obstacle CANNOT re-trigger, so
     GUIDED gets its window to fly the path away instead of ODA Maneuvers
     immediately re-arming the sweep;
  D) after the cooldown expires the close obstacle re-triggers;
  E) a state change cancels the cooldown.

plane_filter is disabled and confirm_frames=2 / cooldown=0.5 s are set
directly on the node so the test is fast and needs no MAVROS pose.

Usage: source /opt/ros/humble/setup.bash && source install/setup.bash &&
       python3 test_scripts/test_detection_cooldown.py
"""
import time

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from std_msgs.msg import Bool, String
from sensor_msgs.msg import Image

from sentinel_oda.detection_node import DetectionNode


def make_depth(width=64, height=64, far=20.0, near=2.0, box=12):
    """Synthetic metric depth map: far background with a near block at the
    centre (inside the virtual box)."""
    arr = np.full((height, width), far, dtype=np.float32)
    c = width // 2
    half = box // 2
    arr[c - half:c + half, c - half:c + half] = near
    msg = Image()
    msg.header.frame_id = "depth_camera"
    msg.header.stamp.sec = int(time.time())
    msg.height = height
    msg.width = width
    msg.encoding = "32FC1"
    msg.is_bigendian = 0
    msg.step = width * 4
    msg.data = arr.tobytes()
    return msg


class Harness(Node):
    def __init__(self):
        super().__init__("detection_cooldown_harness")
        self.obstacles = []
        self.create_subscription(
            Bool, "/detection_node/obstacle_detected", self._cb, 10
        )

    def _cb(self, msg):
        self.obstacles.append(msg.data)


def main():
    rclpy.init()
    n = DetectionNode()
    # Test knobs – members set directly (same style as test_guided_node).
    n._plane_filter = False
    n._confirm_n = 2
    n._post_sweep_cooldown = 0.5
    h = Harness()
    ex = SingleThreadedExecutor()
    ex.add_node(n)
    ex.add_node(h)

    results = []

    def expect(cond, label):
        print(f"[{'PASS' if cond else 'FAIL'}] {label}")
        results.append(bool(cond))

    def pump(seconds=0.3):
        end = time.time() + seconds
        while time.time() < end:
            ex.spin_once(timeout_sec=0.05)

    img = make_depth()

    # A) during a sweep the trigger validates normally (sanity check).
    n._state_cb(String(data="oda"))
    n._sweeping_cb(Bool(data=True))
    for _ in range(3):
        n._depth_cb(img)
    pump()
    expect(n._obstacle, "A: close obstacle validates during a sweep")

    # B) sweep end -> latch cleared, cooldown armed.
    n._sweeping_cb(Bool(data=False))
    expect(not n._obstacle, "B1: sweep end clears the latch")
    expect(n._post_sweep_until is not None, "B2: cooldown armed")

    # C) cooldown suppresses the fresh re-trigger.
    for _ in range(6):
        n._depth_cb(img)
    pump()
    expect(not n._obstacle, "C1: no re-trigger during the cooldown")
    expect(h.obstacles and h.obstacles[-1] is False,
           "C2: obstacle_detected stayed False on the topic")

    # D) after the cooldown expires the trigger works again.
    time.sleep(0.7)
    for _ in range(3):
        n._depth_cb(img)
    expect(n._obstacle, "D: close obstacle re-triggers after the cooldown")

    # E) a state change cancels the cooldown.
    n._sweeping_cb(Bool(data=True))
    n._sweeping_cb(Bool(data=False))
    expect(n._post_sweep_until is not None, "E1: cooldown re-armed after a new sweep")
    n._state_cb(String(data="mission"))
    expect(n._post_sweep_until is None, "E2: state change cancels the cooldown")

    ok = all(results)
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    n.destroy_node()
    h.destroy_node()
    rclpy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
