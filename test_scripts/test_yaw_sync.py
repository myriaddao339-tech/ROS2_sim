#!/usr/bin/env python3
"""
test_yaw_sync.py – unit tests for DetectionNode._yaw_at (capture-time yaw).

Feeds a synthetic pose history (yaw sweeping at 90 deg/s) and checks the
wrap-aware interpolation: linear region, between samples, across the
+/-pi wrap, and the thin-history fallback.

Usage: source install/setup.bash && python3 test_scripts/test_yaw_sync.py
"""
import math

import rclpy

from sentinel_oda.detection_node import DetectionNode


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def short_arc(a, b):
    return (a - b + math.pi) % (2.0 * math.pi) - math.pi


def fill(node, yaw_fn, t0=0.0, t1=1.0, step=0.02):
    node._pose_hist.clear()
    t = t0
    while t <= t1 + 1e-9:
        node._pose_hist.append((t, yaw_fn(t)))
        t += step


def main():
    rclpy.init()
    node = DetectionNode()
    ok = True

    # linear region, 90 deg/s
    rate = math.radians(90.0)
    base = 0.5
    fill(node, lambda t: base + rate * t)
    y = node._yaw_at(0.055)
    ok &= expect(abs(short_arc(y, base + rate * 0.055)) < 1e-6,
                 f"linear interpolation at 0.055 s (got {y:.4f})")
    y = node._yaw_at(0.0)
    ok &= expect(abs(short_arc(y, base)) < 1e-9, "before history -> first sample")
    y = node._yaw_at(5.0)
    ok &= expect(abs(short_arc(y, base + rate * 1.0)) < 1e-9, "after history -> last sample")

    # wrap: yaw crosses +pi at t = (pi - 3.0) / 0.5
    fill(node, lambda t: 3.0 + 0.5 * t, t0=0.0, t1=1.0)
    y = node._yaw_at(0.29)   # true yaw = 3.145 -> just past +pi (-3.138)
    true = 3.0 + 0.5 * 0.29
    ok &= expect(abs(short_arc(y, true)) < 0.01,
                 f"wrap-aware interpolation across +/-pi (got {y:.4f}, true {true:.4f})")

    # thin history -> None
    node._pose_hist.clear()
    node._pose_hist.append((0.0, 0.0))
    ok &= expect(node._yaw_at(0.0) is None, "single sample -> None (fallback to live yaw)")

    rclpy.shutdown()
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
