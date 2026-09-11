#!/usr/bin/env python3
"""
detection_node.py – Obstacle detection from the Depth node's depth map.

Runs on the PC next to the depth node (loopback DDS).  Reads metric depth
maps and checks a "virtual bounding box" – the pixel footprint the drone's
own silhouette (+ margin) would have at the active threshold distance –
using the standard pinhole camera model.

Altitude-plane filter (the takeoff fix): every pixel's ray is projected
into the world-horizontal plane at the drone's CURRENT ALTITUDE (level
with the world, not with the drone's pitch/roll).  A pixel inside the
virtual box only counts when its measured 3D point lies within
plane_band_below_m .. plane_band_above_m of that plane.  The ground
always sits ~altitude below the plane, so it can never validate a
trigger.  Because the ground is AT the plane while the drone is still
standing on it, validation is additionally suppressed for
standby_suppress_sec after the drone leaves standby – that is what lets
the drone take off without the ground tripping ODA (a timer, not an
altitude gate, so the drone may fly low later).

The drone attitude for the plane projection comes from the MAVROS pose
quaternion: the plane itself is level in the WORLD, but the camera's
pitch/roll still determines where that plane appears in the image.

HUD: the node also subscribes to the depth node's colour-mapped preview
and republishes it with overlays – the active trigger box, the mission
registration band, and the altitude plane drawn as a fine grid.  An
optional live window (show_hud) turns it into a cockpit-style HUD.

Once an obstacle is validated (confirm_frames consecutive hits) it is
NEVER cleared while the drone stays in mission/oda state – validation is
one-way.  After a scout sweep ends the trigger is additionally kept
silent for post_sweep_cooldown_sec: the drone is normally still close
to the obstacle it just swept, and without the cooldown the fresh
re-sweep threshold would immediately re-arm the sweep instead of
letting GUIDED fly the path away.  On every frame the node also segments the near-threshold pixels
into obstacle "blocks" (see ObstacleBlock.msg): clusters separated by a
gap the drone could fly through become separate blocks, so two obstacles
side by side are reported individually with their own width and left edge
(already inflated by box_margin on both sides).

Subscribes:
  /depth_node/depth_map       – sensor_msgs/Image (32FC1, metric metres)
  /depth_node/depth_map_viz   – sensor_msgs/Image (bgr8, HUD base image)
  /drone_node/drone_state     – std_msgs/String  (selects the active threshold)
  /oda_maneuvers/sweeping     – std_msgs/Bool (True while a scout sweep runs)
  /mavros/local_position/pose – geometry_msgs/PoseStamped (attitude + altitude)
  /mavros/local_position/velocity_local – TwistStamped (speed for the HUD)

Publishes (private namespace → /detection_node/<name>):
  ~/obstacle_detected – std_msgs/Bool, True once an obstacle is validated
                        (never resets while flying).
  ~/obstacle_info     – sentinel_oda_msgs/ObstacleInfo (blocks[], plus
                        legacy scalar fields filled from the closest block).
  ~/hud_viz           – sensor_msgs/Image (bgr8): preview + trigger box,
                        registration band and altitude-plane grid overlays.
  ~/heartbeat         – std_msgs/Header (1 Hz) for the Emergency Node.

Thresholds:
  mission state:            mission_obstacle_threshold (default 10.0 m) –
                            triggers the switch into the ODA state.
  oda during a scout sweep: mission threshold again – the sweep registers
                            obstacles at distance (ODA Maneuvers publishes
                            /oda_maneuvers/sweeping = True).
  oda between sweeps:       oda_obstacle_threshold (default 0.80 m) –
                            obstacle very close: forces a new sweep.
obstacle_info registration ALWAYS uses the mission threshold ("the original
threshold registers obstacles at a distance") and is published whenever
blocks are actually seen, independent of the trigger latch.

IMPORTANT: the depth map must be METRIC (Depth Anything V2 Metric-Outdoor).
A relative depth map cannot be compared against metre thresholds.
"""

# possible culprits for why there are too many danger tiles:

# The unvalidation should not be through: danger_decay_timeout as it cancels the whole point of the memorized inner map that is supposed to remember where obstacles are. Forget the unvalidation for now.


# Turns out the biggest contributing factor to the smear is tile_safe_radius, reduce it and the smear is less exagerated.

# If all else fails, let's apply proven real world SLAM techniques

import math
from collections import deque
import time

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

import cv2
import numpy as np

from std_msgs.msg import Bool, Header, String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, TwistStamped
from cv_bridge import CvBridge

