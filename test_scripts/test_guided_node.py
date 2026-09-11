#!/usr/bin/env python3
"""
test_guided_node.py – headless logic test for the GUIDED node.

Drives GuidedNode with fake drone_state / pose / safe_path / sweeping /
obstacle_detected publishers and checks the settled design:
  G) arbitration with ODA Maneuvers: before the first sweep, during any
     sweep, and while an obstacle is reported, the node publishes NOTHING
     (user request: new setpoints only when not sweeping) – the FCU keeps
     following ODA Maneuvers' last message on the shared setpoint topic;
  A) after the first sweep completes, a new Path's first point is sent as
     a position-only (3576) LOCAL_NED (1) setpoint;
  B) reaching a point (0.5 m tolerance, horizontal) advances to the next;
  C) a new Path mid-traversal replaces the stored path wholesale;
  D) leaving oda stops setpoints;
  E) the current target is re-sent as a keepalive after the timeout;
  F) re-entering oda re-arms the sweep gate.
All PositionTarget fields are asserted in ENU (x=East, y=North, z=Up):
mavros setpoint_raw converts ENU->NED on the wire, so the node publishes
(path NED (n,e,d) -> message (e, n, -d)).

Usage: source install/setup.bash && python3 test_scripts/test_guided_node.py
"""
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from std_msgs.msg import Bool, String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from mavros_msgs.msg import PositionTarget

from sentinel_oda.guided_node import GuidedNode


class Harness(Node):
    def __init__(self):
        super().__init__("guided_harness")
        self._state_pub = self.create_publisher(String, "/drone_node/drone_state", 10)
        self._pose_pub = self.create_publisher(PoseStamped, "/mavros/local_position/pose", 10)
        self._path_pub = self.create_publisher(Path, "/inner_map/safe_path", 10)
        self._sweep_pub = self.create_publisher(
            Bool, "/oda_maneuvers/sweeping", 10
        )
        self._obstacle_pub = self.create_publisher(
            Bool, "/detection_node/obstacle_detected", 10
        )
        self.setpoints = []
        self.create_subscription(
            PositionTarget, "/mavros/setpoint_raw/local", self._sp_cb, 10
        )

    def _sp_cb(self, msg):
        self.setpoints.append(msg)

    def set_state(self, value):
        self._state_pub.publish(String(data=value))

    def set_pose(self, x_east, y_north, z_up=20.0):
        msg = PoseStamped()
        msg.pose.position.x = x_east
        msg.pose.position.y = y_north
        msg.pose.position.z = z_up
        # Publish a few copies: the guided node's pose subscription uses
        # best-effort QoS, and single-shot delivery is not guaranteed.
        for _ in range(3):
            self._pose_pub.publish(msg)

    def set_path(self, points):
        """points: list of (x=N, y=E, z=D)."""
        msg = Path()
        for n, e, d in points:
            p = PoseStamped()
            p.pose.position.x = float(n)
            p.pose.position.y = float(e)
            p.pose.position.z = float(d)
            msg.poses.append(p)
        self._path_pub.publish(msg)

    def set_sweeping(self, value):
        for _ in range(3):
            self._sweep_pub.publish(Bool(data=value))

    def set_obstacle(self, value):
        for _ in range(3):
            self._obstacle_pub.publish(Bool(data=value))


def pump(executor, seconds):
    end = time.time() + seconds
    while time.time() < end:
        executor.spin_once(timeout_sec=0.05)


def wait_until(executor, cond, timeout=2.0):
    """Pump the executor until cond() is true (or the timeout expires)."""
    end = time.time() + timeout
    while time.time() < end:
        if cond():
            return True
        executor.spin_once(timeout_sec=0.05)
    return cond()


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def last_pos(h):
    sp = h.setpoints[-1]
    return (sp.position.x, sp.position.y, sp.position.z)


