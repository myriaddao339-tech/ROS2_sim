#!/usr/bin/env python3
"""
inner_map.py – obstacle-tile map + A* path planning (the "planner").

Runs on the drone.  Only operates while drone_state == "oda".

Responsibilities:
  1. Accumulate Detection's obstacle_info reports into a world-fixed
     tile grid (default 200x200 tiles, 2 m each, centred on the EKF
     origin).  A tile needs `confirm_count` obstacle reports to become
     dangerous, and its confirm counter resets if no report lands within
     `danger_count_timeout` (scattered mistakes can never add up).
     A dangerous tile that receives no new report for
     `danger_decay_timeout` is cleared again – the map self-heals from
     false positives, but only while obstacles keep being re-observed.
  2. Whenever a NEW tile becomes dangerous (or a new target waypoint
     arrives), run A* from the drone's tile to the target waypoint tile.
     Moves are strictly vertical/horizontal between tile centres – no
     diagonals (too risky).
  3. Publish the resulting path as nav_msgs/Path on ~/safe_path for the
     GUIDED node: first point = the drone's current position, then the
     tile centres; z = target waypoint z everywhere.

Outputs to other packages:
  - No path exists -> publish True on ~/dead_end_detected.  The
    Emergency Node treats it like any other emergency and RTL is
    initiated.  Planning keeps retrying on every map change.
  - Target waypoint tile is dangerous or outside the grid -> publish
    True on ~/waypoint_skip; the Mission Node skips to the next waypoint
    and republishes the new target.

Grid lifecycle:
  - The grid is an improvised SLAM: danger tiles persist across
    mission <-> oda transitions.  Leaving ODA clears the charted path
    (empty Path) but keeps the grid.  Only entering "standby" (a new
    flight) resets the map.

Subscribes (absolute paths – these topics belong to other nodes):
  /detection_node/obstacle_info  – sentinel_oda_msgs/ObstacleInfo
  /mavros/local_position/pose     – geometry_msgs/PoseStamped (ENU)
  /drone_node/drone_state         – std_msgs/String
  /mission_node/target_waypoint   – geometry_msgs/PoseStamped (local NED)

Publishes:
  ~/safe_path          – nav_msgs/Path (GUIDED node)
  ~/dead_end_detected  – std_msgs/Bool (Emergency Node)
  ~/waypoint_skip      – std_msgs/Bool (Mission Node)

Coordinate conventions:
  - The grid and the published path are in LOCAL NED metres relative to
    the EKF origin: x = North, y = East, z = Down.
  - /mavros/local_position/pose is ENU (x = East, y = North, z = Up), so
    NED position = (pose.y, pose.x, -pose.z).
  - current_heading in obstacle_info uses Detection's ENU convention
    (0 = East, positive = counterclockwise toward North).  A block point
    at along-axis distance d and right-positive lateral offset c lies at:
        alpha = atan2(c, d)
        world = drone_ned + d * (sin(theta - alpha), cos(theta - alpha))
  - Tile index:  ix = floor(x / tile_size) + grid_tiles / 2.
    Tile centre: x = (ix - grid_tiles / 2) * tile_size + tile_size / 2.
"""

from collections import deque
import heapq
import math

import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from std_msgs.msg import Bool, String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

from sentinel_oda_msgs.msg import ObstacleInfo


