#!/usr/bin/env python3
"""
oda_maneuvers.py – the "scout": yaw-sweep probing in GUIDED mode.

Runs on the drone.  Only operates while drone_state == "oda".

Flow:
  1. ODA entered -> this node switches the FCU to GUIDED mode (it owns that
     switch) and the drone brakes to a position hold.
  2. Once GUIDED is confirmed -> the scouting sweep starts.  The current
     yaw (ψ0) is recorded and the drone rotates at `sweep_rate_deg_s`
     (default 3 deg/s, so a 180 deg fan takes ~60 s) from ψ0+span/2 to
     ψ0-span/2, then (by default) returns to ψ0.  The rotation is
     commanded through the yaw field of SET_POSITION_TARGET_LOCAL_NED,
     with the drone's CURRENT NED position carried in the same message
     (position hold).  ArduPilot Copter drops commands whose position,
     velocity AND acceleration bits are all masked (it calls
     hold_position() without ever reading yaw or yaw_rate – verified in
     4.8-dev GCS_MAVLink_Copter.cpp), so the position must be present.
     The commanded yaw is ramped at the sweep rate; the rate is
     proportional to the remaining error near the target, so the stop is
     smooth and accurate, not a snap.
  3. Sweep done -> the rate command stops and the node waits.  A fresh
     rising edge on obstacle_detected (in ODA that is the 0.8 m threshold)
     starts a new sweep.  Obstacles seen DURING a sweep never restart it.
  4. Leaving ODA (mission resumed, emergency -> landing) -> all setpoints
     stop immediately and the node resets.

While sweeping, ~/sweeping = True is published; the Detection node uses it
to run with the 10 m threshold during sweeps and the 0.8 m threshold
between them.

Yaw bookkeeping:
  - Heading is read from /mavros/local_position/pose with the standard
    ENU-quaternion yaw formula (0 = East, CCW positive) – the same
    convention detection_node uses for current_heading.
  - Sweep offsets are applied in that ENU domain, so +90 deg = turn left.
  - The yaw sent to the FCU is converted to the NED convention expected by
    SET_POSITION_TARGET_LOCAL_NED:  yaw_ned = pi/2 - yaw_enu.

Subscribes (absolute paths – these topics belong to other nodes):
  /drone_node/drone_state           – std_msgs/String (oda gate)
  /detection_node/obstacle_detected – std_msgs/Bool (re-sweep trigger)
  /mavros/local_position/pose       – geometry_msgs/PoseStamped (yaw)
  /mavros/state                     – mavros_msgs/State (mode confirmation)

Publishes:
  /mavros/setpoint_raw/local – mavros_msgs/PositionTarget, current NED
                               position + ramped yaw angle
                               (coordinate_frame=1, velocity/accel/yaw_rate
                               ignored, yaw used)
  ~/sweeping                 – std_msgs/Bool, threshold selector for Detection

Service client:
  /mavros/set_mode           – mavros_msgs/SetMode -> custom_mode "GUIDED"

All service calls are async (call_async + poll on a timer tick) – NEVER
spin_until_future_complete in a callback.
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Duration

from std_msgs.msg import Bool, String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import PositionTarget, State
from mavros_msgs.srv import SetMode


def _wrap_pi(a: float) -> float:
    """Wrap an angle to [-pi, pi)."""
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def _angle_diff(a: float, b: float) -> float:
    """Signed difference a - b, wrapped to [-pi, pi)."""
    return _wrap_pi(a - b)


class OdaManeuvers(Node):
    """Scouting yaw sweep – GUIDED switch + 180 deg position-hold yaw fan."""

    def __init__(self):
        super().__init__("oda_maneuvers")

        # ---- parameters ----
        self.declare_parameter("tick_rate", 10.0)                 # Hz, state-machine tick
        self.declare_parameter("sweep_rate_deg_s", 3.0)           # deg/s, sweep yaw rate (180 deg in 60 s)
        self.declare_parameter("sweep_span_deg", 180.0)           # deg, total fan width of the sweep
        self.declare_parameter("return_to_heading", True)         # rotate back to ψ0 after the fan
        self.declare_parameter("sweep_rate_kp", 1.0)              # 1/s, proportional rate near the target
        self.declare_parameter("yaw_tolerance_deg", 5.0)          # deg, "heading reached"
        self.declare_parameter("leg_timeout_scale", 2.5)          # reach timeout = expected leg time × scale
        self.declare_parameter("mode_switch_retry_interval", 2.0) # s, SetMode backoff

        tick_rate = max(1.0, float(self.get_parameter("tick_rate").value))
        self._tick_period = 1.0 / tick_rate
        self._rate_max = math.radians(max(0.1, float(self.get_parameter("sweep_rate_deg_s").value)))
        self._span = math.radians(max(0.0, float(self.get_parameter("sweep_span_deg").value)))
        self._return_to_psi0 = bool(self.get_parameter("return_to_heading").value)
        self._rate_kp = max(0.05, float(self.get_parameter("sweep_rate_kp").value))
        self._yaw_tol = math.radians(float(self.get_parameter("yaw_tolerance_deg").value))
        self._timeout_scale = max(1.1, float(self.get_parameter("leg_timeout_scale").value))
        self._mode_retry_interval = float(self.get_parameter("mode_switch_retry_interval").value)

        # ---- state ----
        self._drone_state = "standby"
        self._yaw_enu = None           # None until the first pose message arrives
        self._fcu_mode = ""            # latest /mavros/state mode string
        self._phase = "idle"           # idle | switching | sweeping | waiting
        self._mode_future = None       # pending SetMode(GUIDED) future
        self._mode_req_sent_at = None
        self._mode_retry_after = None
        self._break_sent = False       # breaking command sent
        self._psi0 = 0.0               # yaw at sweep start (ENU domain)
        self.pi = math.pi              # pi constant for convenience
        self._cmd_yaw_enu = 0.0        # commanded yaw (ENU), ramped at sweep rate
        self._pos_ned = None           # latest NED position (x=N, y=E, z=D)
        self.yaws = [self.pi/2.0, -self.pi/4.0, 
                    -self.pi/4.0, -self.pi/4.0, 
                    -self.pi/4.0, self.pi/2.0] 
        self._break_start_time = self.get_clock().now()
        self._sweep_start_time = self.get_clock().now()
        self._obstacle_edge = False    # rising edge seen on obstacle_detected
        self._obstacle_prev = False

        # ---- subscriptions (absolute paths: other nodes' topics) ----
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)
        self.create_subscription(
            Bool, "/detection_node/obstacle_detected", self._obstacle_cb, 10
        )
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )
        self.create_subscription(State, "/mavros/state", self._fcu_state_cb, 10)

        # ---- publishers ----
        self._setpoint_pub = self.create_publisher(
            PositionTarget, "/mavros/setpoint_raw/local", 10
        )
        self._sweeping_pub = self.create_publisher(Bool, "~/sweeping", 10)

        # ---- service client ----
        self._mode_cli = self.create_client(SetMode, "/mavros/set_mode")

        # ---- state-machine tick ----
        self.create_timer(1.0 / tick_rate, self._tick)

        self.get_logger().info(
            "ODA Maneuvers ready – position-hold yaw sweep: "
            f"{math.degrees(self._span):.0f} deg fan at "
            f"{math.degrees(self._rate_max):.1f} deg/s, "
            f"tolerance {math.degrees(self._yaw_tol):.1f} deg, "
            f"{'returning to ψ0' if self._return_to_psi0 else 'no return leg'}"
        )

    # ==================================================================
    # Callbacks (never block – flags and state only)
    # ==================================================================

    def _state_cb(self, msg: String):
        if msg.data == self._drone_state:
            return
        prev = self._drone_state
        self._drone_state = msg.data
        if msg.data == "oda" and prev != "oda":
            self._on_oda_enter()
        elif msg.data != "oda" and prev == "oda":
            self._on_oda_exit()

    def _obstacle_cb(self, msg: Bool):
        # Rising-edge detector; only the waiting phase consumes the flag.
        # Edges raised DURING a sweep are discarded: detection publishes
        # True for the whole sweep and resets to False when it ends, so a
        # mid-sweep edge would otherwise restart the sweep forever.
        prev = self._obstacle_prev
        self._obstacle_prev = msg.data
        if msg.data and not prev and self._phase != "sweeping":
            self._obstacle_edge = True

    def _pose_cb(self, msg: PoseStamped):
        q = msg.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self._yaw_enu = math.atan2(siny, cosy)
        # /mavros/local_position/pose is ENU (x=East, y=North, z=Up);
        # SET_POSITION_TARGET_LOCAL_NED wants NED (x=North, y=East, z=Down).
        self._pos_ned = (
            float(msg.pose.position.y),
            float(msg.pose.position.x),
            float(-msg.pose.position.z),
        )

    def _fcu_state_cb(self, msg: State):
        self._fcu_mode = msg.mode

    # ==================================================================
    # ODA entry / exit
    # ==================================================================

    def _on_oda_enter(self):
        self._phase = "switching"
        self._mode_future = None
        self._mode_req_sent_at = None
        self._mode_retry_after = None
        self._legs = []
        self._obstacle_edge = False
        self._publish_sweeping(False)
        self.get_logger().info("ODA entered – switching to GUIDED, then scouting sweep")

    def _on_oda_exit(self):
        self._phase = "idle"
        self._mode_future = None
        self._mode_req_sent_at = None
        self._mode_retry_after = None
        self._legs = []
        self._obstacle_edge = False
        self._publish_sweeping(False)
        self.get_logger().info("ODA left – setpoints stopped, node reset")

    # ==================================================================
    # State-machine tick (timer-driven)
    # ==================================================================

    def _tick(self):
        if self._drone_state != "oda":
            return  # idle – nothing published

        if self._phase == "switching":
            self._tick_switching()
        elif self._phase == "breaking":
            self._break_drone()
        elif self._phase == "sweeping":
            self._do_sweep()
        elif self._phase == "waiting" and self._obstacle_edge:
            if self._do_sweep():
                self._obstacle_edge = False
            else:
                self.get_logger().warn(
                    "No pose yet – cannot start sweep, will retry"
                )

    def _tick_switching(self):
        if self._fcu_mode == "GUIDED":
            self.get_logger().info(
                "GUIDED confirmed – initiating breaking sequence before starting the scouting sweep"
            )
            self._obstacle_edge = False
            self._phase = "breaking"
            self._break_start_time = self.get_clock().now()
            return

        # Never override an emergency/landing flight mode.
        if self._fcu_mode in ("RTL", "LAND"):
            self.get_logger().warn(
                f"FCU is in {self._fcu_mode} – holding off on the GUIDED switch"
            )
            return

        now = self.get_clock().now()

        if self._mode_future is None:
            if self._mode_retry_after is not None and now < self._mode_retry_after:
                return
            if not self._mode_cli.service_is_ready():
                self.get_logger().warn(
                    "SetMode service not ready – will retry"
                )
                self._mode_retry_after = now + Duration(seconds=self._mode_retry_interval)
                return
            req = SetMode.Request()
            req.base_mode = 0
            req.custom_mode = "GUIDED"
            self._mode_future = self._mode_cli.call_async(req)
            self._mode_req_sent_at = now
            self.get_logger().info("Requesting GUIDED mode from the FCU...")
            return

        # pending future: abandon it if mavros never answers
        pending = (now - self._mode_req_sent_at).nanoseconds / 1e9
        if not self._mode_future.done():
            if pending > 5.0:
                self.get_logger().warn("GUIDED request timed out – will retry")
                self._mode_future = None
                self._mode_retry_after = now + Duration(seconds=self._mode_retry_interval)
            return

        res = self._mode_future.result()
        self._mode_future = None
        self._mode_req_sent_at = None
        if res is None or not res.mode_sent:
            self.get_logger().warn(
                "GUIDED switch rejected – will retry"
            )
            self._mode_retry_after = now + Duration(seconds=self._mode_retry_interval)
            return

        self.get_logger().info("GUIDED request sent – waiting for FCU confirmation")

    # ==================================================================
    # Sweep sequencing
    # ==================================================================

    def _break_drone(self):
        """Breaking sequence before starting the sweep"""

        if not self._break_sent:
            self._break_start_time = self.get_clock().now()
            msg = PositionTarget()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
            msg.type_mask = (
                PositionTarget.IGNORE_PX | PositionTarget.IGNORE_PY | PositionTarget.IGNORE_PZ
                | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ
                | PositionTarget.IGNORE_YAW_RATE
            )
            
            msg.velocity.x, msg.velocity.y, msg.velocity.z = 0.0, 0.0, 0.0
            msg.yaw = 0.0
            self._setpoint_pub.publish(msg)
            self.get_logger().info(f"#####################################Breaking command sent !#####################################")

            self._break_sent = True

        if self.get_clock().now() - self._break_start_time < Duration(seconds=10.0):
            return  # wait for the pose to finish
        
        self._phase = "sweeping"
        self._do_sweep()
        return True

    def _do_sweep(self) -> bool:
        """Begin a sweep relative to the current yaw."""
        self._publish_sweeping(True)

        if self.get_clock().now() - self._sweep_start_time < Duration(seconds=5.0):
            return  # wait for the pose to finish

        if len(self.yaws) == 0:
            self._finish_sweep()
            return

        self._sweep_start_time = self.get_clock().now()
        self._cmd_yaw_enu = self.yaws.pop()
        msg = PositionTarget()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
        msg.type_mask = (
            PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ
            | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ
            | PositionTarget.IGNORE_YAW_RATE
        )
        
        msg.position.x, msg.position.y, msg.position.z = 0.0, 0.0, 0.0
        msg.yaw = self._cmd_yaw_enu
        self._setpoint_pub.publish(msg)
        self.get_logger().info(f"#####################################Published yaw setpoint !#####################################")

        self.get_logger().info(
            f"Scouting ongoing, current leg: {self._cmd_yaw_enu}"
        )
        return True

    def _finish_sweep(self):
        self._phase = "waiting"
        self.yaws = [self.pi/2.0, -self.pi/4.0, 
                    -self.pi/4.0, -self.pi/4.0, 
                    -self.pi/4.0, self.pi/2.0]
        self._publish_sweeping(False)
        self.get_logger().info(
            "Sweep complete – setpoints stopped, waiting for the next "
            "obstacle_detected trigger"
        )

    # ==================================================================
    # Setpoint / helper publishers
    # ==================================================================

    def _send_yaw_setpoint(self):
        """
        Publish a PositionTarget that holds the current position and asks
        for a yaw angle.

        ArduPilot Copter's handle_message_set_position_target_local_ned
        treats a command whose position, velocity AND acceleration bits are
        ALL masked as unsupported and calls hold_position() WITHOUT reading
        yaw or yaw_rate (verified in 4.8-dev GCS_MAVLink_Copter.cpp) –
        that is why the previous yaw-only and yaw-rate-only commands never
        rotated the drone.  With the position bits present the FCU takes
        the branch set_pos_NED_m(..., use_yaw=true, ...), which feeds the
        yaw field into auto_yaw ANGLE_RATE mode (0 = North, positive = CW
        in NED) while keeping the position hold active.
        """
        if self._pos_ned is None:
            return
        msg = PositionTarget()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.coordinate_frame = PositionTarget.FRAME_BODY_NED
        msg.type_mask = (
            PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ
            | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ
            | PositionTarget.IGNORE_YAW_RATE
        )
        
        msg.position.x, msg.position.y, msg.position.z = self._pos_ned
        # ENU yaw (0=East, CCW +) -> NED yaw (0=North, CW +): pi/2 - yaw.
        msg.yaw = math.pi / 2.0 - self._cmd_yaw_enu
        self._setpoint_pub.publish(msg)
        self.get_logger().info(f"#####################################Published yaw setpoint !###################################")

    def _publish_sweeping(self, value: bool):
        self._sweeping_pub.publish(Bool(data=value))


def main():
    rclpy.init()
    node = OdaManeuvers()
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
