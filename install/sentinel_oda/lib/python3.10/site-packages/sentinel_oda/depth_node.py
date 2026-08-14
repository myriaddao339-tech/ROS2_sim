#!/usr/bin/env python3
"""
depth_node.py – Monocular depth estimation using Depth Anything V2 (light).

Reads frames from the drone's UDP MPEG‑TS stream (default 127.0.0.1:5600),
or from the PC webcam / a video file, and runs the small Depth Anything V2
Metric-Outdoor checkpoint on the CPU (default) or GPU.

Publishes:
  /depth_node/depth_map     – sensor_msgs/Image  (32FC1, metric metres)
  /depth_node/depth_map_viz – sensor_msgs/Image  (rgb8,  colour-mapped for rviz2)
  /depth_node/heartbeat     – std_msgs/Header     (1 Hz, for Emergency Node)

The inference timer fires at a configurable rate (default 20 Hz); the
camera may be pushing frames faster – stale frames are dropped by
reading the latest available buffer before each inference pass.

NOTE: the timer is not the real limit – effective fps = 1/inference-time.
The stale-frame drain is time-bounded (drain_budget), so it can never
drag the fps below the model's own speed.  On this machine's CPU the
Small checkpoint measures ~1.2 fps @ 518px, ~5.6 fps @ 308px, ~8.0 fps
@ 224px (input size set via model_input_size).  True 20 Hz needs the GPU.

NOTE: this node runs the Metric-Outdoor checkpoint, so the published
depth map is in real metres – which the Detection node needs for its
metre-based thresholds.
"""

import os
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np
import torch


# ---------------------------------------------------------------------------
# Depth Anything V2 model wrapper
# ---------------------------------------------------------------------------

