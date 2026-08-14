#!/usr/bin/env python3
"""
oda_live_test.launch.py – One-shot launch for a live ODA test.

Starts:
  - MAVROS (APM config)    – FCU bridge (SITL UDP or real USB telemetry)
  - mission_node           – waypoint parser & progress tracker
  - emergency_node         – battery + heartbeat watchdog
  - start_trigger          – auto-start signal for the drone node
  - drone_node             – mission state machine
  - depth_node             – Depth Anything V2 on the UDP camera stream
  - detection_node         – obstacle detection + block segmentation

This file also enables the Gazebo camera stream: GstCameraPlugin only
starts pushing MPEG-TS to udp://127.0.0.1:5600 after it receives an
enable_streaming=true message, so an action here sends it (with retries)
right after everything is up.  Disable with enable_camera_stream:=false
(useful for real-drone runs where Gazebo is not running).

NOT started (launched separately, per user's choice):
  - Gazebo:          gz sim -v4 -r obstacle_course.sdf   (world_sim/worlds/)
  - ArduPilot SITL:  sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON
                     --console --out=127.0.0.1:14555
                     --out=192.168.125.89:14550
                     --out=udp:127.0.0.1:14550    <-- extra --out for MAVROS

MAVROS defaults to fcu_url=udp://:14550@ (listen on UDP 14550), so SITL
must stream MAVLink there (see the extra --out above).  For the real
drone over USB telemetry, override it:
    ros2 launch sentinel_oda oda_live_test.launch.py fcu_url:=/dev/ttyACM0:57600
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # default mission: the 2-waypoint obstacle course plan shipped with
    # sentinel_mission (missions/obstacle_course.plan)
    _default_mission = os.path.join(
        get_package_share_directory("sentinel_mission"),
        "missions", "obstacle_course.plan",
    )

    # ---- launch arguments ----
    fcu_url = LaunchConfiguration("fcu_url")
    gcs_url = LaunchConfiguration("gcs_url")
    mission_file = LaunchConfiguration("mission_file")
    camera_stream_topic = LaunchConfiguration("camera_stream_topic")
    enable_camera_stream = LaunchConfiguration("enable_camera_stream")

    args = [
        DeclareLaunchArgument(
            "fcu_url",
            default_value="udp://:14550@",
            description="MAVROS FCU URL (SITL: udp://:14550@, real drone: /dev/ttyACM0:57600)",
        ),
        DeclareLaunchArgument(
            "gcs_url",
            default_value="",
            description="Optional GCS URL for MAVROS",
        ),
        DeclareLaunchArgument(
            "mission_file",
            default_value=_default_mission,
            description="Path to a QGC .plan file (default: missions/obstacle_course.plan)",
        ),
        DeclareLaunchArgument(
            "camera_stream_topic",
            default_value=(
                "/world/obstacle_course/model/sentinel_f450/link/camera_link/"
                "sensor/camera/image/enable_streaming"
            ),
            description="Gazebo topic that turns the GstCameraPlugin stream on",
        ),
        DeclareLaunchArgument(
            "enable_camera_stream",
            default_value="true",
            description="Send the enable_streaming message to the Gazebo camera (false for real-drone runs)",
        ),
    ]

    # ---- MAVROS (APM pluginlist/config, but launched directly so it can
    #      respawn: mavros 2.x can crash with `std::future_error: Promise
    #      already satisfied` under CPU contention; apm.launch's
    #      respawn_mavros arg is declared but NOT wired up in this build,
    #      so we set respawn ourselves.) ----
    mavros_share = get_package_share_directory("mavros")
    mavros_node = Node(
        package="mavros",
        executable="mavros_node",
        namespace="mavros",
        output="screen",
        respawn=True,
        respawn_delay=3.0,
        parameters=[
            {
                "fcu_url": fcu_url,
                "gcs_url": gcs_url,
                "tgt_system": 1,
                "tgt_component": 1,
                "fcu_protocol": "v2.0",
            },
            os.path.join(mavros_share, "launch", "apm_pluginlists.yaml"),
            os.path.join(mavros_share, "launch", "apm_config.yaml"),
            {
                # Same denylist as apm_pluginlists.yaml, plus home_position.
                # mavros's home_position plugin polls MAV_CMD_GET_HOME_POSITION
                # 10 s after every FCU connect; ArduPilot ACKs that command
                # TWICE, and mavros 2.x aborts on the duplicate ACK
                # (std::future_error: Promise already satisfied).  We never
                # use /mavros/home_position, so the plugin is dropped entirely.
                # Listed last so it overrides the yaml files above.
                "plugin_denylist": [
                    # common
                    "actuator_control",
                    "ftp",
                    "hil",
                    # extras
                    "altitude",
                    "debug_value",
                    "image_pub",
                    "px4flow",
                    "vibration",
                    "vision_speed_estimate",
                    "wheel_odometry",
                    # project: unused, and its 10 s GET_HOME_POSITION poll
                    # triggers the mavros duplicate-ACK crash
                    "home_position",
                ],
            },
        ],
    )

    # ---- mission package nodes (same set as mission_package.launch.py) ----
    mission_node = Node(
        package="sentinel_mission",
        executable="mission_node",
        name="mission_node",
        #output="screen",
        parameters=[{"mission_file_path": mission_file}],
    )
    emergency_node = Node(
        package="sentinel_mission",
        executable="emergency_node",
        name="emergency_node",
        #output="screen",
    )
    start_trigger = Node(
        package="sentinel_mission",
        executable="start_trigger",
        name="start_trigger",
        #output="screen",
    )
    drone_node = Node(
        package="sentinel_mission",
        executable="drone_node",
        name="drone_node",
        output="screen",
    )

    # ---- depth node: reads the drone/Gazebo camera stream (MPEG-TS UDP) ----
    depth_node = Node(
        package="sentinel_oda",
        executable="depth_node",
        name="depth_node",
        output="screen",
        parameters=[
            {
                "video_source": "udp",      # Gazebo GstCameraPlugin / drone relay
                "udp_port": 5600,           # camera streams here (see world_sim model)
                "inference_rate": 20.0,     # timer cap; CPU tops out ~5-8 fps @ 308px
                "model_input_size": 308,    # window size kept per user request
                "device": "cpu",            # switch to "cuda" once the GPU is safe
                "show_preview": True,       # pop-up depth map window (TURBO colormap)
            }
        ],
    )

    # ---- detection node: OV5647-style camera params ----
    detection_node = Node(
        package="sentinel_oda",
        executable="detection_node",
        name="detection_node",
        output="screen",
        parameters=[
            {
                "camera_hfov_deg": 53.5,    # user camera spec (OV5647 setup)
                "drone_width": 0.363,
                "drone_height": 0.363,
                "box_margin": 0.2,
                "confirm_frames": 10,       # one-way validation, no clearing
                "mission_obstacle_threshold": 10.0,
                "oda_obstacle_threshold": 0.8,
                "depth_margin": 0.5,
            }
        ],
    )

    # ---- enable the Gazebo camera stream ----------------
    # GstCameraPlugin only starts pushing MPEG-TS to udp://127.0.0.1:5600
    # after it receives enable_streaming=true (ardupilot_gazebo behaviour).
    # Retried for up to 30 s so it tolerates slow Gazebo startup; harmless
    # if Gazebo is not running (prints a warning and moves on).
    enable_camera_stream_cmd = ExecuteProcess(
        cmd=[
            "bash",
            "-c",
            'for i in $(seq 1 30); do '
            'if gz topic -t "$1" -m gz.msgs.Boolean -p "data: 1" 2>/dev/null; then '
            'echo "[oda_live_test] Gazebo camera streaming enabled on udp://127.0.0.1:5600"; '
            'exit 0; fi; '
            'sleep 1; done; '
            'echo "[oda_live_test] WARNING: could not enable the Gazebo camera stream " '
            '"(is gz sim running?)" >&2; exit 0',
            "oda_camera_enable",
            camera_stream_topic,
        ],
        output="screen",
        condition=IfCondition(enable_camera_stream),
    )

    return LaunchDescription(
        args
        + [
            mavros_node,
            enable_camera_stream_cmd,
            mission_node,
            emergency_node,
            start_trigger,
            drone_node,
            depth_node,
            detection_node,
        ]
    )
