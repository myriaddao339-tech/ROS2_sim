#!/usr/bin/env python3
"""
test_extract_blocks.py – unit tests for DetectionNode._extract_blocks.

Puts the two merge-related hypotheses from test_logs.txt against the REAL
production code:
  H2 – gap with NO valid depth: the code judges the gap at the nearer
       obstacle's distance, d_gap = min(cur[2], nxt[2]) (conservative
       -> merge).  A far, depth-valid gap splits.
  H3 – cur/nxt are mutable lists: the in-place mutation is intended
       (it extends the current merged block); the block list must stay
       correct across merges and splits, and repeated calls must give
       identical results.

Usage: source install/setup.bash && python3 test_scripts/test_extract_blocks.py
"""
import math

import numpy as np
import rclpy

from sentinel_oda.detection_node import DetectionNode

H, W, FOCAL, CX = 20, 200, 320.0, 100.0
TRIGGER = 9.5


def make_band(comps, gap_depth):
    """Synthetic band: obstacle segments (x0, x1, depth) with the columns
    between them set to gap_depth (float -> valid far depth, nan -> no
    valid depth, like sky / dropouts)."""
    band = np.full((H, W), np.nan, dtype=np.float32)
    for x0, x1, d in comps:
        band[:, x0 : x1 + 1] = d
    for (x0, x1, _d), (nx0, _nx1, _nd) in zip(comps, comps[1:]):
        band[:, x1 + 1 : nx0] = gap_depth
    return band


def blocks_summary(blocks):
    return [(round(b.distance, 3), round(b.left, 3), round(b.width, 3)) for b in blocks]


def expect(cond, label):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def main():
    rclpy.init()
    node = DetectionNode()
    ok = True

    # --- H2a: far, depth-valid gap -> split into two blocks ---
    band = make_band([(20, 40, 5.0), (60, 80, 5.0)], gap_depth=50.0)
    blocks = node._extract_blocks(band, 0, H, TRIGGER, CX, FOCAL)
    ok &= expect(len(blocks) == 2, f"H2a far-valid gap splits (got {blocks_summary(blocks)})")

    # --- H2b: gap with NO valid depth -> conservative merge (1 block) ---
    band = make_band([(20, 40, 5.0), (60, 80, 5.0)], gap_depth=np.nan)
    blocks = node._extract_blocks(band, 0, H, TRIGGER, CX, FOCAL)
    merged_ok = len(blocks) == 1 and abs(blocks[0].distance - 5.0) < 1e-6
    ok &= expect(merged_ok, f"H2b no-depth gap merges conservatively (got {blocks_summary(blocks)})")

    # --- touching components -> one block ---
    band = make_band([(20, 40, 5.0), (41, 60, 5.0)], gap_depth=np.nan)
    blocks = node._extract_blocks(band, 0, H, TRIGGER, CX, FOCAL)
    ok &= expect(len(blocks) == 1, f"touching components merge (got {blocks_summary(blocks)})")

    # --- H3: merge A+B (no-depth gap) and split C (far-valid gap) ---
    comps = [(20, 40, 5.0), (60, 80, 5.0), (120, 140, 6.0)]
    band = np.full((H, W), np.nan, dtype=np.float32)
    for x0, x1, d in comps:
        band[:, x0 : x1 + 1] = d
    band[:, 41:60] = np.nan       # gap A-B: no depth -> merge
    band[:, 81:120] = 50.0        # gap B-C: far depth -> split
    blocks = node._extract_blocks(band, 0, H, TRIGGER, CX, FOCAL)
    got = blocks_summary(blocks)
    exp_first = (5.0, (20 - CX) * 5.0 / FOCAL - 0.2, 60.0 * 5.0 / FOCAL)
    exp_last = (6.0, (120 - CX) * 6.0 / FOCAL - 0.2, 20.0 * 6.0 / FOCAL)
    chk = (
        len(blocks) == 2
        and all(abs(a - b) < 0.02 for a, b in zip(got[0], exp_first))
        and all(abs(a - b) < 0.02 for a, b in zip(got[1], exp_last))
    )
    ok &= expect(chk, f"H3 merge+split chain correct (got {got}, expected ~{exp_first}, {exp_last})")

    # --- H3: idempotence – mutation must not corrupt a second call ---
    blocks2 = node._extract_blocks(band, 0, H, TRIGGER, CX, FOCAL)
    ok &= expect(
        blocks_summary(blocks2) == got,
        f"H3 repeated call identical (got {blocks_summary(blocks2)})",
    )

    rclpy.shutdown()
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
