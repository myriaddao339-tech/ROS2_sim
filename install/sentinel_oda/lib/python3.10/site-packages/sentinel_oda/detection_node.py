#!/usr/bin/env python3
"""
detection_node.py – Obstacle detection from the Depth node's depth map.

Runs on the PC next to the depth node (loopback DDS).  Reads metric depth
maps and checks a "virtual bounding box" – the pixel footprint the drone's
own silhouette (+ margin) would have at the active threshold distance –
using the standard pinhole camera model.

Once an obstacle is validated (confirm_frames consecutive hits) it is
NEVER cleared while the drone stays in mission/oda state – validation is
one-way.  On every frame the node also segments the near-threshold pixels
into obstacle "blocks" (see ObstacleBlock.msg): clusters separated by a
gap the drone could fly through become separate blocks, so two obstacles
side by side are reported individually with their own width and left edge
(already inflated by box_margin on both sides).

Subscribes:
  /depth_node/depth_map       – sensor_msgs/Image (32FC1, metric metres)
  /drone_node/drone_state     – std_msgs/String  (selects the active threshold)
  /mavros/local_position/pose – geometry_msgs/PoseStamped (drone yaw)

Publishes (private namespace → /detection_node/<name>):
  ~/obstacle_detected – std_msgs/Bool, True once an obstacle is validated
                        (never resets while flying).
  ~/obstacle_info     – sentinel_oda_msgs/ObstacleInfo (blocks[], plus
                        legacy scalar fields filled from the closest block).
  ~/heartbeat         – std_msgs/Header (1 Hz) for the Emergency Node.

Two thresholds, switched by drone_state:
  mission state: mission_obstacle_threshold (default 10.0 m) – registers
                 obstacles ahead; this is the trigger that sends the drone
                 into the ODA state.
  oda state:     oda_obstacle_threshold     (default 0.80 m) – obstacle
                 very close: forces ODA Maneuvers to stop and sweep again.

IMPORTANT: the depth map must be METRIC (Depth Anything V2 Metric-Outdoor).
A relative depth map cannot be compared against metre thresholds.
"""

import math
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

import cv2
import numpy as np

from std_msgs.msg import Bool, Header, String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge

from sentinel_oda_msgs.msg import ObstacleBlock, ObstacleInfo


class DetectionNode(Node):
    """Obstacle detection – virtual bounding box + obstacle block segmentation."""

    def __init__(self):
        super().__init__("detection_node")

        # ---- parameters ----
        self.declare_parameter("mission_obstacle_threshold", 10.0)  # metres, mission state
        self.declare_parameter("oda_obstacle_threshold", 0.80)      # metres, oda state
        self.declare_parameter("depth_margin", 0.5)     # metres added to the threshold (model error)
        self.declare_parameter("drone_width", 0.363)    # metres
        self.declare_parameter("drone_height", 0.363)   # metres
        self.declare_parameter("box_margin", 0.2)       # metres, safety pad around the drone
        self.declare_parameter("camera_hfov_deg", 53.5) # horizontal FOV of the drone camera
        self.declare_parameter("confirm_frames", 10)    # consecutive hits to validate a danger tile
        self.declare_parameter("min_block_px", 3)       # ignore near-pixel components smaller than this
        self.declare_parameter("median_window", 5)      # frames for closest_distance median
        self.declare_parameter("heartbeat_rate", 1.0)   # Hz

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

        # ---- state ----
        self._bridge = CvBridge()
        self._drone_state = "standby"
        self._yaw = None              # None until the first pose message arrives
        self._obstacle = False        # validated output state – never cleared while flying
        self._consecutive = 0         # consecutive hits (reset on a miss)
        self._dist_hist = deque(maxlen=self._median_n)

        # ---- subscriptions (absolute paths: these topics belong to other nodes) ----
        self.create_subscription(Image, "/depth_node/depth_map", self._depth_cb, 10)
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )

        # ---- publishers (private namespace → /detection_node/<name>) ----
        self._obstacle_pub = self.create_publisher(Bool, "~/obstacle_detected", 10)
        self._info_pub = self.create_publisher(ObstacleInfo, "~/obstacle_info", 10)
        self._heartbeat_pub = self.create_publisher(Header, "~/heartbeat", 10)

        # ---- heartbeat ----
        self._heartbeat_timer = self.create_timer(1.0 / heartbeat_rate, self._heartbeat_cb)

        self.get_logger().info(
            f"Detection node ready – mission threshold {self._mission_thr:.2f} m, "
            f"oda threshold {self._oda_thr:.2f} m (margin +{self._depth_margin:.2f} m), "
            f"validate after {self._confirm_n} consecutive frames, obstacles never cleared"
        )

    # ==================================================================
    # Callbacks
    # ==================================================================

    def _state_cb(self, msg: String):
        self._drone_state = msg.data

    def _pose_cb(self, msg: PoseStamped):
        q = msg.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self._yaw = math.atan2(siny, cosy)

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
            self.get_logger().error(f"Bad depth map: {e}", throttle_duration_sec=5.0)
            return

        h, w = depth.shape[:2]
        threshold = self._oda_thr if self._drone_state == "oda" else self._mission_thr
        trigger_dist = threshold + self._depth_margin

        # Pinhole model: the box is the drone silhouette (+ margin) as it
        # would appear at the active threshold distance.
        focal_px = (w / 2.0) / math.tan(self._hfov / 2.0)
        box_w_px = max(1, int((self._drone_w + self._box_margin) * focal_px / threshold))
        box_h_px = max(1, int((self._drone_h + self._box_margin) * focal_px / threshold))

        cx, cy = w // 2, h // 2
        x0 = max(0, min(w, cx - box_w_px // 2))
        x1 = max(0, min(w, cx + box_w_px // 2))
        y0 = max(0, min(h, cy - box_h_px // 2))
        y1 = max(0, min(h, cy + box_h_px // 2))
        if x1 <= x0 or y1 <= y0:
            return  # box collapsed outside the image – nothing to check

        # ---- trigger check: anything near inside the virtual box ----
        region = depth[y0:y1, x0:x1]
        valid = np.isfinite(region) & (region > 0.0)
        near = valid & (region < trigger_dist)
        found = bool(np.any(near))

        # ---- validation: N consecutive hits, one-way (never cleared) ----
        if found:
            self._consecutive = min(self._confirm_n, self._consecutive + 1)
            self._dist_hist.append(float(np.min(region[valid])))
            if not self._obstacle and self._consecutive >= self._confirm_n:
                self._obstacle = True
                self.get_logger().info("obstacle_detected = True (locked until state change)")
        else:
            # A miss only breaks the run of consecutive hits; it never
            # clears an already-validated obstacle.
            self._consecutive = 0

        self._obstacle_pub.publish(Bool(data=self._obstacle))

        # ---- obstacle_info (published on every frame while validated) ----
        if not self._obstacle:
            return

        blocks = self._extract_blocks(depth, y0, y1, trigger_dist, cx, focal_px)
        info = ObstacleInfo()
        if self._dist_hist:
            info.closest_distance = float(np.median(self._dist_hist))
        info.current_heading = self._yaw if self._yaw is not None else 0.0
        # Legacy single-obstacle fields mirror the closest block.
        info.obstacle_width = blocks[0].width if blocks else 0.0
        info.obstacle_left = blocks[0].left if blocks else 0.0
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
            block.width = raw_width + 2.0 * self._box_margin
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