class DepthAnythingV2Model:
    """
    Thin wrapper around depth-anything/Depth-Anything-V2-* models via the
    HuggingFace transformers depth-estimation pipeline.
    """

    def __init__(self, model_name: str = "depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf",
                 device: str = "cpu",
                 input_size: int = 308,
                 cpu_threads: int = 0):
        self._device = self._resolve_device(device)
        self._model_name = model_name
        self._input_size = input_size
        self._cpu_threads = max(0, int(cpu_threads))
        self._n_threads = 0
        self._loaded = False

    # -- device resolution --
    @staticmethod
    def _resolve_device(device: str) -> str:
        if device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return device

    # -- loading --
    def load(self):
        """Import & load the model.  Call once during node startup."""
        from transformers import pipeline  # noqa: E402

        # pipeline device: -1 = CPU, 0 = cuda:0
        pipe_device = 0 if self._device.startswith("cuda") else -1

        # Cap PyTorch's CPU thread pool so inference leaves cores free for
        # MAVROS/Gazebo/SITL when they share the machine (GPU runs are
        # unaffected).  Portable across machines: cpu_threads=0 means
        # "auto" (all cores minus two, minimum one); set N for a fixed pool.
        if not self._device.startswith("cuda"):
            n_cores = os.cpu_count() or 2
            self._n_threads = self._cpu_threads if self._cpu_threads > 0 else max(1, n_cores - 2)
            torch.set_num_threads(self._n_threads)
        else:
            self._n_threads = 0

        self._pipe = pipeline(
            task="depth-estimation",
            model=self._model_name,
            device=pipe_device,
        )
        # Override the preprocessor's model input size.  The ViT encoder
        # cost grows with the square of the token count, so smaller inputs
        # are dramatically faster on CPU (detail vs fps trade-off).
        self._pipe.image_processor.size = {
            "height": self._input_size,
            "width": self._input_size,
        }
        self._loaded = True

    @property
    def device(self) -> str:
        """Device the model is actually running on (resolved from 'auto')."""
        return self._device

    @property
    def cpu_threads(self) -> int:
        """PyTorch CPU thread-pool size in effect (0 = not on CPU)."""
        return self._n_threads

    # -- inference --
    def infer(self, rgb: np.ndarray) -> np.ndarray:
        """
        Run depth estimation on an RGB numpy image (H×W×3, uint8).

        Returns a float32 numpy array (H×W) with metric depth values in
        metres (the Metric-Outdoor checkpoint).
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded – call .load() first")

        # The pipeline handles preprocessing; 'depth' is the prediction
        # resized back to the original input resolution.  transformers
        # load_image() rejects raw numpy arrays, so pass a PIL image.
        from PIL import Image  # noqa: E402

        pil_img = Image.fromarray(rgb)
        result = self._pipe(pil_img)
        # Prefer the float tensor; some transformers versions expose the
        # post-processed map as a PIL image under 'depth' instead.
        depth_t = result.get("predicted_depth", result.get("depth"))
        if depth_t is None:
            raise RuntimeError("Depth pipeline returned no depth map")
        if isinstance(depth_t, torch.Tensor):
            return depth_t.cpu().numpy().astype(np.float32)
        return np.asarray(depth_t, dtype=np.float32)


# ---------------------------------------------------------------------------
# Colour‑map helper
# ---------------------------------------------------------------------------

def _depth_to_colormap(depth: np.ndarray, vmin: float = 0.0, vmax: float = 50.0) -> np.ndarray:
    """
    Convert a float32 depth map to an 8‑bit colour image suitable for rviz2.

    Uses OpenCV's TURBO colormap.  Values <= vmin are black; values >= vmax
    saturate to the top of the colour scale.
    """
    clipped = np.clip(depth, vmin, vmax)
    normalized = ((clipped - vmin) / (vmax - vmin) * 255.0).astype(np.uint8)
    coloured = cv2.applyColorMap(normalized, cv2.COLORMAP_TURBO)
    return coloured


# ---------------------------------------------------------------------------
# ROS 2 Node
# ---------------------------------------------------------------------------

class DepthNode(Node):
    """Depth estimation node – reads video, runs Depth Anything V2, publishes maps."""

    def __init__(self):
        super().__init__("depth_node")

        # ---- parameters ----
        self.declare_parameter("udp_port", 5600)
        self.declare_parameter("video_source", "udp")  # "udp" (drone relay) | "webcam" | any URI/path
        self.declare_parameter("webcam_width", 640)       # capture resolution (webcam only)
        self.declare_parameter("webcam_height", 480)
        self.declare_parameter("webcam_fps", 30)          # requested capture fps (webcam only)
        self.declare_parameter("show_preview", False)     # pop-up OpenCV window
        self.declare_parameter("inference_rate", 20.0)    # Hz target (timer cap; effective fps limited by model speed on CPU)
        self.declare_parameter("drain_budget", 0.1)       # s, max time spent draining stale frames per pass
        self.declare_parameter("heartbeat_rate", 1.0)     # Hz
        self.declare_parameter("model_name", "depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf")
        self.declare_parameter("device", "cpu")           # "cuda", "cpu", "auto"
        self.declare_parameter("cpu_threads", 0)          # PyTorch CPU thread pool: 0 = auto (cores-2), N = fixed
        self.declare_parameter("model_input_size", 308)   # 224|308|448|518 – smaller = faster on CPU
        self.declare_parameter("relative_depth", False)   # metric model – fixed colormap (vmin/vmax)
        self.declare_parameter("color_map_vmin", 0.0)     # used only when relative_depth=false
        self.declare_parameter("color_map_vmax", 50.0)
        self.declare_parameter("frame_id", "depth_camera")

        udp_port = self.get_parameter("udp_port").value
        video_source = self.get_parameter("video_source").value
        webcam_width = self.get_parameter("webcam_width").value
        webcam_height = self.get_parameter("webcam_height").value
        webcam_fps = self.get_parameter("webcam_fps").value
        self._is_webcam = video_source == "webcam"
        self._show_preview = self.get_parameter("show_preview").value
        inference_rate = self.get_parameter("inference_rate").value
        self._drain_budget = float(self.get_parameter("drain_budget").value)
        heartbeat_rate = self.get_parameter("heartbeat_rate").value
        model_name = self.get_parameter("model_name").value
        device = self.get_parameter("device").value
        cpu_threads = self.get_parameter("cpu_threads").value
        model_input_size = self.get_parameter("model_input_size").value
        self._relative_depth = self.get_parameter("relative_depth").value
        self._cmap_vmin = self.get_parameter("color_map_vmin").value
        self._cmap_vmax = self.get_parameter("color_map_vmax").value
        self._frame_id = self.get_parameter("frame_id").value

        # ---- OpenCV video capture ----
        # video_source: "udp" (default, MPEG‑TS on localhost), "webcam"
        # (camera index 0), or any other URI / device path / video file.
        # FFmpeg udp protocol options:
        #   fifo_size         – bigger receive buffer, fewer packet drops
        #   overrun_nonfatal  – survive a fifo overrun instead of aborting
        #   timeout           – µs read timeout, so grab() never blocks forever
        if video_source == "udp":
            stream_uri = f"udp://127.0.0.1:{udp_port}?fifo_size=5000000&overrun_nonfatal=1&timeout=500000"
            self._cap = cv2.VideoCapture(stream_uri)
        elif video_source == "webcam":
            # NOTE: integer index, not the string "0" – OpenCV's GStreamer
            # backend would otherwise parse the string as a pipeline spec.
            stream_uri = f"webcam index 0 @ {webcam_width}x{webcam_height} ({webcam_fps} fps)"
            self._cap = cv2.VideoCapture(0)
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
            self._cap.set(cv2.CAP_PROP_FPS, webcam_fps)
        else:
            stream_uri = video_source
            self._cap = cv2.VideoCapture(video_source)

        self.get_logger().info(f"Opening video source: {stream_uri}")
        if not self._cap.isOpened():
            self.get_logger().error(f"Failed to open video source at {stream_uri}")
            raise RuntimeError(f"Cannot open {stream_uri}")

        # ---- CV bridge (numpy ↔ ROS Image) ----
        self._bridge = CvBridge()

        # ---- Load Depth Anything V2 model ----
        self.get_logger().info(f"Loading model '{model_name}' on device '{device}'…")
        try:
            self._model = DepthAnythingV2Model(model_name=model_name, device=device,
                                               input_size=model_input_size,
                                               cpu_threads=cpu_threads)
            self._model.load()
            self.get_logger().info(f"Model loaded successfully on device '{self._model.device}'")
            if not self._model.device.startswith("cuda"):
                self.get_logger().info(
                    f"PyTorch CPU thread pool limited to {self._model.cpu_threads} threads "
                    f"(override with -p cpu_threads:=N, 0 = auto)"
                )
        except Exception as e:
            self.get_logger().error(f"Failed to load model: {e}")
            raise

        # ---- publishers ----
        # Using private namespace (~) so topics become /depth_node/<name>
        # Other nodes subscribe using the absolute path /depth_node/<name>
        self._depth_pub = self.create_publisher(Image, "~/depth_map", 10)
        self._viz_pub = self.create_publisher(Image, "~/depth_map_viz", 10)
        self._heartbeat_pub = self.create_publisher(Header, "~/heartbeat", 10)

        # ---- busy flag: skip timer ticks while an inference pass is still
        #      running.  Without it the executor queues a backlog of
        #      callbacks and the node pegs the CPU, starving MAVROS/Gazebo/
        #      SITL on the same machine. ----------------
        self._infer_busy = False

        # ---- timers ----
        infer_period = 1.0 / inference_rate
        self._infer_timer = self.create_timer(infer_period, self._inference_callback)

        hb_period = 1.0 / heartbeat_rate
        self._heartbeat_timer = self.create_timer(hb_period, self._heartbeat_callback)

        self.get_logger().info(
            f"Depth node ready – inference @ {inference_rate} Hz, "
            f"heartbeat @ {heartbeat_rate} Hz"
        )

    # ==================================================================
    # Callbacks
    # ==================================================================

    def _inference_callback(self):
        """
        Grab the latest frame, run depth estimation, and publish results.

        Called by a ROS timer – NEVER call spin_until_future_complete here.
        """
        # Non-blocking guard: if the previous inference pass is still
        # running, skip this tick instead of queueing a backlog.
        if self._infer_busy:
            return
        self._infer_busy = True

        # ---- grab the latest frame --
        if self._is_webcam:
            # V4L2 already returns the newest buffered frame on read();
            # draining would block for ~1/fps per grab (e.g. 50 x 140 ms
            # at 7 fps = 7 s stalls between inferences).
            ret, frame = self._cap.read()
        else:
            # UDP / file sources: drain stale frames – keep only the newest.
            # Bounded by count AND wall time (drain_budget) so a live stream
            # can never stall the inference loop while waiting for frames.
            deadline = time.monotonic() + self._drain_budget
            for _ in range(50):
                if not self._cap.grab():
                    break
                if time.monotonic() >= deadline:
                    break
            ret, frame = self._cap.retrieve()

        if not ret or frame is None:
            self._infer_busy = False
            self.get_logger().warn("Failed to retrieve frame from video stream", throttle_duration_sec=5.0)
            return

        # frame is BGR (OpenCV default) – convert to RGB for the model
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.get_logger().info(
            f"Running inference on {rgb.shape[1]}x{rgb.shape[0]} frame…",
            throttle_duration_sec=5.0,
        )

        # ---- run inference ----
        t0 = self.get_clock().now()
        try:
            depth = self._model.infer(rgb)
        except Exception as e:
            self._infer_busy = False
            self.get_logger().error(f"Inference failed: {e}", throttle_duration_sec=5.0)
            return
        dt = (self.get_clock().now() - t0).nanoseconds / 1e9
        self.get_logger().info(f"Inference done in {dt:.2f}s", throttle_duration_sec=5.0)

        # ---- publish raw depth map (32FC1) ----
        now = self.get_clock().now().to_msg()
        depth_msg = self._bridge.cv2_to_imgmsg(depth, encoding="32FC1")
        depth_msg.header.stamp = now
        depth_msg.header.frame_id = self._frame_id
        self._depth_pub.publish(depth_msg)

        # ---- publish colour-mapped depth (rgb8) ----
        if self._relative_depth:
            # Relative depth has no metric scale – stretch the colormap
            # over the 2nd–98th percentile of the current frame.
            if depth.size:
                vmin, vmax = np.percentile(depth, [2.0, 98.0])
            else:
                vmin, vmax = 0.0, 1.0
            if float(vmax) - float(vmin) < 1e-6:
                vmax = float(vmin) + 1.0
            coloured = _depth_to_colormap(depth, float(vmin), float(vmax))
        else:
            coloured = _depth_to_colormap(depth, self._cmap_vmin, self._cmap_vmax)
        viz_msg = self._bridge.cv2_to_imgmsg(coloured, encoding="bgr8")
        viz_msg.header.stamp = now
        viz_msg.header.frame_id = self._frame_id
        self._viz_pub.publish(viz_msg)

        # ---- optional live preview window ----
        if self._show_preview:
            cv2.imshow("Depth map (TURBO)", coloured)
            cv2.waitKey(1)

        self._infer_busy = False

    def _heartbeat_callback(self):
        """Publish a heartbeat at a fixed rate for the Emergency Node."""
        msg = Header()
        msg.stamp = self.get_clock().now().to_msg()
        msg.frame_id = "depth_node"
        self._heartbeat_pub.publish(msg)

    # ==================================================================
    # Cleanup
    # ==================================================================

    def destroy_node(self):
        if hasattr(self, "_cap") and self._cap is not None:
            self._cap.release()
        if self._show_preview:
            cv2.destroyAllWindows()
        super().destroy_node()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    rclpy.init()
    node = DepthNode()
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