class InnerMap(Node):
    """Obstacle-tile map + A* path planner (oda state only)."""

    def __init__(self):
        super().__init__("inner_map")

        # ---- parameters ----
        self.declare_parameter("tile_size", 2.0)              # m per tile
        self.declare_parameter("grid_tiles", 200)             # NxN, EKF origin at the centre
        self.declare_parameter("tile_safe_radius", 1.5)       # m, obstacle-to-tile-centre danger distance
        self.declare_parameter("danger_margin", 0.3)          # m, extension at each block end
        self.declare_parameter("confirm_count", 3)           # reports needed to mark a tile dangerous
        self.declare_parameter("danger_count_timeout", 4.0)   # s, gap that resets a tile's counter
        self.declare_parameter("danger_decay_timeout", 15.0)  # s, unobserved danger tiles become safe again (0 = never)
        self.declare_parameter("segment_step", 0.25)          # m, sampling step along a block
        self.declare_parameter("show_map", False)             # pop-up tile-map window
        self.declare_parameter("map_rate", 5.0)               # Hz, map redraw rate
        self.declare_parameter("map_scale_px", 5)             # px per tile (window = grid_tiles * scale)
        self.declare_parameter("max_yaw_rate_deg", 25.0)      # deg/s; drop obstacle_info while yawing faster
        self.declare_parameter("yaw_gate_holdoff_sec", 0.5)   # s; keep gating after the slew (depth lag)
        self.declare_parameter("yaw_window_sec", 0.35)        # s; window of the yaw-rate estimate

        self._tile = max(0.1, float(self.get_parameter("tile_size").value))
        self._n = max(4, int(self.get_parameter("grid_tiles").value))
        self._half = self._n // 2
        self._safe_r = float(self.get_parameter("tile_safe_radius").value)
        self._margin = float(self.get_parameter("danger_margin").value)
        self._confirm = max(1, int(self.get_parameter("confirm_count").value))
        self._timeout = float(self.get_parameter("danger_count_timeout").value)
        self._decay = max(0.0, float(self.get_parameter("danger_decay_timeout").value))
        self._step = max(0.05, float(self.get_parameter("segment_step").value))
        self._show_map = bool(self.get_parameter("show_map").value)
        self._map_seen = False  # window actually shown at least once (X-close detection)
        map_rate = max(1.0, float(self.get_parameter("map_rate").value))
        self._map_scale = max(1, int(self.get_parameter("map_scale_px").value))
        self._max_yaw_rate = float(self.get_parameter("max_yaw_rate_deg").value)
        self._gate_holdoff = float(self.get_parameter("yaw_gate_holdoff_sec").value)
        self._yaw_window = max(0.1, float(self.get_parameter("yaw_window_sec").value))
        self._yaw_hist = deque(maxlen=64)   # (stamp_seconds, yaw) pose samples
        self._yaw_rate = 0.0                # deg/s, window estimate
        self._gate_until = 0.0              # node-clock s; drop obstacle_info until then
        self._gate_logged = False           # log the drop once per slew burst

        # ---- grid (world-fixed, EKF-origin-centred, local NED) ----
        self._counts = np.zeros((self._n, self._n), dtype=np.uint16)
        self._last_hit = np.full((self._n, self._n), np.nan, dtype=np.float64)
        self._dangerous = np.zeros((self._n, self._n), dtype=bool)
        self._danger_tiles = 0

        # ---- inputs ----
        self._drone_state = "standby"
        self._pose_ned = None        # (x=N, y=E, z=D) local NED metres
        self._target_wp = None       # (x, y, z) local NED metres
        self._path_xy = []           # latest safe path (world NED xy points)

        # ---- subscriptions (absolute paths: other nodes' topics) ----
        self.create_subscription(
            ObstacleInfo, "/detection_node/obstacle_info", self._obstacle_info_cb, 10
        )
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)
        self.create_subscription(
            PoseStamped, "/mission_node/target_waypoint", self._target_cb, 10
        )

        # ---- publishers ----
        self._path_pub = self.create_publisher(Path, "~/safe_path", 10)
        self._dead_end_pub = self.create_publisher(Bool, "~/dead_end_detected", 10)
        self._skip_pub = self.create_publisher(Bool, "~/waypoint_skip", 10)

        # ---- map window (visualisation only) ----
        self._map_timer = self.create_timer(1.0 / map_rate, self._map_cb)

        self.get_logger().info(
            f"Inner Map ready – {self._n}x{self._n} grid of {self._tile:.1f} m "
            f"tiles, danger = {self._confirm} reports within "
            f"{self._timeout:.1f} s"
        )
        if self._show_map:
            self.get_logger().info("Map window enabled – close with X, q or ESC")

    # ==================================================================
    # Callbacks
    # ==================================================================

    def _state_cb(self, msg: String):
        if msg.data == self._drone_state:
            return
        prev = self._drone_state
        self._drone_state = msg.data

        if prev == "oda" and msg.data != "oda":
            # Keep the grid (improvised SLAM), drop the charted path.
            self._publish_path([])
            self.get_logger().info(
                f"Left ODA ({msg.data}) – path cleared, grid kept "
                f"({self._danger_tiles} danger tiles)"
            )
        if msg.data == "standby":
            # New flight – fresh map.
            self._counts[:] = 0
            self._last_hit[:] = np.nan
            self._dangerous[:] = False
            self._danger_tiles = 0
            self._pose_ned = None
            self._target_wp = None
            self.get_logger().info("Standby – tile grid reset for a new flight")

    def _pose_cb(self, msg: PoseStamped):
        p = msg.pose.position
        # ENU (x=E, y=N, z=U) -> NED (x=N, y=E, z=D)
        self._pose_ned = (float(p.y), float(p.x), float(-p.z))

        # Yaw-rate estimate (deg/s) over a short pose-history window.
        # Used to gate obstacle registration during ODA sweep slews:
        # Gazebo depth frames lag the heading by up to ~0.5 s, so blocks
        # seen while the drone rotates fast get painted at stale bearings
        # and smear danger tiles around the drone.
        q = msg.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny, cosy)
        t = float(msg.header.stamp.sec) + float(msg.header.stamp.nanosec) * 1e-9
        self._yaw_hist.append((t, yaw))
        while len(self._yaw_hist) > 1 and self._yaw_hist[0][0] < t - self._yaw_window:
            self._yaw_hist.popleft()
        if len(self._yaw_hist) >= 2:
            t0, y0 = self._yaw_hist[0]
            dt = t - t0
            if dt >= 0.05:
                dy = (yaw - y0 + math.pi) % (2.0 * math.pi) - math.pi
                self._yaw_rate = math.degrees(dy / dt)
                if self._max_yaw_rate > 0.0 and abs(self._yaw_rate) > self._max_yaw_rate:
                    self._gate_until = max(self._gate_until, self._now() + self._gate_holdoff)

    def _target_cb(self, msg: PoseStamped):
        p = msg.pose.position
        self._target_wp = (float(p.x), float(p.y), float(p.z))
        self.get_logger().info(
            f"New target waypoint: NED ({p.x:.1f}, {p.y:.1f}, {p.z:.1f})"
        )
        self._plan_and_publish()

    def _obstacle_info_cb(self, msg: ObstacleInfo):
        # Strictly ODA: if all goes well, the obstacle that triggered ODA
        # is re-captured by Detection during the ODA maneuvers sweep.
        if self._drone_state != "oda":
            return
        if self._pose_ned is None:
            self.get_logger().warn(
                "No pose yet – dropping obstacle_info"
            )
            return

        # Yaw-slew gate: blocks are only trustworthy when the heading was
        # stable at depth-frame capture time.  While the ODA sweep slews
        # (or right after – pipeline lag), drop the report instead of
        # painting tiles at a stale bearing.
        if self._max_yaw_rate > 0.0 and self._now() < self._gate_until:
            if not self._gate_logged:
                self.get_logger().info(
                    "obstacle_info dropped – yaw slew detected "
                    f"(|rate| > {self._max_yaw_rate:.0f} deg/s)"
                )
                self._gate_logged = True
            return
        self._gate_logged = False

        decayed = self._expire_counters()

        # Blocks list is the primary input; fall back to the legacy
        # single-obstacle fields if the list is empty.
        if msg.blocks:
            blocks = [(b.distance, b.left, b.width) for b in msg.blocks]
        elif msg.closest_distance > 0.0:
            blocks = [(msg.closest_distance, msg.obstacle_left, msg.obstacle_width)]
        else:
            blocks = []

        theta = float(msg.current_heading)
        new_danger = False
        for d, left, width in blocks:
            new_danger |= self._mark_block(theta, d, left, width)

        if new_danger or decayed > 0:
            self._plan_and_publish()

    # ==================================================================
    # Grid marking
    # ==================================================================

    def _now(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _expire_counters(self) -> int:
        """Reset confirm counters not re-validated within the timeout, and
        decay dangerous tiles that have not been re-observed within
        danger_decay_timeout.  Returns how many tiles became safe again."""
        now = self._now()
        stale = (
            ~np.isnan(self._last_hit)
            & (now - self._last_hit > self._timeout)
            & ~self._dangerous   # dangerous tiles keep their last_hit for decay
        )
        if np.any(stale):
            self._counts[stale] = 0
            self._last_hit[stale] = np.nan
        decayed = 0
        if self._decay > 0.0:
            unobs = (
                self._dangerous
                & (~np.isnan(self._last_hit))
                & (now - self._last_hit > self._decay)
            )
            if np.any(unobs):
                decayed = int(np.count_nonzero(unobs))
                self._dangerous[unobs] = False
                self._counts[unobs] = 0
                self._last_hit[unobs] = np.nan
                self._danger_tiles -= decayed
                self.get_logger().info(
                    f"Decayed {decayed} danger tile(s) – not re-observed for "
                    f"{self._decay:.1f} s ({self._danger_tiles} remain)"
                )
        return decayed

    def _mark_block(self, theta: float, d: float, left: float, width: float) -> bool:
        """Mark the tiles covered by one obstacle block.

        Returns True if any tile BECAME dangerous with this call.
        """
        if not np.isfinite(d) or d <= 0.0:
            return False

        # Sample the block between its margin-extended edges.  c is the
        # right-positive lateral offset at along-axis distance d; the
        # world point is drone_ned + d * (sin, cos)(theta - atan2(c, d)).
        c_min = left - self._margin
        c_max = left + width + self._margin
        steps = max(2, int(math.ceil((c_max - c_min) / self._step)) + 1)
        c_vals = np.linspace(c_min, c_max, steps)
        angles = theta - np.arctan2(c_vals, d)
        nx, ny = self._pose_ned[0], self._pose_ned[1]
        xs = nx + d * np.sin(angles)
        ys = ny + d * np.cos(angles)

        new_danger = False
        for x, y in zip(xs, ys):
            new_danger |= self._hit_point(float(x), float(y))
        return new_danger

    def _hit_point(self, x: float, y: float) -> bool:
        """Register one obstacle point: bump the confirm counter of every
        non-dangerous tile whose centre is within tile_safe_radius."""
        r = self._safe_r
        ix_min = math.floor((x - r) / self._tile) + self._half
        ix_max = math.floor((x + r) / self._tile) + self._half
        iy_min = math.floor((y - r) / self._tile) + self._half
        iy_max = math.floor((y + r) / self._tile) + self._half
        ix_min = max(0, ix_min)
        ix_max = min(self._n - 1, ix_max)
        iy_min = max(0, iy_min)
        iy_max = min(self._n - 1, iy_max)
        if ix_min > ix_max or iy_min > iy_max:
            return False

        now = self._now()
        new_danger = False
        for iy in range(iy_min, iy_max + 1):
            for ix in range(ix_min, ix_max + 1):
                if self._dangerous[iy, ix]:
                    # Already dangerous – a fresh hit still re-validates
                    # it, so decay only clears tiles that have stopped
                    # being observed.
                    self._last_hit[iy, ix] = now
                    continue
                cx = (ix - self._half) * self._tile + self._tile / 2.0
                cy = (iy - self._half) * self._tile + self._tile / 2.0
                if (cx - x) ** 2 + (cy - y) ** 2 > r * r:
                    continue
                self._counts[iy, ix] += 1
                self._last_hit[iy, ix] = now
                if self._counts[iy, ix] >= self._confirm:
                    self._dangerous[iy, ix] = True
                    self._danger_tiles += 1
                    new_danger = True
                    self.get_logger().info(
                        f"Tile ({ix}, {iy}) marked dangerous "
                        f"(centre NED {cx:.1f}, {cy:.1f}) – "
                        f"{self._danger_tiles} total"
                    )
        return new_danger

    # ==================================================================
    # Planning
    # ==================================================================

    def _world_to_tile(self, x: float, y: float):
        ix = math.floor(x / self._tile) + self._half
        iy = math.floor(y / self._tile) + self._half
        if 0 <= ix < self._n and 0 <= iy < self._n:
            return (ix, iy)
        return None

    def _plan_and_publish(self):
        if self._drone_state != "oda":
            return
        if self._pose_ned is None or self._target_wp is None:
            self.get_logger().warn(
                "Cannot plan yet – waiting for pose and target waypoint"
            )
            return

        sx, sy, _ = self._pose_ned
        gx, gy, gz = self._target_wp
        start = self._world_to_tile(sx, sy)
        goal = self._world_to_tile(gx, gy)

        if start is None:
            self._report_dead_end("drone is outside the tile grid")
            return
        if goal is None:
            self._request_waypoint_skip("target waypoint is outside the tile grid")
            return
        if self._dangerous[goal[1], goal[0]]:
            self._request_waypoint_skip("target waypoint lies in a danger tile")
            return

        tiles = self._astar(start, goal)
        if tiles is None:
            self._report_dead_end(
                f"no 4-connected A* path from tile {start} to tile {goal}"
            )
            return

        # First pose = the drone's current position; then one pose per
        # tile centre (the start tile is skipped – the drone is already
        # at its spot).  z = target waypoint z everywhere.
        stamp = self.get_clock().now().to_msg()
        poses = []
        first = PoseStamped()
        first.header.stamp = stamp
        first.pose.position.x = sx
        first.pose.position.y = sy
        first.pose.position.z = gz
        poses.append(first)
        for ix, iy in tiles[1:]:
            pose = PoseStamped()
            pose.header.stamp = stamp
            pose.pose.position.x = (ix - self._half) * self._tile + self._tile / 2.0
            pose.pose.position.y = (iy - self._half) * self._tile + self._tile / 2.0
            pose.pose.position.z = gz
            poses.append(pose)
        self._publish_path(poses)
        self.get_logger().info(
            f"A* path published: {len(poses)} poses, {len(tiles) - 1} tiles, "
            f"goal NED ({gx:.1f}, {gy:.1f})"
        )

    def _astar(self, start, goal):
        """4-connected A* over the tile grid (vertical/horizontal moves
        only – no diagonals).  Returns the tile path including start and
        goal, or None when no path exists."""

        def heuristic(tile):
            return abs(tile[0] - goal[0]) + abs(tile[1] - goal[1])

        g_score = {start: 0.0}
        came_from = {}
        open_set = [(heuristic(start), 0, start)]
        closed = set()

        while open_set:
            _, g, cur = heapq.heappop(open_set)
            if cur in closed:
                continue
            if cur == goal:
                path = [cur]
                while cur in came_from:
                    cur = came_from[cur]
                    path.append(cur)
                path.reverse()
                return path
            closed.add(cur)

            for nxt in (
                (cur[0] + 1, cur[1]),
                (cur[0] - 1, cur[1]),
                (cur[0], cur[1] + 1),
                (cur[0], cur[1] - 1),
            ):
                if not (0 <= nxt[0] < self._n and 0 <= nxt[1] < self._n):
                    continue
                if self._dangerous[nxt[1], nxt[0]]:
                    continue
                if nxt in closed:
                    continue
                ng = g + 1.0
                if ng < g_score.get(nxt, math.inf):
                    g_score[nxt] = ng
                    came_from[nxt] = cur
                    heapq.heappush(open_set, (ng + heuristic(nxt), ng, nxt))
        return None

    # ==================================================================
    # Map visualisation (simple cv2 window)
    # ==================================================================

    def _map_cb(self):
        """Redraw the tile-map window (white = free, red = danger,
        green = safe path, X = drone)."""
        if not self._show_map:
            return
        img = self._draw_map()
        cv2.imshow("Inner Map", img)
        key = cv2.waitKey(1) & 0xFF
        # The X button destroys the window and the next imshow would
        # re-create it – detect that.  A freshly created window can
        # report "not visible" for a few frames while the window
        # manager maps it, so only honour the visibility check once
        # the window has been seen visible at least once (q/ESC always).
        visible = cv2.getWindowProperty("Inner Map", cv2.WND_PROP_VISIBLE)
        if visible >= 1.0:
            self._map_seen = True
        if key in (ord("q"), 27) or (self._map_seen and visible < 1.0):
            cv2.destroyWindow("Inner Map")
            self._show_map = False
            self.get_logger().info("Map window closed – show_map set to false")

    def _world_to_px(self, x: float, y: float):
        """World NED (North, East) -> pixel (column, row), North up."""
        s = self._map_scale
        row = (self._half - 0.5 - x / self._tile) * s
        col = (y / self._tile + self._half + 0.5) * s
        return int(round(col)), int(round(row))

    def _draw_map(self):
        """Render the grid into a BGR image (North up, East right)."""
        n, s = self._n, self._map_scale
        img = np.full((n * s, n * s, 3), 255, dtype=np.uint8)

        # danger tiles in red (tile ix = North axis = image rows)
        for iy, ix in zip(*np.nonzero(self._dangerous)):
            r0 = (n - 1 - ix) * s
            c0 = iy * s
            img[r0:r0 + s, c0:c0 + s] = (0, 0, 255)

        # faint grid lines + border
        for k in range(1, n):
            img[:, k * s - 1] = (225, 225, 225)
            img[k * s - 1, :] = (225, 225, 225)
        img[0, :] = img[-1, :] = img[:, 0] = img[:, -1] = (180, 180, 180)

        # safe path in green
        pts = [self._world_to_px(x, y) for x, y in self._path_xy]
        for (c1, r1), (c2, r2) in zip(pts, pts[1:]):
            cv2.line(img, (c1, r1), (c2, r2), (0, 200, 0), 2, cv2.LINE_AA)

        # drone as an X
        if self._pose_ned is not None:
            c, r = self._world_to_px(self._pose_ned[0], self._pose_ned[1])
            arm = max(2, int(round(1.2 * s)))
            cv2.line(img, (c - arm, r - arm), (c + arm, r + arm),
                     (0, 0, 0), 2, cv2.LINE_AA)
            cv2.line(img, (c - arm, r + arm), (c + arm, r - arm),
                     (0, 0, 0), 2, cv2.LINE_AA)
        return img

    # ==================================================================
    # Publishers / outputs
    # ==================================================================

    def _publish_path(self, poses):
        msg = Path()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"
        msg.poses = poses
        self._path_pub.publish(msg)
        # Keep the map window's green polyline in sync with the last
        # published path (also clears the polyline when poses is empty).
        self._path_xy = [
            (float(pose.pose.position.x), float(pose.pose.position.y))
            for pose in poses
        ]

    def _report_dead_end(self, reason: str):
        """No path exists – hand the problem to the Emergency Node."""
        self.get_logger().error(f"DEAD END – {reason}; requesting emergency")
        self._dead_end_pub.publish(Bool(data=True))

    def _request_waypoint_skip(self, reason: str):
        self.get_logger().warn(
            f"Skipping waypoint – {reason}"
        )
        self._skip_pub.publish(Bool(data=True))


    def destroy_node(self):
        if self._show_map:
            cv2.destroyAllWindows()
        super().destroy_node()


def main():
    rclpy.init()
    node = InnerMap()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
