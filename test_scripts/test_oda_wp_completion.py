#!/usr/bin/env python3
"""
test_oda_wp_completion.py – headless test for waypoint completion during ODA.

The ODA package flies the drone itself in GUIDED mode, so the FCU never
reports "waypoint reached".  Two fixes are covered:

  MissionNode (position-based completion while drone_state == oda):
    A) drone within oda_wp_reach_radius of an intermediate target ->
       waypoint_reached published once, target advanced;
    B) drone within radius of the LAST waypoint -> mission_finished
       published (the current obstacle_course.plan has only 2 real
       waypoints, so this is the live case);
    C) the check stays silent outside the radius.

  DroneNode (state machine):
    D) waypoint_reached in oda -> mission (resume);
    E) mission_finished in oda -> landing (the last-waypoint edge case).

Usage: source /opt/ros/humble/setup.bash && source install/setup.bash &&
       python3 test_scripts/test_oda_wp_completion.py
"""
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from std_msgs.msg import Bool, Int32, String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State

from sentinel_mission.mission_node import MissionNode
from sentinel_mission.drone_node import DroneNode


def pose_ned_msg(x_north, y_east, z_down=-20.0):
    """Build a /mavros/local_position/pose-style message (ENU fields)."""
    msg = PoseStamped()
    msg.pose.position.x = y_east    # ENU East = NED y
    msg.pose.position.y = x_north   # ENU North = NED x
    msg.pose.position.z = -z_down   # ENU Up = -NED z
    return msg


class MissionHarness(Node):
    def __init__(self):
        super().__init__("oda_wp_mission_harness")
        self.reached = []
        self.finished = []
        self.create_subscription(
            Int32, "/mission_node/waypoint_reached", self._r_cb, 10
        )
        self.create_subscription(
            Bool, "/mission_node/mission_finished", self._f_cb, 10
        )

    def _r_cb(self, msg):
        self.reached.append(msg.data)

    def _f_cb(self, msg):
        self.finished.append(msg.data)


def pump(executor, seconds):
    end = time.time() + seconds
    while time.time() < end:
        executor.spin_once(timeout_sec=0.05)


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def main():
    rclpy.init()
    h = MissionHarness()
    ex = SingleThreadedExecutor()
    ex.add_node(h)
    ok = True

    # ================= MissionNode: ODA position check =================
    m = MissionNode()
    ex.add_node(m)
    pump(ex, 0.5)

    # Loaded mission: home + 2 real waypoints (obstacle_course.plan):
    # WP1 = NED (0, 5, -20), WP2 = NED (0, 180, -20) = LAST.
    m._drone_state_cb(String(data="oda"))

    # A) near WP1 -> waypoint_reached 1, target advances to 2.
    m._pose_cb(pose_ned_msg(0.5, 5.2))
    m._republish_target()   # timer path (1 Hz in production)
    pump(ex, 0.4)
    ok &= expect(h.reached == [1],
                 f"A: waypoint_reached 1 published (got {h.reached})")
    ok &= expect(m.target_index == 2,
                 f"A2: target advanced to 2 (got {m.target_index})")

    # C) far from WP2 -> nothing published.
    m._pose_cb(pose_ned_msg(0.0, 100.0))
    m._republish_target()
    pump(ex, 0.4)
    ok &= expect(len(h.reached) == 1 and not h.finished,
                 "C: far from the waypoint -> nothing published")

    # B) near WP2 (last) -> mission_finished published.
    m._pose_cb(pose_ned_msg(0.2, 179.6))
    m._republish_target()
    pump(ex, 0.6)
    ok &= expect(any(h.finished),
                 f"B: mission_finished for the last waypoint (got {h.finished})")

    m.destroy_node()

    # ================= DroneNode: state machine =================
    d = DroneNode()
    d._init_timer.cancel()      # silence the startup init sequence
    ex.add_node(d)
    pump(ex, 0.5)
    st = State()
    st.connected = True
    st.armed = True
    st.mode = "GUIDED"
    d.fcu_state = st

    # D) waypoint_reached in oda -> mission (resume).
    d._sm.set_state("oda")
    d._current_state = "oda"
    d._wp_reached_cb(Int32(data=1))
    pump(ex, 0.5)
    ok &= expect(d._current_state == "mission",
                 f"D: waypoint_reached in oda -> mission (got {d._current_state})")
    d._init_timer.cancel()
    d.destroy_node()

    # E) mission_finished in oda -> landing (last-waypoint edge case).
    d2 = DroneNode()
    d2._init_timer.cancel()
    ex.add_node(d2)
    pump(ex, 0.5)
    d2._sm.set_state("oda")
    d2._current_state = "oda"
    d2.do_mission_finished()
    pump(ex, 0.5)
    ok &= expect(d2._current_state == "landing",
                 f"E: mission_finished in oda -> landing (got {d2._current_state})")
    d2.destroy_node()

    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    ex.shutdown()
    h.destroy_node()
    rclpy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
