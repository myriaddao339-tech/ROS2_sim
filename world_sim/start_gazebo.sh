#!/usr/bin/env bash
# Sentinel V1 sim – launch the obstacle course world in Gazebo.
# Run in its own terminal (or use start_sim.sh, which opens one).

set -euo pipefail

WS="${ROS2_SIM_WS:-$HOME/Desktop/ROS2_sim}"

export GZ_SIM_RESOURCE_PATH="$WS/world_sim/models:$WS/world_sim/worlds:$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/src/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH:-}"

cd "$WS/world_sim/worlds"

# Closing the Gazebo window can leave an orphaned `gz sim -r -s` server
# behind.  Those pile up (one per run), each eats ~100% CPU, holds the
# SITL plugin ports (9002/9003) and scrambles Gazebo's transport, which
# makes the NEXT launch show an empty world with 0 entities.  Kill any
# leftovers from previous runs before starting a fresh one.
pkill -f "gz sim .*obstacle_course" 2>/dev/null || true
sleep 1

# No `exec`: we want to run a cleanup trap after the GUI exits, so the
# server child process is always reaped (window-close does not reliably
# shut it down).
gz sim -v4 -r obstacle_course.sdf &
GZSIM_PID=$!

cleanup() {
    kill "$GZSIM_PID" 2>/dev/null || true
    pkill -f "gz sim .*obstacle_course" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

wait "$GZSIM_PID" || true
