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
import copy

import rclpy
from rclpy.node import Node
from rclpy.time import Duration
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import PositionTarget



class OdaManeuvers(Node):
    """Scouting yaw sweep – GUIDED switch + 180 deg position-hold yaw fan."""

    def __init__(self):
        super().__init__("oda_maneuvers")

        # ---- parameters ----
        self.declare_parameter("tick_rate", 10.0)                 # Hz, state-machine tick

        tick_rate = max(1.0, float(self.get_parameter("tick_rate").value))

        # ---- state ----
        self._psi0 = 0.0               # yaw at sweep start (ENU domain)
        self.pi = math.pi              # pi constant for convenience
        self._cmd_yaw_enu = 0.0        # commanded yaw (ENU), ramped at sweep rate
        self._pos_ned = None           # latest NED position (x=N, y=E, z=D)
        self.yaws = [self.pi/2.0, -self.pi/4.0, 
                     -self.pi/4.0, -self.pi/4.0, 
                     -self.pi/4.0, self.pi/2.0]                 # list of yaw setpoints to send  

        # ---- subscriptions (absolute paths: other nodes' topics) ----
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )

        # ---- publishers ----
        self._setpoint_pub = self.create_publisher(
            PositionTarget, "/mavros/setpoint_raw/local", 10
        )
        # ---- state-machine tick ----
        self.create_timer(1.0 / tick_rate, self._send_yaw_setpoint)
        self.start_time = self.get_clock().now()

    # ==================================================================
    # Callbacks (never block – flags and state only)
    # ==================================================================


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

        if self.get_clock().now() - self.start_time < Duration(seconds=5.0):
            return  # wait for the pose to finish

        if len(self.yaws) == 0:
            return

        self.start_time = self.get_clock().now()
        self._cmd_yaw_enu = self.yaws.pop()
        pos = copy.deepcopy(self._pos_ned)
        msg = PositionTarget()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
        msg.type_mask = (
            PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ
            | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ
            | PositionTarget.IGNORE_YAW_RATE
        )
        
        msg.position.x, msg.position.y, msg.position.z = 0.0, 0.0, 0.0
        # ENU yaw (0=East, CCW +) -> NED yaw (0=North, CW +): pi/2 - yaw.
        msg.yaw = self._cmd_yaw_enu
        self._setpoint_pub.publish(msg)
        self.get_logger().info(f"#####################################Published yaw setpoint !###################################")


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

