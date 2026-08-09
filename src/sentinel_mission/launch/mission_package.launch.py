#!/usr/bin/env python3
"""
Launch file for the Sentinel V1 Mission package.

Launches all mission-package nodes:
  - drone_node       (state machine orchestrator)
  - mission_node     (waypoint parser & progress tracker)
  - emergency_node   (battery & heartbeat monitor)
  - start_trigger    (auto-start signal)

Prerequisites (run in separate terminals first):
  - Gazebo:   quick_sim
  - SITL:     quick_sitl
  - MAVROS:   mavros
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="sentinel_mission",
                executable="mission_node",
                name="mission_node",
                output="screen",
            ),
            Node(
                package="sentinel_mission",
                executable="emergency_node",
                name="emergency_node",
                output="screen",
            ),
            Node(
                package="sentinel_mission",
                executable="start_trigger",
                name="start_trigger",
                output="screen",
            ),
            Node(
                package="sentinel_mission",
                executable="drone_node",
                name="drone_node",
                output="screen",
            ),
        ]
    )