from sentinel_oda_msgs.msg import ObstacleBlock, ObstacleInfo


class DetectionNode(Node):
    """Obstacle detection – virtual bounding box + obstacle block segmentation."""

    def __init__(self):
        super().__init__("detection_node")

        # ---- parameters ----
        self.declare_parameter("mission_obstacle_threshold", 10.0)  # metres, mission state
        self.declare_parameter("oda_obstacle_threshold", 4.5)      # metres, oda state
        self.declare_parameter("depth_margin", 0.5)     # metres added to the threshold (model error)
        self.declare_parameter("drone_width", 0.363)    # metres
        self.declare_parameter("drone_height", 0.363)   # metres
        self.declare_parameter("box_margin", 0.2)       # metres, safety pad around the drone
        self.declare_parameter("camera_hfov_deg", 53.5) # horizontal FOV of the drone camera
        self.declare_parameter("confirm_frames", 5)    # consecutive hits to validate a danger tile
        self.declare_parameter("min_block_px", 3)       # ignore near-pixel components smaller than this
        self.declare_parameter("median_window", 5)      # frames for closest_distance median
        self.declare_parameter("plane_filter", True)       # only obstacles near the drone's altitude plane count
        self.declare_parameter("plane_band_below_m", 2.0)  # m below the plane still accepted
        self.declare_parameter("plane_band_above_m", 5.0)  # m above the plane still accepted
        self.declare_parameter("standby_suppress_sec", 10.0)  # seconds of suppressed validation after leaving standby (takeoff grace)
        self.declare_parameter("post_sweep_cooldown_sec", 10.0)  # seconds the trigger stays silent after a sweep ends (lets GUIDED fly away)
        self.declare_parameter("camera_pitch_offset_deg", 0.0)  # + = camera tilted down (HUD calibration)
        self.declare_parameter("camera_roll_offset_deg", 0.0)   # + = right side down (HUD calibration)
        self.declare_parameter("show_hud", False)      # pop-up HUD window (box + plane grid)
        self.declare_parameter("hud_rate", 15.0)       # Hz, HUD redraw / publish rate
        self.declare_parameter("heartbeat_rate", 1.0)   # Hz
        self.declare_parameter("pose_history_sec", 2.0)     # s of yaw history kept for depth-frame sync
        self.declare_parameter("depth_frame_lag_sec", 0.15) # s, frame content age vs its arrival stamp

        self._mission_thr = float(self.get_parameter("mission_obstacle_threshold").value)
        self._oda_thr = float(self.get_parameter("oda_obstacle_threshold").value)
        self._depth_margin = float(self.get_parameter("depth_margin").value)
        self._drone_w = float(self.get_parameter("drone_width").value)
        self._drone_h = float(self.get_parameter("drone_height").value)
        self._box_margin = float(self.get_parameter("box_margin").value)
        self._hfov = math.radians(float(self.get_parameter("camera_hfov_deg").value))
        self._confirm_n = max(1, int(self.get_parameter("confirm_frames").value))
        self._min_block_px = max(1, int(self.get_parameter("min_block_px").value))
        self._median_n = max(1, int(self.get_parameter("median_window").value))
        # A gap narrower than this cannot be flown through → the two sides
        # belong to the same obstacle block.
        self._passable_m = self._drone_w + 2.0 * self._box_margin
        heartbeat_rate = float(self.get_parameter("heartbeat_rate").value)
        self._plane_filter = bool(self.get_parameter("plane_filter").value)
        self._band_below = float(self.get_parameter("plane_band_below_m").value)
        self._band_above = float(self.get_parameter("plane_band_above_m").value)
        self._standby_suppress_sec = float(self.get_parameter("standby_suppress_sec").value)
        self._post_sweep_cooldown = max(0.0, float(self.get_parameter("post_sweep_cooldown_sec").value))
        self._pitch_off = float(self.get_parameter("camera_pitch_offset_deg").value)
        self._roll_off = float(self.get_parameter("camera_roll_offset_deg").value)
        self._show_hud = bool(self.get_parameter("show_hud").value)
        self._hud_seen = False  # window actually shown at least once (X-close detection)
        hud_rate = float(self.get_parameter("hud_rate").value)

        # ---- state ----
        self._bridge = CvBridge()
        self._drone_state = "standby"
        self._sweeping = False        # True while ODA Maneuvers runs a scout sweep
        self._yaw = None              # None until the first pose message arrives
        self._pose_hist = deque()     # (wall-clock seconds, yaw) – capture-time yaw lookup
        self._pose_hist_sec = float(self.get_parameter("pose_history_sec").value)
        self._depth_lag = float(self.get_parameter("depth_frame_lag_sec").value)
        self._standby_since = None      # time we left standby (post-standby grace timer)
        self._post_sweep_until = None   # trigger silenced until this time (ROS clock) after a sweep ends
        self._vel = None                # current speed (m/s) for the HUD
        self._obstacle = False        # validated trigger state (reset on state change)
        self._consecutive = 0         # consecutive hits (reset on a miss)
        self._dist_hist = deque(maxlen=self._median_n)

        # Attitude / altitude for the altitude-plane filter and HUD.
        self._qw = self._qx = self._qy = self._qz = None
        self._alt = None              # ENU altitude (m) from MAVROS local pose
        self._R_eff = None            # 3x3 camera→ENU rotation (attitude + mount offsets)
        self._cam = None              # {"w","h","fx","cx","cy"} of the last depth map
        self._ray_cache = None        # (key, B) per-pixel ray directions cache
        self._viz = None              # latest /depth_node/depth_map_viz (bgr8)
        self._hud = {}                # per-frame snapshot for the HUD overlay

        # ---- subscriptions (absolute paths: these topics belong to other nodes) ----
        self.create_subscription(Image, "/depth_node/depth_map", self._depth_cb, 10)
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)
        self.create_subscription(Bool, "/oda_maneuvers/sweeping", self._sweeping_cb, 10)
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )
        self.create_subscription(
            TwistStamped, "/mavros/local_position/velocity_local", self._vel_cb,
            qos_profile_sensor_data,
        )
        self.create_subscription(Image, "/depth_node/depth_map_viz", self._viz_cb, 10)

        # ---- publishers (private namespace → /detection_node/<name>) ----
        self._obstacle_pub = self.create_publisher(Bool, "~/obstacle_detected", 10)
        self._info_pub = self.create_publisher(ObstacleInfo, "~/obstacle_info", 10)
        self._heartbeat_pub = self.create_publisher(Header, "~/heartbeat", 10)
        self._hud_pub = self.create_publisher(Image, "~/hud_viz", 10)

        # ---- heartbeat ----
        self._heartbeat_timer = self.create_timer(1.0 / heartbeat_rate, self._heartbeat_cb)

        # ---- HUD (preview + trigger box + altitude-plane grid) ----
        self._hud_timer = self.create_timer(1.0 / max(1.0, hud_rate), self._hud_cb)

        self.get_logger().info(
            f"Detection node ready – mission threshold {self._mission_thr:.2f} m, "
            f"oda threshold {self._oda_thr:.2f} m (margin +{self._depth_margin:.2f} m), "
            f"validate after {self._confirm_n} consecutive frames, obstacles never cleared, "
            f"post-sweep cooldown {self._post_sweep_cooldown:.1f} s"
        )
        if self._plane_filter:
            self.get_logger().info(
                f"Altitude-plane filter ON: band [{-self._band_below:+.1f} .. "
                f"+{self._band_above:.1f}] m around the drone altitude, "
                f"{self._standby_suppress_sec:.1f} s grace after leaving standby"
            )

    # ==================================================================
    # Callbacks
    # ==================================================================

    def _state_cb(self, msg: String):
        if msg.data == self._drone_state:
            return
        if self._drone_state == "standby":
            # Leaving standby = takeoff: the ground is AT the altitude
            # plane then, so suppress validation for standby_suppress_sec
            # (timer, not altitude – low-altitude flight stays possible).
            self._standby_since = self.get_clock().now()
        self._drone_state = msg.data
        # Fresh state phase = fresh validation. Never carry a latched
        # obstacle across a state change (mission <-> oda), or the next
        # trigger could never produce a new rising edge. Drone Node
        # edge-detects on this topic, so a False here is harmless.
        self._reset_detection()
        self._post_sweep_until = None   # any state change cancels the post-sweep cooldown
        self._obstacle_pub.publish(Bool(data=False))

    def _sweeping_cb(self, msg: Bool):
        """ODA Maneuvers publishes True while a scout sweep is running."""
        prev = self._sweeping
        self._sweeping = msg.data
        if prev and not self._sweeping and self._drone_state == "oda":
            # Sweep finished: the 4.5 m re-sweep trigger takes over with a
            # clean slate, so a near obstacle yields a fresh rising edge.
            if self._obstacle:
                self._reset_detection()
                self._obstacle_pub.publish(Bool(data=False))
            # Post-sweep cooldown: the drone is usually still close to the
            # obstacle it just swept, so a fresh trigger would immediately
            # re-arm the sweep instead of letting GUIDED fly the path away.
            # Keep the trigger silent for post_sweep_cooldown_sec.
            if self._post_sweep_cooldown > 0.0:
                self._post_sweep_until = self.get_clock().now() + Duration(
                    seconds=self._post_sweep_cooldown
                )
                self.get_logger().info(
                    f"Sweep finished – trigger cooldown "
                    f"{self._post_sweep_cooldown:.1f} s"
                )

    def _pose_cb(self, msg: PoseStamped):
        q = msg.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self._yaw = math.atan2(siny, cosy)
        self._qw, self._qx, self._qy, self._qz = q.w, q.x, q.y, q.z
        self._alt = float(msg.pose.position.z)
        self._update_camera_rotation()
        # Wall-clock arrival time of this pose – key for the capture-time
        # yaw lookup (same clock domain as the depth-frame stamps).
        now = time.time()
        self._pose_hist.append((now, self._yaw))
        while self._pose_hist and self._pose_hist[0][0] < now - self._pose_hist_sec:
            self._pose_hist.popleft()

    def _yaw_at(self, t: float):
        """Heading (ENU rad) at wall-clock time t, linearly interpolated
        from the pose history (wrap-aware).  None when the history is too
        thin – the caller then falls back to the live yaw."""
        hist = self._pose_hist
        if len(hist) < 2:
            return None
        if t <= hist[0][0]:
            return hist[0][1]
        if t >= hist[-1][0]:
            return hist[-1][1]
        for i in range(len(hist) - 1, 0, -1):
            t0, y0 = hist[i - 1]
            t1, y1 = hist[i]
            if t0 <= t <= t1:
                dt = t1 - t0
                if dt <= 0.0:
                    return y1
                dy = (y1 - y0 + math.pi) % (2.0 * math.pi) - math.pi
                return y0 + dy * (t - t0) / dt
        return hist[-1][1]

    def _vel_cb(self, msg: TwistStamped):
        t = msg.twist.linear
        self._vel = math.sqrt(t.x * t.x + t.y * t.y + t.z * t.z)

    def _update_camera_rotation(self):
        """Recompute the camera→ENU rotation from attitude + mount offsets."""
        qw, qx, qy, qz = self._qw, self._qx, self._qy, self._qz
        R = np.array([
            [1.0 - 2.0 * (qy * qy + qz * qz), 2.0 * (qx * qy - qz * qw), 2.0 * (qx * qz + qy * qw)],
            [2.0 * (qx * qy + qz * qw), 1.0 - 2.0 * (qx * qx + qz * qz), 2.0 * (qy * qz - qx * qw)],
            [2.0 * (qx * qz - qy * qw), 2.0 * (qy * qz + qx * qw), 1.0 - 2.0 * (qx * qx + qy * qy)],
        ])
        po = math.radians(self._pitch_off)   # + = camera tilted down
        ro = math.radians(self._roll_off)    # + = right side down
        # ENU body axes: x fwd, y left, z up.  Camera down-tilt = +rotation
        # about y (fwd tilts toward −z); right side down = +rotation about x.
        R_pitch = np.array([
            [math.cos(po), 0.0, math.sin(po)],
            [0.0, 1.0, 0.0],
            [-math.sin(po), 0.0, math.cos(po)],
        ])
        R_roll = np.array([
            [1.0, 0.0, 0.0],
            [0.0, math.cos(ro), -math.sin(ro)],
            [0.0, math.sin(ro), math.cos(ro)],
        ])
        self._R_eff = R @ R_pitch @ R_roll

    def _depth_cb(self, msg: Image):
        """Process one depth map: run the virtual-box check and publish."""
        if self._drone_state not in ("mission", "oda"):
            # Not flying a mission – detection off (heartbeat keeps running).
            if self._obstacle:
                self._reset_detection()
                self._obstacle_pub.publish(Bool(data=False))
            return

        try:
            depth = self._bridge.imgmsg_to_cv2(msg, desired_encoding="32FC1")
        except Exception as e:
            self.get_logger().error(f"Bad depth map: {e}")
            return

        h, w = depth.shape[:2]

        # ---- trigger threshold ----
        # mission:                 mission threshold (10 m)
        # oda during a scout sweep: mission threshold again (registration)
        # oda between sweeps:       oda threshold (0.8 m, forces re-sweep)
        if self._drone_state == "oda":
            threshold = self._mission_thr if self._sweeping else self._oda_thr
        else:
            threshold = self._mission_thr
        trigger_dist = threshold - self._depth_margin

        # ---- obstacle_info registration: ALWAYS the mission threshold --
        reg_dist = self._mission_thr - self._depth_margin

        # Pinhole model: each box is the drone silhouette (+ margin) as it
        # would appear at that box's threshold distance.
        focal_px = (w / 2.0) / math.tan(self._hfov / 2.0)
        self._cam = {"w": w, "h": h, "fx": focal_px, "cx": w // 2, "cy": h // 2}
        box_w_px = max(1, int((self._drone_w + self._box_margin) * focal_px / threshold))
        box_h_px = max(1, int((self._drone_h + self._box_margin) * focal_px / threshold))
        reg_w_px = max(1, int((self._drone_w + self._box_margin) * focal_px / self._mission_thr))
        reg_h_px = max(1, int((self._drone_h + self._box_margin) * focal_px / self._mission_thr))

        cx, cy = w // 2, h // 2
        # Align the box with the drone's altitude plane: shift its
        # vertical centre to the row where the plane crosses the image
        # centre column, so the box sits between the two plane band
        # lines in the HUD.
        if self._plane_filter and self._R_eff is not None and abs(self._R_eff[2, 2]) > 1e-6:
            cy = cy + focal_px * (self._R_eff[2, 0] / self._R_eff[2, 2])
            cy = max(0, min(h - 1, int(round(cy))))
        x0 = max(0, min(w, cx - box_w_px // 2))
        x1 = max(0, min(w, cx + box_w_px // 2))
        y0 = max(0, min(h, cy - box_h_px // 2))
        y1 = max(0, min(h, cy + box_h_px // 2))
        reg_y0 = max(0, min(h, cy - reg_h_px // 2))
        reg_y1 = max(0, min(h, cy + reg_h_px // 2))
        if x1 <= x0 or y1 <= y0:
            return  # box collapsed outside the image – nothing to check

        # ---- trigger check: anything near inside the virtual box ----
        region = depth[y0:y1, x0:x1]
        valid = np.isfinite(region) & (region > 0.0)
        near = valid & (region < trigger_dist)

        # ---- altitude-plane filter -------------
        # Every pixel's ray is projected into the world-horizontal plane
        # at the drone's current altitude.  A box pixel only validates the
        # trigger if its measured 3D point sits within [below .. above] of
        # that plane.  The ground is always ~altitude below the plane, so
        # it can never validate.  While the drone is still taking off the
        # ground is practically AT the plane, so validation is suppressed
        # for standby_suppress_sec after it leaves standby (timer, not an
        # altitude gate).
        suppress_reason = None
        if self._plane_filter:
            if self._R_eff is None:
                suppress_reason = "no attitude from MAVROS yet"
            elif self._alt is None:
                suppress_reason = "no altitude from MAVROS yet"
            elif self._standby_since is not None:
                left = self._standby_suppress_sec - (
                    self.get_clock().now() - self._standby_since
                ).nanoseconds * 1e-9
                if left > 0.0:
                    suppress_reason = f"post-standby grace, {left:.1f} s left"
                else:
                    self._standby_since = None
            if suppress_reason is None:
                alt_rel = region * self._up_map(w, h, focal_px)[y0:y1, x0:x1]
                near &= (alt_rel >= -self._band_below) & (alt_rel <= self._band_above)
        if suppress_reason is not None:
            near = np.zeros_like(near)
            self.get_logger().info(
                f"plane filter: trigger suppressed ({suppress_reason})"
            )

        found = bool(np.any(near))

        # Post-sweep cooldown: right after a scout sweep the drone is
        # still close to the obstacle it just swept – keep the trigger
        # silent for post_sweep_cooldown_sec so GUIDED gets to fly the
        # path away instead of ODA Maneuvers re-arming the sweep.
        if self._post_sweep_until is not None:
            if self.get_clock().now() < self._post_sweep_until:
                found = False
            else:
                self._post_sweep_until = None

        # Diagnostic for threshold tuning: closest valid depth inside the
        # virtual box vs the current trigger distance, plus how many box
        # pixels pass the altitude-plane filter.
        box_depths = region[valid]
        closest_box = float(np.min(box_depths)) if box_depths.size else None
        if box_depths.size:
            self.get_logger().info(
                f"virtual box: closest depth = {closest_box:.2f} m "
                f"(triggers below {trigger_dist:.1f} m, "
                f"plane-valid px = {int(np.count_nonzero(near))})"
            )

        # HUD snapshot for the overlay timer.
        self._hud = {
            "state": self._drone_state,
            "sweeping": self._sweeping,
            "threshold": threshold,
            "trigger_dist": trigger_dist,
            "box": (x0, y0, x1, y1),
            "reg_band": (reg_y0, reg_y1),
            "closest": closest_box,
            "alt": self._alt,
            "speed": self._vel,
            "band": (self._band_below, self._band_above),
            "obstacle": self._obstacle,
            "consecutive": self._consecutive,
            "blocks": 0,
        }

        # ---- validation: N consecutive hits, one-way (never cleared) ----
        if found:
            self._consecutive = min(self._confirm_n, self._consecutive + 1)
            self._dist_hist.append(float(np.min(region[valid])))
            if not self._obstacle and self._consecutive >= self._confirm_n:
                self._obstacle = True
                self.get_logger().info(
                    "obstacle_detected = True (latched until state change or sweep end)"
                )
        else:
            # A miss only breaks the run of consecutive hits; it never
            # clears an already-validated obstacle.
            self._consecutive = 0

        self._obstacle_pub.publish(Bool(data=self._obstacle))

        # ---- obstacle_info: published only while the obstacle is
        #      confirmed (same time as obstacle_detected). ----
        blocks = self._extract_blocks(depth, reg_y0, reg_y1, reg_dist, cx, focal_px)
        self._hud["blocks"] = len(blocks)
        if not blocks or not self._obstacle:
            return
        info = ObstacleInfo()
        info.closest_distance = blocks[0].distance  # blocks sorted by distance
        # Heading at DEPTH-FRAME CAPTURE time, not the live yaw: the frame
        # is 0.1-0.4 s old, and during the ODA yaw sweep a stale heading
        # paints the blocks at wrong bearings (the danger-tile smear).
        cap_t = (
            float(msg.header.stamp.sec)
            + float(msg.header.stamp.nanosec) * 1e-9
            - self._depth_lag
        )
        yaw_sync = self._yaw_at(cap_t)
        info.current_heading = (
            yaw_sync if yaw_sync is not None
            else (self._yaw if self._yaw is not None else 0.0)
        )
        # Legacy single-obstacle fields mirror the closest block.
        info.obstacle_width = blocks[0].width
        info.obstacle_left = blocks[0].left
        info.blocks = blocks
        self._info_pub.publish(info)

    def _extract_blocks(self, depth, y0, y1, trigger_dist, cx, focal_px):
        """
        Cluster near-threshold pixels into obstacle blocks.

        Runs on the virtual box's row band (y0:y1) but across the FULL
        image width, so an obstacle wider than the box is measured
        completely.  Connected components of near pixels are merged
        left-to-right while the gap between them is narrower than the
        drone's passable width (drone_width + 2*box_margin, evaluated at
        the gap's own depth) – i.e. a gap the drone could fly through
        splits the obstacle into separate blocks, while small noise gaps
        inside one obstacle are re-merged.

        Widths/lefts are inflated by box_margin on both sides so consumers
        can mark tiles directly.
        """
        band = depth[y0:y1, :]
        valid = np.isfinite(band) & (band > 0.0)
        near = valid & (band < trigger_dist)
        if not np.any(near):
            return []

        n_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
            near.astype(np.uint8), connectivity=8
        )

        # (x_start, x_end, closest_distance) per component, image columns.
        comps = []
        for lab in range(1, n_labels):
            x, _y, wpx, _hpx, area = stats[lab]
            if area < self._min_block_px:
                continue
            dist = float(np.min(band[labels == lab]))
            comps.append([x, x + wpx - 1, dist])

        if not comps:
            return []
        comps.sort(key=lambda c: c[0])

        # Greedy left-to-right merge across impassable gaps.
        merged = []
        cur = comps[0]
        for nxt in comps[1:]:
            gap_px = nxt[0] - cur[1] - 1
            if gap_px > 0:
                gap_depth = band[:, cur[1] + 1:nxt[0]]
                gv = gap_depth[np.isfinite(gap_depth) & (gap_depth > 0.0)]
                if gv.size:
                    d_gap = float(np.median(gv))
                else:
                    # No valid depth in the gap – judge it at the nearer
                    # obstacle's distance (conservative → merge).
                    d_gap = min(cur[2], nxt[2])
                gap_m = gap_px * d_gap / focal_px
                if gap_m >= self._passable_m:
                    merged.append(cur)
                    cur = nxt
                    continue
            # Touching columns or impassable gap → same obstacle.
            cur[1] = max(cur[1], nxt[1])
            cur[2] = min(cur[2], nxt[2])
        merged.append(cur)

        # Build margin-inflated ObstacleBlock messages.
        blocks = []
        for x_start, x_end, dist in merged:
            d_left = self._edge_depth(band, x_start, trigger_dist, dist)
            d_right = self._edge_depth(band, x_end, trigger_dist, dist)
            left_m = (x_start - cx) * d_left / focal_px
            right_m = (x_end - cx) * d_right / focal_px
            raw_width = right_m - left_m

            block = ObstacleBlock()
            block.distance = dist
            block.width = raw_width 
            block.left = left_m - self._box_margin
            blocks.append(block)

        blocks.sort(key=lambda b: b.distance)
        return blocks

    @staticmethod
    def _edge_depth(band, col, trigger_dist, fallback):
        """Median depth of the near pixels in one column of the band."""
        col_vals = band[:, col]
        near_vals = col_vals[
            np.isfinite(col_vals) & (col_vals > 0.0) & (col_vals < trigger_dist)
        ]
        return float(np.median(near_vals)) if near_vals.size else float(fallback)

    # ==================================================================
    # Altitude-plane projection + HUD overlay
    # ==================================================================

    def _body_dirs(self, w, h, fx):
        """Unit camera ray directions per pixel, in ENU body axes (fwd, left, up).

        MAVROS /mavros/local_position/pose carries an ENU quaternion, so the
        camera ray must be expressed the same way: camera X (right) → body
        −y (left), camera Y (down) → body −z (up), camera Z (forward) → +x.
        """
        key = (w, h, round(fx, 1))
        if self._ray_cache is not None and self._ray_cache[0] == key:
            return self._ray_cache[1]
        cx, cy = w // 2, h // 2
        u = (np.arange(w, dtype=np.float32) - cx) / fx
        v = (np.arange(h, dtype=np.float32) - cy) / fx
        uu, vv = np.meshgrid(u, v)
        n = np.sqrt(1.0 + uu * uu + vv * vv)
        B = np.stack([1.0 / n, -uu / n, -vv / n])  # fwd, left, up
        self._ray_cache = (key, B)
        return B

    def _up_map(self, w, h, fx):
        """ENU up-component of every pixel's unit ray (+ = above the drone plane)."""
        B = self._body_dirs(w, h, fx).reshape(3, -1)
        return (self._R_eff @ B)[2].reshape(h, w)

    def _viz_cb(self, msg: Image):
        """Keep the latest colour-mapped depth preview for the HUD."""
        try:
            self._viz = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception:
            self._viz = None

    def _hud_cb(self):
        """Redraw + publish the HUD: preview, trigger box, plane grid, text."""
        if self._viz is None:
            return
        img = self._viz.copy()
        self._draw_hud(img)
        hud_msg = self._bridge.cv2_to_imgmsg(img, encoding="bgr8")
        hud_msg.header.stamp = self.get_clock().now().to_msg()
        hud_msg.header.frame_id = "depth_camera"
        self._hud_pub.publish(hud_msg)
        if self._show_hud:
            cv2.imshow("Detection HUD", img)
            key = cv2.waitKey(1) & 0xFF
            # The X button destroys the window and the next imshow would
            # re-create it – detect that.  A freshly created window can
            # report "not visible" for a few frames while the window
            # manager maps it, so only honour the visibility check once
            # the window has been seen visible at least once (q/ESC always).
            visible = cv2.getWindowProperty("Detection HUD", cv2.WND_PROP_VISIBLE)
            if visible >= 1.0:
                self._hud_seen = True
            if key in (ord("q"), 27) or (self._hud_seen and visible < 1.0):
                cv2.destroyWindow("Detection HUD")
                self._show_hud = False
                self.get_logger().info(
                    "HUD window closed – show_hud set to false"
                )

    def _draw_hud(self, img):
        hud = self._hud
        if hud.get("box"):
            x0, y0, x1, y1 = hud["box"]
            cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 1, cv2.LINE_AA)
            ry0, ry1 = hud["reg_band"]
            self._dashed_h_line(img, ry0, (255, 255, 0))
            self._dashed_h_line(img, ry1, (255, 255, 0))
        self._draw_plane_grid(img)
        self._draw_hud_text(img)

    def _draw_plane_grid(self, img):
        """Draw the drone's altitude plane as a fine perspective grid."""
        R = self._R_eff
        if R is None or not self._cam:
            return
        fx, cx, cy = self._cam["fx"], self._cam["cx"], self._cam["cy"]
        fwd = R @ np.array([1.0, 0.0, 0.0])
        lat = R @ np.array([0.0, 1.0, 0.0])  # ENU body y = left; grid is symmetric
        fwd[2] = 0.0
        lat[2] = 0.0
        nf, nr = float(np.linalg.norm(fwd)), float(np.linalg.norm(lat))
        if nf < 1e-3 or nr < 1e-3:
            return
        fwd /= nf
        lat /= nr
        Rt = R.T

        def project(pt):
            # pt is ENU; R maps camera→ENU, so body = Rᵀ·pt is in ENU
            # BODY axes (x fwd, y left, z up).  Convert to camera axes
            # (x right, y down, z forward) before the pinhole projection.
            b = Rt @ pt
            cam_z = b[0]
            if cam_z < 0.2:
                return None
            cam_x = -b[1]
            cam_y = -b[2]
            return (int(round(fx * cam_x / cam_z + cx)), int(round(fx * cam_y / cam_z + cy)))

        # Altitude offsets (ENU z, up positive): plane itself, band below
        # (negative), band above (positive).
        half = 8.0
        for hh in (0.0, -self._band_below, self._band_above):
            on_plane = abs(hh) < 1e-6
            colour = (0, 220, 220) if on_plane else (220, 220, 220)
            # lateral lines: constant lateral offset, depth from 0.8 to 100 m
            for s in np.arange(-half, half + 1e-6, 2.0):
                p1 = project(fwd * 0.8 + lat * float(s) + np.array([0.0, 0.0, hh]))
                p2 = project(fwd * 100.0 + lat * float(s) + np.array([0.0, 0.0, hh]))
                if p1 is not None and p2 is not None:
                    self._draw_line(img, p1, p2, colour, dashed=not on_plane)
            # depth lines: constant depth, lateral offset from −half to +half
            for t in (2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 30.0, 50.0):
                p1 = project(fwd * t - lat * half + np.array([0.0, 0.0, hh]))
                p2 = project(fwd * t + lat * half + np.array([0.0, 0.0, hh]))
                if p1 is not None and p2 is not None:
                    self._draw_line(img, p1, p2, colour, dashed=not on_plane)

    @staticmethod
    def _draw_line(img, p1, p2, colour, dashed=False):
        if not dashed:
            cv2.line(img, p1, p2, colour, 1, cv2.LINE_AA)
            return
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 1.0:
            return
        steps = max(1, int(dist // 6.0))
        for i in range(0, steps, 2):
            a, b = i / steps, min(1.0, (i + 0.5) / steps)
            cv2.line(
                img,
                (int(round(x1 + a * dx)), int(round(y1 + a * dy))),
                (int(round(x1 + b * dx)), int(round(y1 + b * dy))),
                colour, 1, cv2.LINE_AA,
            )

    @staticmethod
    def _dashed_h_line(img, y, colour):
        y = int(round(y))
        if y < 0 or y >= img.shape[0]:
            return
        for x in range(0, img.shape[1], 12):
            cv2.line(img, (x, y), (min(img.shape[1] - 1, x + 6), y), colour, 1, cv2.LINE_AA)

    def _draw_hud_text(self, img):
        hud = self._hud
        if not hud:
            return
        sweep = " (sweeping)" if hud["sweeping"] else ""
        lines = [
            f"state={hud['state']}{sweep}",
            f"trigger < {hud['trigger_dist']:.1f} m  (thr {hud['threshold']:.1f} + {self._depth_margin:.1f})",
        ]
        if hud["alt"] is not None:
            lines.append(
                f"alt {hud['alt']:.1f} m  plane band [{-hud['band'][0]:+.1f} .. +{hud['band'][1]:.1f}] m"
            )
        if hud.get("speed") is not None:
            lines.append(f"speed {hud['speed']:.1f} m/s")
        if hud["closest"] is not None:
            lines.append(f"box closest {hud['closest']:.2f} m")
        lines.append(
            f"obstacle={hud['obstacle']} ({hud['consecutive']}/{self._confirm_n})  blocks={hud['blocks']}"
        )
        y = 16
        for text in lines:
            cv2.putText(img, text, (4, y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, text, (4, y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 1, cv2.LINE_AA)
            y += 15

    def _reset_detection(self):
        self._obstacle = False
        self._consecutive = 0
        self._dist_hist.clear()

    def _heartbeat_cb(self):
        """Publish a heartbeat for the Emergency Node."""
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = "detection_node"
        self._heartbeat_pub.publish(msg)

    def destroy_node(self):
        if self._show_hud:
            cv2.destroyAllWindows()
        super().destroy_node()


def main():
    rclpy.init()
    node = DetectionNode()
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
