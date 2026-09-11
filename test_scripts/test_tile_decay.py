#!/usr/bin/env python3
"""
test_tile_decay.py – unit tests for the danger-tile invalidation (decay).

A dangerous tile that receives no fresh report for danger_decay_timeout
must become safe again, while a tile that keeps being observed must stay
dangerous, and danger_decay_timeout = 0 must disable the decay entirely.
The node clock is wall time, so the test stamps _last_hit directly to
emulate the passage of time.

Usage: source install/setup.bash && python3 test_scripts/test_tile_decay.py
"""
import numpy as np
import rclpy

from sentinel_oda.inner_map import InnerMap


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def main():
    rclpy.init()
    im = InnerMap()
    im._drone_state = "oda"
    im._pose_ned = (0.0, 0.0, -20.0)
    im._confirm = 1
    im._safe_r = 1.7   # deterministic marks for the test geometry
    ok = True

    # One block straight east at 3 m -> east tiles dangerous.
    im._mark_block(0.0, 3.0, -1.5, 3.0)
    n_danger = int(np.count_nonzero(im._dangerous))
    ok &= expect(n_danger > 0, f"tile marked dangerous ({n_danger} tiles)")

    # Fresh re-observation prevents decay.
    im._mark_block(0.0, 3.0, -1.5, 3.0)
    decayed = im._expire_counters()
    ok &= expect(decayed == 0 and int(np.count_nonzero(im._dangerous)) == n_danger,
                 "fresh re-observation keeps the tile dangerous")

    # Simulate 31 s without any report: the tile must decay back to safe.
    im._last_hit[:] = im._now() - 31.0
    decayed = im._expire_counters()
    ok &= expect(decayed == n_danger and int(np.count_nonzero(im._dangerous)) == 0,
                 f"stale tiles decay after the timeout ({decayed} cleared)")

    # Decay disabled (0) must keep the tile permanent.
    im._decay = 0.0
    im._mark_block(0.0, 3.0, -1.5, 3.0)
    im._last_hit[:] = im._now() - 1000.0
    decayed = im._expire_counters()
    ok &= expect(decayed == 0 and int(np.count_nonzero(im._dangerous)) > 0,
                 "decay disabled (timeout 0) keeps tiles permanent")

    rclpy.shutdown()
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
