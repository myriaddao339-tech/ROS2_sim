#!/usr/bin/env python3
"""
drone_node.py – Central state machine orchestrator for Sentinel V1.

States:  standby → mission → (oda) → landing → standby
Triggers (all topics, continuous until target state reached):
  start, end, emergency, mission_finished, waypoint_reached, obstacle_detected

Publishes drone_state at 1 Hz so every other node can gate its behaviour.
Uses the `transitions` library for clean state management.
"""

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Duration

from std_msgs.msg import Bool, Int32, String
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL, WaypointPush
from sentinel_mission_msgs.srv import GetMission

from transitions import Machine


# ---------------------------------------------------------------------------
# Drone Node
# ---------------------------------------------------------------------------

class DroneNode(Node):
    """State-machine based mission orchestrator."""

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self):
        super().__init__("drone_node")

        # --- Parameters ---
        self.declare_parameter("mission_service_name", "mission_node/get_mission")
        self.declare_parameter("takeoff_altitude", 15.0)
        self.declare_parameter("prearm_check_timeout", 30.0)
        self.declare_parameter("arm_timeout", 10.0)
        self.declare_parameter("takeoff_timeout", 30.0)
        self.declare_parameter("connection_timeout", 5.0)
        self.declare_parameter("waypoint_upload_timeout", 10.0)
        self.declare_parameter("state_publish_rate", 1.0)
        self.declare_parameter("takeoff_settle_sec", 2.0)
        self.declare_parameter("takeoff_retry_interval", 2.0)

        self._takeoff_alt = self.get_parameter("takeoff_altitude").value
        self._prearm_timeout = self.get_parameter("prearm_check_timeout").value
        self._arm_timeout = self.get_parameter("arm_timeout").value
        self._takeoff_timeout = self.get_parameter("takeoff_timeout").value
        self._conn_timeout = self.get_parameter("connection_timeout").value
        self._wp_upload_timeout = self.get_parameter("waypoint_upload_timeout").value
        self._takeoff_settle_sec = self.get_parameter("takeoff_settle_sec").value
        self._takeoff_retry_interval = self.get_parameter("takeoff_retry_interval").value

        # --- MAVROS service clients ---
        self._arm_cli = self.create_client(CommandBool, "/mavros/cmd/arming")
        self._takeoff_cli = self.create_client(CommandTOL, "/mavros/cmd/takeoff")
        self._mode_cli = self.create_client(SetMode, "/mavros/set_mode")
        self._wp_push_cli = self.create_client(WaypointPush, "/mavros/mission/push")

        self._waypoints_future = None
        self._arm_future = None
        self._takeoff_future = None
        self._takeoff_guided_sent = False
        self._guided_mode_future = None
        self._auto_mode_future = None
        self._rtl_mode_future = None
        self._guided_ok_since = None
        self._takeoff_backoff_until = None
        self._takeoff_accepted = False

        # --- Mission service client ---
        mission_srv_name = self.get_parameter("mission_service_name").value
        self._mission_cli = self.create_client(GetMission, mission_srv_name)
        self._mission_future = None

        # --- MAVROS subscriptions ---
        self.fcu_state = State()
        self.create_subscription(State, "/mavros/state", self._fcu_state_cb, 10)

        self.local_pose = PoseStamped()
        self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self._pose_cb, qos_profile_sensor_data
        )

        # --- Trigger subscriptions ---
        self._trigger_values = {
            "start": False, "end": False, "emergency": False,
            "mission_finished": False, "obstacle_detected": False,
        }
        self._trigger_last = dict(self._trigger_values)
        self._waypoint_reached_seq = None

        self.create_subscription(Bool, "/start_trigger/start", self._make_trigger_cb("start"), 10)
        self.create_subscription(Bool, "~/end", self._make_trigger_cb("end"), 10)
        self.create_subscription(Bool, "/emergency_node/emergency", self._make_trigger_cb("emergency"), 10)
        self.create_subscription(Bool, "/mission_node/mission_finished", self._make_trigger_cb("mission_finished"), 10)
        self.create_subscription(Bool, "/detection_node/obstacle_detected", self._make_trigger_cb("obstacle_detected"), 10)
        self.create_subscription(Int32, "/mission_node/waypoint_reached", self._wp_reached_cb, 10)

        # --- Publisher: drone_state ---
        self._state_pub = self.create_publisher(String, "~/drone_state", 10)
        self._current_state = "standby"

        pub_period = 1.0 / self.get_parameter("state_publish_rate").value
        self._state_timer = self.create_timer(pub_period, self._publish_state)

        # --- State machine (transitions library) ---
        self._sm = Machine(
            model=self,
            states=["standby", "mission", "oda", "landing"],
            initial="standby",
            send_event=True,           # callbacks receive event_data
            queued=True,               # queue transitions so they don't nest
        )

        # Define transitions
        self._sm.add_transition(
            trigger="do_start", source="standby", dest="mission",
            after="_on_enter_mission",
        )
        self._sm.add_transition(
            trigger="do_obstacle", source="mission", dest="oda",
            after="_on_enter_oda",
        )
        self._sm.add_transition(
            trigger="do_mission_finished", source="mission", dest="landing",
            after="_on_enter_landing",
        )
        self._sm.add_transition(
            trigger="do_emergency", source=["mission", "oda"], dest="landing",
            after="_on_enter_landing",
        )
        self._sm.add_transition(
            trigger="do_waypoint_reached", source="oda", dest="mission",
            after="_on_resume_mission",
        )
        self._sm.add_transition(
            trigger="do_end", source="landing", dest="standby",
            after="_on_enter_standby",
        )

        # --- Mission initialization state machine (sub-steps) ---
        # Steps: 0=idle, 1=request_
        # Reset trigger edge-detectimission, 2=verify_fcu, 3=upload_wp,
        #        4=prearm, 5=arm, 6=takeoff, 7=auto_mode, 8=done
        self._init_step = 1
        self._init_step_start_time = None
        self._mission_waypoints = []
        self._init_timer = self.create_timer(0.2, self._advance_init_step)

        self.get_logger().info("Drone node ready – state = standby")

    # ------------------------------------------------------------------
    # MAVROS callbacks
    # ------------------------------------------------------------------

    def _fcu_state_cb(self, msg: State):
        self.fcu_state = msg
        # Catch-all: disarmed → standby (safety net, step 13)
        if self._current_state != "standby" and not msg.armed:
            self.get_logger().warn("Drone disarmed unexpectedly — returning to standby")
            self._force_standby()

    def _pose_cb(self, msg: PoseStamped):
        self.local_pose = msg

    # ------------------------------------------------------------------
    # Trigger subscription helpers
    # ------------------------------------------------------------------

    def _make_trigger_cb(self, name: str):
        """Create a callback that does edge detection on a Bool trigger topic."""
        def cb(msg: Bool):
            prev = self._trigger_last[name]
            self._trigger_last[name] = msg.data
            # React on False → True edge only
            if msg.data and not prev:
                self.get_logger().info(f"Trigger [{name}] fired")
                self._handle_trigger(name)
        return cb

    def _wp_reached_cb(self, msg: Int32):
        self.get_logger().info(f"Trigger [waypoint_reached] seq={msg.data}")
        self._waypoint_reached_seq = msg.data
        self._handle_trigger("waypoint_reached")

    def _handle_trigger(self, name: str):
        """Route a trigger to the appropriate transition method."""
        current = self._current_state
        self.get_logger().info(f"Trigger [{name}] in state [{current}]")

        if name == "start" and current == "standby":
            self.do_start()
        elif name == "obstacle_detected" and current == "mission":
            self.do_obstacle()
        elif name == "mission_finished" and current == "mission":
            self.do_mission_finished()
        elif name == "emergency" and current in ("mission", "oda"):
            self.do_emergency()
        elif name == "waypoint_reached":
            if current == "oda":
                self.do_waypoint_reached()
            elif current == "mission":
                self.get_logger().info(
                    f"Waypoint {self._waypoint_reached_seq} reached (already in mission)"
                )
            # else: ignore in other states
        elif name == "end" and current == "landing":
            self.do_end()
        else:
            self.get_logger().debug(
                f"Ignoring trigger [{name}] — not valid in state [{current}]"
            )

    # ------------------------------------------------------------------
    # State publishing
    # ------------------------------------------------------------------

    def _publish_state(self):
        msg = String()
        msg.data = self._current_state
        self._state_pub.publish(msg)

    def _set_state(self, new_state: str):
        """Update the tracked state (kept in sync with transitions machine)."""
        self._current_state = new_state
        self.get_logger().info(f"STATE → {new_state}")

        # Publish immediately instead of waiting for the next 1 Hz tick:
        # nodes like ODA Maneuvers gate on drone_state and must start the
        # GUIDED brake the moment mission → oda happens.
        self._publish_state()

    def _force_standby(self):
        """Force reset to standby (used for unexpected disarm)."""
        self._init_timer.cancel()
        self._sm.set_state("standby")
        self._set_state("standby")

    # ==================================================================
    # STATE: standby
    # ==================================================================

    def _on_enter_standby(self, event):
        self._set_state("standby")
        self._init_step = 1
        self._init_step_start_time = self.get_clock().now()
        self._init_timer.reset()
        self._landing_step = 0
        self._takeoff_guided_sent = False
        self._takeoff_accepted = False
        # Reset trigger edge-detection flags so start can fire again
        for key in self._trigger_last:
            self._trigger_last[key] = False
        self._waypoint_reached_seq = None
        self._mission_waypoints = []
        self.get_logger().info("=== STANDBY: ready for next mission ===")

    # ==================================================================
    # STATE: mission  (entry = run init sequence)
    # ==================================================================

    def _on_enter_mission(self, event):
        self._set_state("mission")
        self._guided_ok_since = None
        self._takeoff_backoff_until = None
        self._takeoff_accepted = False
        self.get_logger().info("Starting MISSION")

    def _advance_init_step(self):
        """
        Timer-driven state machine for the mission initialization sequence.
        Steps:
          1 – Request mission from Mission Node
          2 – Verify FCU connection
          3 – Upload waypoints to FCU
          4 – Pre-arm checks
          5 – Arm
          6 – Takeoff
          7 – Switch to AUTO
          8 – Done (mission is now running)
        """
        step = self._init_step
        if step == 0:
            return  # idle

        now = self.get_clock().now()
        elapsed = (now - self._init_step_start_time).nanoseconds / 1e9 if self._init_step_start_time else 0.0

        if step == 1:
            self._step_request_mission(elapsed)
        elif step == 2:
            self._step_verify_fcu(elapsed)
        elif step == 3:
            self._step_upload_waypoints(elapsed)
        elif step == 4:
            self._step_prearm(elapsed)
        elif step == 5:
            self._step_arm(elapsed)
        elif step == 6 and self._current_state == "mission":
            self._step_takeoff(elapsed)
        elif step == 7:
            self._step_auto_mode(elapsed)
        elif step >= 8:
            self._init_timer.cancel()
            self.get_logger().info("=== MISSION: flying AUTO, waiting for triggers ===")

    def _advance(self, timeout: float) -> bool:
        """Check for timeout on current step. Returns True if timed out."""
        elapsed = (self.get_clock().now() - self._init_step_start_time).nanoseconds / 1e9
        if elapsed > timeout:
            self.get_logger().error(f"Init step {self._init_step} timed out ({timeout}s)")
            self._force_standby()
            return True
        return False

    def _next_step(self):
        self._init_step += 1
        self._init_step_start_time = self.get_clock().now()

    # -- Step 1: Request mission ---
    def _step_request_mission(self, elapsed):
        if self._mission_future is None:
            if not self._mission_cli.service_is_ready():
                if elapsed > self._wp_upload_timeout:  # or a dedicated mission_timeout param
                    self.get_logger().error("Mission service not available")
                    self._force_standby()
                return
            req = GetMission.Request()
            req.mission_file = ""
            self._mission_future = self._mission_cli.call_async(req)
            return  # response not ready yet, check again next tick

        if not self._mission_future.done():
            if elapsed > self._wp_upload_timeout:
                self.get_logger().error("Mission request timed out — no response")
                self._mission_future = None
                self._force_standby()
            return

        res = self._mission_future.result()
        self._mission_future = None
        if res is None or not res.success:
            self.get_logger().error(f"Mission request failed: {res.message if res else 'no response'}")
            self._force_standby()
            return

        self._mission_waypoints = res.waypoints
        self.get_logger().info(f"Received {len(self._mission_waypoints)} waypoints")
        self._next_step()
        
    # -- Step 2: Verify FCU connection ---
    def _step_verify_fcu(self, elapsed):
        self.get_logger().info("Step 2: Verifying FCU connection...")
        if self.fcu_state.connected:
            self.get_logger().info("FCU connected")
            self._next_step()
        elif elapsed > self._conn_timeout:
            self.get_logger().error("FCU connection timeout")
            self._force_standby()

    # -- Step 3: Upload waypoints ---
    def _step_upload_waypoints(self, elapsed):
        self.get_logger().info("Step 3: Uploading waypoints to FCU...")
        if not self._waypoints_future:
            if not self._wp_push_cli.service_is_ready():
                if elapsed > self._wp_upload_timeout:
                    self.get_logger().error("WaypointPush service unavailable")
                    self._force_standby()
                return

            req = WaypointPush.Request()
            req.start_index = 0
            req.waypoints = self._mission_waypoints
            self._waypoints_future = self._wp_push_cli.call_async(req)
            return

        if not self._waypoints_future.done():
            if elapsed > self._wp_upload_timeout:
                self.get_logger().error("Waypoint request timed out — no response")
                self._waypoints_future = None
                self._force_standby()
            return

        res = self._waypoints_future.result()

        if res is None or not res.success:
            self.get_logger().error("Waypoint upload failed")
            self._force_standby()
            return

        self.get_logger().info(
            f"Uploaded {res.wp_transfered}/{len(self._mission_waypoints)} waypoints"
        )
        
        self._waypoints_future = None
        self._next_step()

    # -- Step 4: Pre-arm checks ---
    def _step_prearm(self, elapsed):
        self.get_logger().info("Step 4: Pre-arm checks...")
        # system_status >= 3 means MAV_STATE_STANDBY (ready to arm)
        if self.fcu_state.system_status >= 3 and not self.fcu_state.armed:
            self.get_logger().info("Pre-arm checks passed")
            self._next_step()
        elif elapsed > self._prearm_timeout:
            self.get_logger().error(
                f"Pre-arm timeout — system_status={self.fcu_state.system_status}, "
                f"armed={self.fcu_state.armed}"
            )
            self._force_standby()

    # -- Step 5: Arm ---
    def _step_arm(self, elapsed):
        
        # Wait for armed confirmation
        if self.fcu_state.armed:
            self.get_logger().info("Armed")
            self._next_step()
            return
        
        self.get_logger().info("Step 5: Arming...")

        if not self._arm_future:
            if not self._arm_cli.service_is_ready():
                if elapsed > self._arm_timeout:
                    self.get_logger().error("Arming service unavailable")
                    self._force_standby()
                return

            arm_req = CommandBool.Request()
            arm_req.value = True
            self._arm_future = self._arm_cli.call_async(arm_req)
            return

        if not self._arm_future.done():
            if elapsed > self._arm_timeout:
                self.get_logger().error("Arming request timed out — no response")
                self._arm_future = None
                self._force_standby()
            return

        res = self._arm_future.result()
        self._arm_future = None

        if res is None or not res.success:
            if elapsed > self._arm_timeout:
                self.get_logger().error("Arming command failed")
                self._force_standby()
            return

        if elapsed > self._arm_timeout:
            self.get_logger().error("Arming Failed - timeout")
            self._force_standby()
            return

    # -- Step 6: Takeoff ---
    def _step_takeoff(self, elapsed):
        # Wait for altitude
        if self.local_pose.pose.position.z >= self._takeoff_alt - 0.5:
            self.get_logger().info(f"Takeoff altitude reached: {self.local_pose.pose.position.z:.1f}m")
            self._next_step()
            return

        # --- Switch to GUIDED mode before takeoff (ArduPilot requirement) ---
        if not self.fcu_state.mode == "GUIDED":
            self.get_logger().info("Step 6: Switching to GUIDED mode...")
            if self._guided_mode_future is None:
                
                if not self._mode_cli.service_is_ready():
                    if elapsed > self._takeoff_timeout:
                        self.get_logger().error("Failed to switch to GUIDED mode - service unavailable")
                        self._force_standby()
                    return
                mode_req = SetMode.Request()
                mode_req.base_mode = 0
                mode_req.custom_mode = "GUIDED"
                self._guided_mode_future = self._mode_cli.call_async(mode_req)
                return
            if elapsed > self._takeoff_timeout:
                self.get_logger().error("Failed to switch to GUIDED mode - timeout")
                self._force_standby()
            return

        # --- Send CommandTOL ---
        self._guided_mode_future = None  # reset guided mode future after successful switch

        # Once the FCU has ACCEPTED a takeoff command, never re-send it:
        # mavros aborts on duplicate COMMAND_ACKs (std::future_error) and
        # re-sending every tick while climbing was triggering that race.
        # Just monitor the climb instead.
        if self._takeoff_accepted:
            self.get_logger().info(
                f"Takeoff accepted - climbing to {self._takeoff_alt}m "
                f"(current {self.local_pose.pose.position.z:.1f}m)",
                throttle_duration_sec=5.0,
            )
            return

        # Let the mode change settle before the first takeoff command:
        # ArduPilot rejects NAV_TAKEOFF while it is still settling, and the
        # old 0.4 s retry storm (one command per tick) made things worse.
        now = self.get_clock().now()
        if self._guided_ok_since is None:
            self._guided_ok_since = now
        settle_secs = (now - self._guided_ok_since).nanoseconds / 1e9
        if settle_secs < self._takeoff_settle_sec:
            return

        if not self._takeoff_future:
            if not self._takeoff_cli.service_is_ready():
                if elapsed > self._takeoff_timeout:
                    self.get_logger().error("Takeoff service unavailable")
                    self._force_standby()
                return

            # Back off after a rejected command instead of spamming the FCU.
            if self._takeoff_backoff_until is not None and now < self._takeoff_backoff_until:
                return

            self.get_logger().info(f"Step 6: Takeoff to {self._takeoff_alt}m...")

            # CommandTOL request
            takeoff_req = CommandTOL.Request()
            takeoff_req.min_pitch = 0.0
            takeoff_req.yaw = 0.0
            takeoff_req.latitude = 0.0   # 0 = current position
            takeoff_req.longitude = 0.0
            takeoff_req.altitude = self._takeoff_alt

            self._takeoff_future = self._takeoff_cli.call_async(takeoff_req)
            return

        if not self._takeoff_future.done():
            if elapsed > self._takeoff_timeout:
                self.get_logger().error("Takeoff request timed out — no response")
                self._takeoff_future = None
                self._force_standby()
            return
        
        res2 = self._takeoff_future.result()
        self._takeoff_future = None

        if res2 is None or not res2.success:
            self.get_logger().warn(
                "Takeoff command rejected by FCU — backing off and retrying",
                throttle_duration_sec=5.0,
            )
            self._takeoff_backoff_until = (
                self.get_clock().now()
                + Duration(seconds=self._takeoff_retry_interval)
            )
            if elapsed > self._takeoff_timeout:
                self.get_logger().error("Takeoff failed - timeout")
                self._force_standby()
            return

        # Accepted: latch it so we never spam NAV_TAKEOFF again while
        # climbing (re-sends caused duplicate COMMAND_ACKs -> mavros crash).
        self._takeoff_accepted = True
        self.get_logger().info("Takeoff command accepted by FCU - monitoring climb")

        if elapsed > self._takeoff_timeout:
            self.get_logger().error(
                f"Takeoff timeout — current altitude: {self.local_pose.pose.position.z:.1f}m"
            )
            self._force_standby()
            return

    # -- Step 7: Switch to AUTO ---
    def _step_auto_mode(self, elapsed):
        self.get_logger().info("Step 7: Switching to AUTO mode...")

        if self.fcu_state.mode == "AUTO":
            self.get_logger().info("Already in AUTO mode")
            self._next_step()
            return

        if not self._auto_mode_future:
            if not self._mode_cli.wait_for_service(timeout_sec=2.0):
                if elapsed > 10.0:
                    self.get_logger().error("SetMode service unavailable")
                    self._force_standby()
                return

            mode_req = SetMode.Request()
            mode_req.base_mode = 0
            mode_req.custom_mode = "AUTO"
            self._auto_mode_future = self._mode_cli.call_async(mode_req)
            return

        if not self._auto_mode_future.done():
            if elapsed > 10:
                self.get_logger().error("Auto mode request timed out — no response")
                self._auto_mode_future = None
                self._force_standby()
            return
            
        res = self._auto_mode_future.result()
        self._auto_mode_future = None

        if res is None or not res.mode_sent:
            if elapsed > 10.0:
                self.get_logger().error("Failed to switch to AUTO")
                self._force_standby()
            return

        if self.fcu_state.mode == "AUTO":
            self.get_logger().info("AUTO mode engaged — mission is live")
            self._next_step()
        elif elapsed > 10.0:
            self.get_logger().error("AUTO mode confirmation timeout")
            self._force_standby()

    # ==================================================================
    # STATE: oda  (Obstacle Detection & Avoidance)
    # ==================================================================

    def _on_enter_oda(self, event):
        self._set_state("oda")
        self.get_logger().info("=== ODA: obstacle avoidance active ===")
        self.get_logger().info("ODA package handles obstacle detection and avoidance; handing over navigation; waiting for waypoint_reached...")

    # ==================================================================
    # STATE: landing
    # ==================================================================

    def _on_enter_landing(self, event):
        self.get_logger().info("=== LANDING: RTL + touchdown sequence ===")
        self._landing_timer_start = self.get_clock().now()
        self.landing_timer = self.create_timer(0.2, self.rtl_landing)
        self._set_state("landing")
        return 

    def rtl_landing(self):
        # elapsed is a Duration-derived float, NOT a Time – the old code
        # compared a Time against 10 and crashed with a TypeError.
        elapsed = (self.get_clock().now() - self._landing_timer_start).nanoseconds / 1e9
        self.get_logger().info("Switching to RTL mode...")

        if not self._rtl_mode_future:
            if not self._mode_cli.wait_for_service(timeout_sec=2.0):
                if elapsed > 10.0:
                    self.get_logger().error("SetMode service unavailable")
                    self._force_standby()
                return

            mode_req = SetMode.Request()
            mode_req.base_mode = 0
            mode_req.custom_mode = "RTL"
            self._rtl_mode_future = self._mode_cli.call_async(mode_req)
            return

        if not self._rtl_mode_future.done():
            if elapsed > 10.0:
                self.get_logger().error("RTL mode request timed out — no response")
                self._rtl_mode_future = None
                self._force_standby()
            return
            
        res = self._rtl_mode_future.result()
        self._rtl_mode_future = None

        if res is None or not res.mode_sent:
            if elapsed > 10.0:
                self.get_logger().error("Failed to switch to RTL")
                self._force_standby()
            return

        if self.fcu_state.mode == "RTL":
            self.get_logger().info("RTL mode engaged — mission is live")
            self.landing_timer.cancel()
            return
        elif elapsed > 10.0:
            self.get_logger().error("RTL mode confirmation timeout")
            self._force_standby()

    # ==================================================================
    # ODA → Mission resume
    # ==================================================================

    def _on_resume_mission(self, event):
        self._set_state("mission")
        self.get_logger().info("=== Resuming MISSION (from ODA) ===")

        # Re-engage AUTO via the async init step machine.  NEVER call
        # spin_until_future_complete here – this runs inside a topic
        # callback, which would deadlock the executor.
        self._auto_mode_future = None
        self._init_step = 7
        self._init_step_start_time = self.get_clock().now()
        self._init_timer.reset()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    rclpy.init()
    node = DroneNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()