#!/usr/bin/env python3
"""
oda_live_test.launch.py – One-shot launch for a live ODA test.

Starts:
  - MAVROS (APM config)    – FCU bridge (SITL UDP or real USB telemetry)
  - mission_node           – waypoint parser & progress tracker
  - emergency_node         – battery + heartbeat watchdog
  - start_trigger          – auto-start signal for the drone node
  - drone_node             – mission state machine
  - oda_maneuvers          – drone-side scout (GUIDED switch + yaw sweep)
  - depth_node             – Depth Anything V2 on the UDP camera stream,
                             or native Gazebo depth (depth_source:=gazebo_depth)
  - detection_node         – obstacle detection + block segmentation
  - inner_map              – drone-side planner: tile grid + A* safe path
  - guided                 – drone-side pilot: executes the safe path

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
        "missions", "first_mission.plan",
    )

    # ---- launch arguments ----
    fcu_url = LaunchConfiguration("fcu_url")
    gcs_url = LaunchConfiguration("gcs_url")
    mission_file = LaunchConfiguration("mission_file")
    camera_stream_topic = LaunchConfiguration("camera_stream_topic")
    enable_camera_stream = LaunchConfiguration("enable_camera_stream")
    depth_source = LaunchConfiguration("depth_source")

    args = [
        DeclareLaunchArgument(
            "fcu_url",
            default_value="udp://:14555@",
            description="MAVROS FCU URL (SITL: udp://:14555@, real drone: /dev/serial0:57600)",
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
            "depth_source",
            default_value="udp",
            description=(
                "Depth input for depth_node: 'udp' (ML pipeline on the camera "
                "stream), 'webcam' (PC camera), or 'gazebo_depth' (native gz "
                "depth camera – exact metric depth, no ML model)"
            ),
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
        #output="screen",
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
                    # mavros 2.14.0 param plugin crashes on ArduPilot's
                    # double param-ACK (std::future_error: Promise already
                    # satisfied, issue #2159; fixed only in 2.15.x, which
                    # has no jammy binaries).  RTL_ALT_M is preconfigured
                    # in mav.parm / mav_0_1.parm instead of being raised
                    # at runtime; drone_node skips the raise when this
                    # service is absent.
                    "param",
                ],
            },
        ],
        # ArduPilot streams unsolicited param values that mavros.param logs
        # as INFO on every change ("PR: got an unsolicited param value ..."),
        # drowning the terminal.  Raise only that logger to WARN.
        arguments=["--ros-args", "--log-level", "mavros.param:=warn"],
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

    return LaunchDescription(
        args
        + [
            mavros_node,
            mission_node,
            emergency_node,
            start_trigger,
            drone_node,
        ]
    )