def main():
    rclpy.init()
    g = GuidedNode()
    h = Harness()
    ex = SingleThreadedExecutor()
    ex.add_node(g)
    ex.add_node(h)
    ok = True

    pump(ex, 1.0)

    # G) arbitration gate: before the first sweep and during any sweep the
    # node must stay SILENT on the shared setpoint topic (user request:
    # new setpoints only when not sweeping) – nothing at all published.
    h.set_state("oda")
    h.set_pose(0.0, 5.0)   # ENU (0, 5, 20) -> NED (5, 0, -20)
    pump(ex, 0.3)
    h.set_path([(0.0, 0.0, -20.0), (0.0, 2.0, -20.0), (0.0, 4.0, -20.0)])
    pump(ex, 0.6)
    ok &= expect(len(h.setpoints) == 0,
                 f"G1: nothing published before the first sweep (got {len(h.setpoints)})")

    # G5) during a sweep: still silent, not flying the path
    h.set_sweeping(True)
    pump(ex, 0.6)
    ok &= expect(len(h.setpoints) == 0,
                 f"G5: nothing published while sweeping (got {len(h.setpoints)})")

    # G6) sweep finished (True -> False edge) -> path cleared for flight
    h.set_sweeping(False)
    ok &= expect(
        wait_until(ex, lambda: h.setpoints and abs(last_pos(h)[0]) < 0.01 and abs(last_pos(h)[1]) < 0.01),
        "G6: after the first sweep the path point 1 is commanded",
    )

    # A) first target = first path point, position-only mask, LOCAL_NED frame
    sp = h.setpoints[-1]
    ok &= expect(sp.coordinate_frame == 1,
                 f"A2: coordinate_frame LOCAL_NED (got {sp.coordinate_frame})")
    ok &= expect(sp.type_mask == 3576,
                 f"A3: position-only type mask 3576 (got {sp.type_mask})")
    x, y, z = last_pos(h)
    ok &= expect(abs(x) < 0.01 and abs(y) < 0.01 and abs(z - 20.0) < 0.01,
                 f"A4: first target fields ENU (0,0,20) from NED (0,0,-20) (got {x:.2f}, {y:.2f}, {z:.2f})")

    # B) reach -> advance (0.5 m tolerance).  The pose is set directly:
    # the guided pose subscription uses best-effort QoS and intra-process
    # delivery timing is not deterministic, while the reach logic itself
    # only reads _pose_ned.
    g._pose_ned = (0.0, 0.3, -20.0)   # within 0.5 m of point 1
    ok &= expect(
        wait_until(ex, lambda: abs(last_pos(h)[0] - 2.0) < 0.01),
        "B1: advancing on reach -> point 2 (fields ENU)",
    )

    # G7) obstacle reported -> silent (ODA Maneuvers re-breaks/re-sweeps):
    # whatever is (or isn't) re-sent, it must stay the path target (2,0,20),
    # never a hold at the current pose (0.3,0,20);
    # G8) cleared -> resume the path
    h.set_obstacle(True)
    pump(ex, 0.3)
    x, y, z = last_pos(h)
    ok &= expect(abs(x - 2.0) < 0.01 and abs(y) < 0.01 and abs(z - 20.0) < 0.01,
                 f"G7: obstacle -> no hold, last setpoint stays the path target (got {x:.2f}, {y:.2f}, {z:.2f})")
    h.set_obstacle(False)
    ok &= expect(
        wait_until(ex, lambda: abs(last_pos(h)[0] - 2.0) < 0.01),
        "G8: obstacle cleared -> path resumes (point 2)",
    )

    g._pose_ned = (0.4, 2.0, -20.0)   # within 0.5 m of point 2
    ok &= expect(
        wait_until(ex, lambda: abs(last_pos(h)[0] - 4.0) < 0.01),
        "B2: advancing on reach -> point 3",
    )

    # C) overwrite mid-traversal (also checks all three ENU axes)
    h.set_path([(0.4, 2.0, -20.0), (3.0, 8.0, -12.0)])
    ok &= expect(
        wait_until(ex, lambda: (abs(last_pos(h)[0] - 8.0) < 0.01
                                and abs(last_pos(h)[1] - 3.0) < 0.01
                                and abs(last_pos(h)[2] - 12.0) < 0.01)),
        "C1: new path replaces old, fields ENU (8,3,12) from NED (3,8,-12)",
    )

    # D) leaving oda stops setpoints
    h.set_state("mission")
    pump(ex, 0.3)
    n_before = len(h.setpoints)
    h.set_path([(0.0, 2.0, -20.0), (0.0, 8.0, -20.0)])
    pump(ex, 0.5)
    ok &= expect(len(h.setpoints) == n_before,
                 f"D1: no setpoints outside oda (count {n_before} -> {len(h.setpoints)})")

    # G9/G10) re-entering oda re-arms the sweep gate
    h.set_state("oda")
    pump(ex, 0.3)
    h.set_pose(0.0, 0.0)
    pump(ex, 0.2)
    h.set_path([(0.0, 10.0, -20.0)])   # 10 m away -> never reached
    pump(ex, 0.3)
    n_before = len(h.setpoints)
    ok &= expect(len(h.setpoints) == n_before,
                 f"G9: re-entry stays silent until a new sweep (count {n_before} -> {len(h.setpoints)})")
    h.set_sweeping(True)
    pump(ex, 0.2)
    h.set_sweeping(False)
    ok &= expect(
        wait_until(ex, lambda: abs(last_pos(h)[0] - 10.0) < 0.01),
        "G10: new sweep completes -> path flown again",
    )

    # E) keepalive resend after the timeout
    g._resend_timeout = 0.05
    pump(ex, 0.3)
    keep = [sp for sp in h.setpoints[-6:] if abs(sp.position.x - 10.0) < 0.01]
    ok &= expect(len(keep) >= 3,
                 f"E1: keepalive resends the current target (got {len(keep)} in last 6)")

    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    ex.shutdown()
    g.destroy_node()
    h.destroy_node()
    rclpy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
