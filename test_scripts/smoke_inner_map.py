#!/usr/bin/env python3
"""
smoke_inner_map.py – headless logic test for the Inner Map node.

Runs InnerMap in-process and drives it with fake pose / drone_state /
target_waypoint / obstacle_info publishers.  Checks:
  A) clear grid  -> safe_path published, 4-connected (no diagonals)
  B) ring of danger tiles around the drone -> dead_end_detected True
  C) goal tile dangerous -> waypoint_skip True
  D) standby resets the grid -> path computed again afterwards

Usage: source install/setup.bash && python3 test_scripts/smoke_inner_map.py
"""

import math
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from std_msgs.msg import Bool, String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

from sentinel_oda_msgs.msg import ObstacleBlock, ObstacleInfo
from sentinel_oda.inner_map import InnerMap


class Harness(Node):
    def __init__(self):
        super().__init__("inner_map_harness")
        self._state_pub = self.create_publisher(String, "/drone_node/drone_state", 10)
        self._pose_pub = self.create_publisher(PoseStamped, "/mavros/local_position/pose", 10)
        self._target_pub = self.create_publisher(PoseStamped, "/mission_node/target_waypoint", 10)
        self._info_pub = self.create_publisher(ObstacleInfo, "/detection_node/obstacle_info", 10)

        self.last_path = None
        self.last_dead_end = None
        self.last_skip = None
        self.create_subscription(Path, "/inner_map/safe_path", self._path_cb, 10)
        self.create_subscription(Bool, "/inner_map/dead_end_detected", self._dead_cb, 10)
        self.create_subscription(Bool, "/inner_map/waypoint_skip", self._skip_cb, 10)

    def _path_cb(self, msg):
        self.last_path = msg

    def _dead_cb(self, msg):
        self.last_dead_end = msg.data

    def _skip_cb(self, msg):
        self.last_skip = msg.data

    # ---- helpers ----
    def set_state(self, value):
        self._state_pub.publish(String(data=value))

    def set_pose(self, x_east, y_north, z_up=20.0):
        msg = PoseStamped()
        msg.pose.position.x = x_east
        msg.pose.position.y = y_north
        msg.pose.position.z = z_up
        self._pose_pub.publish(msg)

    def set_target(self, x_north, y_east, z_down=-20.0):
        msg = PoseStamped()
        msg.pose.position.x = x_north
        msg.pose.position.y = y_east
        msg.pose.position.z = z_down
        self._target_pub.publish(msg)

    def send_blocks(self, executor, heading, blocks, times=10):
        """Publish obstacle_info `times` times at the given ENU heading,
        spinning the executor between publishes so nothing is dropped."""
        info = ObstacleInfo()
        info.current_heading = heading
        for d, left, width in blocks:
            b = ObstacleBlock()
            b.distance = d
            b.left = left
            b.width = width
            info.blocks.append(b)
        info.closest_distance = blocks[0][0]
        info.obstacle_width = blocks[0][2]
        info.obstacle_left = blocks[0][1]
        for _ in range(times):
            self._info_pub.publish(info)
            executor.spin_once(timeout_sec=0.02)


def pump(executor, node, seconds):
    end = time.time() + seconds
    while time.time() < end:
        executor.spin_once(timeout_sec=0.05)


def expect(cond, label):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}")
    return cond


def main():
    rclpy.init()
    inner = InnerMap()
    h = Harness()
    executor = SingleThreadedExecutor()
    executor.add_node(inner)
    executor.add_node(h)

    ok = True

    # Let DDS discovery complete before publishing anything.
    pump(executor, inner, 1.0)

    # A) clear path
    h.set_state("oda")
    h.set_pose(0.0, 0.0)
    h.set_target(40.0, 0.0)
    pump(executor, inner, 1.0)
    ok &= expect(h.last_path is not None and len(h.last_path.poses) > 1,
                 "A1: safe_path published on clear grid")
    if h.last_path is not None:
        # 4-connectivity: consecutive tile-centre poses must be
        # axis-aligned, one tile (2 m) apart.
        pts = [(p.pose.position.x, p.pose.position.y) for p in h.last_path.poses[1:]]
        if not pts:
            ok &= expect(False, "A2: path is 4-connected (no diagonals)")
        else:
            grid = True
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                dx, dy = abs(x2 - x1), abs(y2 - y1)
                if not ((abs(dx - 2.0) < 0.01 and dy < 0.01) or
                        (dx < 0.01 and abs(dy - 2.0) < 0.01)):
                    grid = False
            ok &= expect(grid, "A2: path is 4-connected (no diagonals)")
            # Goal (40, 0) lies in tile (120, 100) whose centre is (41, 1).
            ok &= expect(abs(pts[-1][0] - 41.0) < 0.01 and abs(pts[-1][1] - 1.0) < 0.01,
                         "A3: path reaches the goal tile")
    ok &= expect(not h.last_dead_end, "A4: no dead end on a clear grid")

    # B) ring of danger tiles around the drone -> no path -> dead end
    # Neighbour tiles at d=3 m: east (0,3), north (3,0), west (0,-3),
    # south (-3,0).  heading: 0=East, pi/2=North, pi=West, -pi/2=South.
    h.last_dead_end = None
    h.set_pose(0.0, 0.0)
    h.set_target(40.0, 0.0)
    pump(executor, inner, 0.3)
    h.send_blocks(executor, 0.0, [(3.0, -1.5, 3.0)])
    h.send_blocks(executor, math.pi / 2, [(3.0, -1.5, 3.0)])
    h.send_blocks(executor, math.pi, [(3.0, -1.5, 3.0)])
    h.send_blocks(executor, -math.pi / 2, [(3.0, -1.5, 3.0)])
    pump(executor, inner, 1.0)
    ok &= expect(h.last_dead_end is True, "B1: dead_end_detected when boxed in")

    # C) goal tile dangerous -> waypoint_skip
    h.last_skip = None
    h.set_target(3.0, 0.0)  # tile (101, 100), now dangerous
    pump(executor, inner, 1.0)
    ok &= expect(h.last_skip is True, "C1: waypoint_skip when goal tile is dangerous")

    # D) standby resets the grid -> a fresh plan succeeds
    h.last_path = None
    h.last_dead_end = None
    h.set_state("standby")
    pump(executor, inner, 0.5)
    h.set_state("oda")
    pump(executor, inner, 0.3)
    h.set_pose(0.0, 0.0)
    h.set_target(10.0, 0.0)
    pump(executor, inner, 1.0)
    ok &= expect(h.last_path is not None and len(h.last_path.poses) > 1,
                 "D1: grid reset on standby (path replanned)")
    ok &= expect(h.last_dead_end is not True,
                 "D2: no dead end after reset")

    print("=" * 40)
    print("ALL PASS" if ok else "SOME CHECKS FAILED")
    executor.shutdown()
    inner.destroy_node()
    h.destroy_node()
    rclpy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
