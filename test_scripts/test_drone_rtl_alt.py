#!/usr/bin/env python3
"""
test_drone_rtl_alt.py – headless test for the landing RTL-altitude raise.

Drives DroneNode into the landing state (mission -> emergency) with fake
MAVROS services and checks the settled behaviour:
  1. ParamSetV2(RTL_ALT_M = 100.0 m = 100 m) is called BEFORE the
     SetMode(RTL) switch;
  2. the mode requested is RTL;
  3. after the FCU confirms RTL, the node stays in landing.

Usage: source install/setup.bash && python3 test_scripts/test_drone_rtl_alt.py
"""
import time

import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node

from mavros_msgs.msg import State
from mavros_msgs.srv import ParamSetV2, SetMode

from sentinel_mission.drone_node import DroneNode


class Harness(Node):
    def __init__(self):
        super().__init__("drone_rtl_harness")
        self._state_pub = self.create_publisher(State, "/mavros/state", 10)
        # Ordered record of every MAVROS service call:
        # ("param", param_id, integer_value) / ("mode", custom_mode)
        self.calls = []
        self._param_srv = self.create_service(ParamSetV2, "/mavros/param/set", self._param_cb)
        self._mode_srv = self.create_service(SetMode, "/mavros/set_mode", self._mode_cb)

    def _param_cb(self, req, res):
        self.calls.append(("param", req.param_id, req.value.double_value))
        res.success = True
        res.value = req.value
        return res

    def _mode_cb(self, req, res):
        self.calls.append(("mode", req.custom_mode))
        res.mode_sent = True
        return res

    def set_fcu(self, mode, armed=True):
        msg = State()
        msg.connected = True
        msg.armed = armed
        msg.mode = mode
        msg.system_status = 4
        self._state_pub.publish(msg)


def pump(executor, seconds):
    end = time.time() + seconds
    while time.time() < end:
        executor.spin_once(timeout_sec=0.05)


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def main():
    rclpy.init()
    node = DroneNode()
    node._init_timer.cancel()   # silence the startup init sequence
    h = Harness()
    ex = SingleThreadedExecutor()
    ex.add_node(node)
    ex.add_node(h)
    ok = True

    pump(ex, 1.0)               # DDS + service discovery

    h.set_fcu("GUIDED", armed=True)
    pump(ex, 0.3)

    # Enter landing exactly like an emergency would: mission -> landing.
    node._sm.set_state("mission")
    node.do_emergency()
    pump(ex, 1.5)

    param_idx = next((i for i, c in enumerate(h.calls) if c[0] == "param"), None)
    mode_idx = next((i for i, c in enumerate(h.calls) if c[0] == "mode"), None)

    ok &= expect(param_idx is not None, f"ParamSet called ({h.calls})")
    ok &= expect(mode_idx is not None, f"SetMode called ({h.calls})")
    if param_idx is not None and mode_idx is not None:
        ok &= expect(param_idx < mode_idx,
                     f"RTL_ALT set BEFORE the RTL switch (order: {h.calls})")
    if param_idx is not None:
        ok &= expect(h.calls[param_idx][1] == "RTL_ALT_M",
                     f"param id = RTL_ALT_M (got {h.calls[param_idx][1]})")
        ok &= expect(h.calls[param_idx][2] == 100.0,
                     f"RTL_ALT_M = 100.0 m (got {h.calls[param_idx][2]})")
    if mode_idx is not None:
        ok &= expect(h.calls[mode_idx][1] == "RTL",
                     f"mode requested = RTL (got {h.calls[mode_idx][1]})")

    # FCU confirms RTL -> the landing timer cancels, state stays landing.
    h.set_fcu("RTL", armed=True)
    pump(ex, 1.0)
    ok &= expect(node._current_state == "landing",
                 f"still in landing after RTL confirmation (got {node._current_state})")

    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    ex.shutdown()
    node.destroy_node()
    h.destroy_node()
    rclpy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
