#!/usr/bin/env python3
"""
test_wall_smear.py – reproduce the ODA-sweep danger-tile smear on InnerMap.

Runs the REAL production chain for every frame of the sweep:
  1. synthesise the depth band the Gazebo camera would see for capture
     heading theta (box west wall: face at East x=139, y -4..4, drone
     6 m in front),
  2. DetectionNode._extract_blocks on that band -> ObstacleBlock list,
  3. InnerMap._mark_block with the heading detection stamps on the
     message.

  STALE run (current behaviour): heading = theta + 27 deg (the Gazebo
      depth pipeline lags the capture heading by ~0.3 s at 90 deg/s).
  SYNC run (target behaviour):   heading = theta.

PASS when STALE smears danger tiles off the wall line and SYNC leaves
essentially none while still flagging the wall itself.

Usage: source install/setup.bash && python3 test_scripts/test_wall_smear.py
"""
import math

import numpy as np
import rclpy

from sentinel_oda.detection_node import DetectionNode
from sentinel_oda.inner_map import InnerMap

WALL_X = 139.0               # box west wall face, NED East
WALL_HALF_Y = 4.0            # wall spans y -4..4
DIST = 3.0                   # drone ends up ~3 m from the face after the brake drift
FOV_HALF = math.radians(26.75)
WALL_HALF_ANG = math.atan2(WALL_HALF_Y, DIST)   # wall angular half-extent from the drone
LAG = math.radians(27.0)     # 0.3 s at 90 deg/s slew
TRIGGER = 9.5
W, FOCAL, CX = 200, 320.0, 100.0
BAND_H = 3


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def make_band(theta):
    """Depth band for capture heading theta: wall pixels get the exact
    range to the x=139 plane, everything else is NaN."""
    band = np.full((BAND_H, W), np.nan, dtype=np.float32)
    for x in range(W):
        b_rel = math.atan((x - CX) / FOCAL)      # image right -> +bearing
        b_w = theta + b_rel
        if abs(b_w) <= WALL_HALF_ANG:
            band[:, x] = DIST / math.cos(b_w)
    return band


def reset_map(im):
    im._counts[:] = 0
    im._last_hit[:] = np.nan
    im._dangerous[:] = False
    im._danger_tiles = 0


def wall_stats(im):
    on_line = off_line = 0
    # _dangerous is indexed [iy(East), ix(North)] -> nonzero gives
    # (row=East index, col=North index).
    for iy, ix in zip(*np.nonzero(im._dangerous)):
        cy = (iy - im._half) * im._tile + im._tile / 2.0   # EAST coordinate
        if abs(cy - WALL_X) <= 3.5:
            on_line += 1
        else:
            off_line += 1
    return on_line, off_line


def run_sweep(det, im, mode):
    """mode 'stale': per-frame heading lag 0.15-0.35 s (Gazebo pipeline),
    mode 'sync': zero lag."""
    reset_map(im)
    frames = 0
    lags = [math.radians(13.5), math.radians(22.5), math.radians(31.5)]
    # The ODA fan pans the drone across +90, -45x4, +90: the camera sweeps
    # the full [-90, +90] heading range around east.
    for i, theta_deg in enumerate(np.arange(-90.0, 90.0, 0.5)):
        theta = math.radians(theta_deg)
        blocks = det._extract_blocks(make_band(theta), 0, BAND_H, TRIGGER, CX, FOCAL)
        if not blocks:
            continue
        lag = lags[i % 3] if mode == "stale" else 0.0
        for b in blocks:
            im._mark_block(theta + lag, b.distance, b.left, b.width)
        frames += 1
    return frames


def main():
    rclpy.init()
    det = DetectionNode()
    im = InnerMap()
    im._drone_state = "oda"
    im._pose_ned = (0.0, WALL_X - DIST, -20.0)   # NED (North, East, Down)
    im._confirm = 1                               # unit test: 1 hit marks a tile
    im._safe_r = 1.7                              # this test targets heading staleness, not radius
    ok = True

    frames = run_sweep(det, im, mode="stale")
    on_l, off_l = wall_stats(im)
    print(f"STALE: {frames} frames -> danger tiles: {on_l} on wall, {off_l} off wall")
    stale_off = off_l
    ok &= expect(off_l > 0, "STALE run reproduces the smear (off-wall danger tiles)")

    frames = run_sweep(det, im, mode="sync")
    on_l, off_l = wall_stats(im)
    print(f"SYNC: {frames} frames -> danger tiles: {on_l} on wall, {off_l} off wall")
    ok &= expect(off_l <= 2, "SYNC run: (almost) zero off-wall danger tiles")
    ok &= expect(on_l > 5, "SYNC run still flags the wall line itself")
    ok &= expect(stale_off > off_l, "heading sync strictly reduces the smear")

    rclpy.shutdown()
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
