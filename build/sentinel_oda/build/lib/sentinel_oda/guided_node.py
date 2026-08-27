#!/usr/bin/env python3
"""
guided_node.py – the "pilot": executes Inner Map's safe path in GUIDED mode.

Runs on the drone.  Only acts while drone_state == "oda".

Design (settled with the user):
  - Subscribes to /inner_map/safe_path (nav_msgs/Path).  Every new Path
    REPLACES the stored path wholesale, even mid-traversal (Inner Map may
    keep refining the route while ODA Maneuvers probes).
  - The path is in LOCAL NED metres (x = North, y = East, z = Down),
    anchored to the EKF origin: first pose = the drone's current
    position, then one pose per safe-tile centre.
  - Walks the path sequentially: publishes the current target as a
    mavros_msgs/PositionTarget on /mavros/setpoint_raw/local with
    coordinate_frame = FRAME_LOCAL_NED (1, fixed EKF origin) and
    type_mask = 3576 (position-only: velocity/accel/yaw/yaw-rate all
    ignored).  CRITICAL: the message FIELDS must be ENU (x=East, y=North,
    z=Up) – mavros setpoint_raw converts the message from ENU to NED
    before sending it to the FCU (verified in mavros 2.14
    setpoint_raw.cpp::local_cb and on the wire in the SITL tlog: a NED
    hold (0, 110, -20) arrived at the FCU as (110, 0, +20)).  The path is
    NED, so this node swaps x/y and negates z here; mavros then converts
    back to the correct NED values on the wire.
  - Advances to the next point once /mavros/local_position/pose is within
    reach_tolerance_m (0.5 m, horizontal) of the current target.
  - Keepalive: if no target has been sent for resend_timeout (1.0 s), the
    current target is re-published unchanged (pure position targets in
    ArduPilot GUIDED hold until replaced, so this is a safety net, not a
    streaming requirement).
  - ARBITRATION with ODA Maneuvers: this node and oda_maneuvers share
    /mavros/setpoint_raw/local and the FCU follows the LAST message, so
    publishing ANYTHING while the scout sweep runs would stomp the brake
    and the yaw legs (observed live: the drone skipped the sweep and
    dived).  The path is therefore only flown once the first sweep has
    completed (rising True->False edge of /oda_maneuvers/sweeping);
    during every sweep, and whenever Detection reports an obstacle (ODA
    Maneuvers re-breaks/re-sweeps on those edges), this node publishes
    NOTHING at all – the FCU keeps following the last command ODA
    Maneuvers sent (user request: new setpoints only when not sweeping).
  - Leaving oda clears the path and stops all setpoints.  Emergency needs
    no dedicated check here: the state machine always leaves oda on
    emergency, and the FCU drops GUIDED targets in RTL/LAND anyway.
  - The GUIDED flight-mode switch is owned by oda_maneuvers, NOT this
    node (it is switched on ODA entry, before any path arrives).

Subscribes (absolute paths – these topics belong to other nodes):
  /inner_map/safe_path            – nav_msgs/Path
  /drone_node/drone_state         – std_msgs/String
  /oda_maneuvers/sweeping         – std_msgs/Bool (sweep gate)
  /detection_node/obstacle_detected – std_msgs/Bool (obstacle gate)
  /mavros/local_position/pose     – geometry_msgs/PoseStamped (ENU)

Publishes:
  /mavros/setpoint_raw/local  – mavros_msgs/PositionTarget
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from std_msgs.msg import Bool, String
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from mavros_msgs.msg import PositionTarget


class GuidedNode(Node):
    """Executes Inner Map's safe path in GUIDED mode (oda state only)."""

    # SET_POSITION_TARGET_LOCAL_NED type mask: position only (velocity,
    # acceleration, yaw and yaw-rate fields all ignored) = 3576.
    _POSITION_ONLY_MASK = (
        PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ
        | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ
        | PositionTarget.IGNORE_YAW | PositionTarget.IGNORE_YAW_RATE
    )

    def __init__(self):
        super().__init__("guided")

        # ---- parameters ----
        self.declare_parameter("reach_tolerance_m", 0.5)  # m, horizontal distance to a point before advancing
        self.declare_parameter("resend_timeout", 1.0)     # s, keepalive resend of the current target
        self.declare_parameter("tick_rate", 10.0)         # Hz, state-machine tick
        self.declare_parameter("status_rate", 1.0)        # Hz, in-ODA status log (position/altitude/gates)

        self._tol = max(0.1, float(self.get_parameter("reach_tolerance_m").value))
        self._resend_timeout = max(0.1, float(self.get_parameter("resend_timeout").value))
        tick_rate = max(1.0, float(self.get_parameter("tick_rate").value))
        status_rate = max(0.1, float(self.get_parameter("status_rate").value))

        # ---- state ----
        self._drone_state = "standby"
        self._pose_ned = None      # (x=N, y=E, z=D) local NED metres
        self._path = []            # [(x, y, z)] NED points of the current path
        self._idx = 0              # index of the target being flown to
        self._last_sent = 0.0      # node-clock seconds of the last setpoint
        self._sent = False         # a target has been sent for the current path

        # ---- sweep / obstacle arbitration -------
        self._sweeping = False        # True while ODA Maneuvers runs a scout sweep
        self._sweep_prev = False      # previous /oda_maneuvers/sweeping value
        self._sweep_ever_done = False # first full sweep completed -> path cleared
        self._obstacle = False        # latest /detection_node/obstacle_detected

        # ---- subscriptions (absolute paths: other nodes' topics) ----
        self.create_subscription(Path, "/inner_map/safe_path", self._path_cb, 10)
        self.create_subscription(String, "/drone_node/drone_state", self._state_cb, 10)
        self.create_subscription(
            Bool, "/oda_maneuvers/sweeping", self._sweeping_cb, 10
        )
        self.create_subscription(
            Bool, "/detection_node/obstacle_detected", self._obstacle_cb, 10
        )
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )

        # ---- publishers ----
        self._setpoint_pub = self.create_publisher(
            PositionTarget, "/mavros/setpoint_raw/local", 10
        )

        # ---- timers ----
        self.create_timer(1.0 / tick_rate, self._tick)
        self.create_timer(1.0 / status_rate, self._status_timer_cb)

        self.get_logger().info(
            f"GUIDED node ready – tolerance {self._tol:.1f} m, "
            f"keepalive {self._resend_timeout:.1f} s, "
            f"setpoints only while flying (sweep/obstacle gate ON)"
        )

    # ==================================================================
    # Callbacks
    # ==================================================================

    def _state_cb(self, msg: String):
        if msg.data == self._drone_state:
            return
        prev = self._drone_state
        self._drone_state = msg.data
        if prev != "oda" and msg.data == "oda":
            # Fresh ODA entry: the scout sweep must run BEFORE the path
            # is flown, so reset the sweep/obstacle tracking.
            self._sweeping = False
            self._sweep_prev = False
            self._sweep_ever_done = False
            self._obstacle = False
        elif prev == "oda" and msg.data != "oda":
            # Leaving ODA – drop the path and stop publishing setpoints.
            self._path = []
            self._idx = 0
            self._sent = False
            self.get_logger().info(
                f"Left ODA ({msg.data}) – safe path dropped, setpoints stopped"
            )

    def _sweeping_cb(self, msg: Bool):
        # Track the ODA Maneuvers scout sweep.  A True -> False edge means
        # one full sweep completed – only then may the path be flown.
        self._sweep_prev = self._sweeping
        self._sweeping = msg.data
        if self._sweep_prev and not self._sweeping and not self._sweep_ever_done:
            self._sweep_ever_done = True
            self.get_logger().info(
                "First scout sweep finished – safe path cleared for flight"
            )

    def _obstacle_cb(self, msg: Bool):
        self._obstacle = msg.data

    def _path_cb(self, msg: Path):
        # Only act while in ODA.
        if self._drone_state != "oda":
            return
        # Overwrite the stored path wholesale, even mid-traversal.
        self._path = [
            (float(p.pose.position.x), float(p.pose.position.y), float(p.pose.position.z))
            for p in msg.poses
        ]
        self._idx = 0
        self._sent = False
        self.get_logger().info(
            f"New safe path received: {len(self._path)} poses – replacing previous"
        )
        self._tick()   # command the first target right away

    def _pose_cb(self, msg: PoseStamped):
        p = msg.pose.position
        # ENU (x=E, y=N, z=U) -> NED (x=N, y=E, z=D)
        self._pose_ned = (float(p.y), float(p.x), float(-p.z))

    # ==================================================================
    # Tick: advance on reach, send / resend the current target
    # ==================================================================

    def _now(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def _gated(self) -> bool:
        """True while guided must publish NOTHING on the setpoint topic:
        until the first scout sweep completes, during every sweep, and
        whenever Detection reports an obstacle (ODA Maneuvers re-breaks /
        re-sweeps on those edges).  While gated, the FCU keeps following
        the last command ODA Maneuvers sent."""
        return self._sweeping or not self._sweep_ever_done or self._obstacle

    def _status_timer_cb(self):
        if self._drone_state != "oda" or self._pose_ned is None:
            return
        x, y, z = self._pose_ned
        self.get_logger().info(
            f"status: NED ({x:.1f}, {y:.1f}, {z:.1f}), alt {-z:.1f} m, "
            f"sweeping={self._sweeping}, sweep_done={self._sweep_ever_done}, "
            f"obstacle={self._obstacle}, gated={self._gated()}"
        )

    def _tick(self):
        if self._drone_state != "oda" or not self._path:
            return

        now = self._now()

        # Arbitration with ODA Maneuvers: publish NOTHING while the
        # scout sweep runs (or before the first one, or while an
        # obstacle is reported).  Any message here would stomp ODA
        # Maneuvers' brake and sweep legs on the shared setpoint topic.
        if self._gated():
            self._sent = False
            return

        if self._idx >= len(self._path):
            return  # path complete – the FCU holds the last position

        # Advance when within tolerance of the current target (horizontal).
        if self._pose_ned is not None:
            tx, ty, _ = self._path[self._idx]
            nx, ny, _ = self._pose_ned
            if math.hypot(tx - nx, ty - ny) <= self._tol:
                self._idx += 1
                self.get_logger().info(
                    f"Reached point {self._idx}/{len(self._path)}"
                )
                if self._idx >= len(self._path):
                    self.get_logger().info(
                        "Safe path complete – holding the last position"
                    )
                    return

        # Send the current target, or resend it as a keepalive.
        if not self._sent or now - self._last_sent >= self._resend_timeout:
            self._send_target(self._idx, now, quiet=self._sent)

    def _send_target(self, idx: int, now: float, quiet: bool = False):
        """Publish one path point as a position-only GUIDED setpoint.
        The path is NED; the message fields must be ENU (x=East, y=North,
        z=Up) because mavros converts ENU->NED on the wire."""
        x, y, z = self._path[idx]     # NED: x=N, y=E, z=D
        msg = PositionTarget()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.coordinate_frame = PositionTarget.FRAME_LOCAL_NED  # 1, fixed EKF origin
        msg.type_mask = self._POSITION_ONLY_MASK               # 3576
        msg.position.x = y           # ENU East
        msg.position.y = x           # ENU North
        msg.position.z = -z          # ENU Up
        self._setpoint_pub.publish(msg)
        self._last_sent = now
        self._sent = True
        if not quiet:
            self.get_logger().info(
                f"Setpoint {idx + 1}/{len(self._path)}: NED "
                f"({x:.1f}, {y:.1f}, {z:.1f})"
            )


def main():
    rclpy.init()
    node = GuidedNode()
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
