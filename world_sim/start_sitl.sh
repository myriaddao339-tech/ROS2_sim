#!/usr/bin/env bash
# Sentinel V1 sim – launch ArduPilot SITL with the Gazebo JSON backend.
# Run in its own terminal (or use start_sim.sh, which opens one).
#
# The extra --out=udp:127.0.0.1:14550 is for MAVROS (the ROS launch file
# listens on that port with fcu_url=udp://:14550@).

set -euo pipefail

ARDUPILOT_DIR="${ARDUPILOT_HOME:-$HOME/ardupilot}"
cd "$ARDUPILOT_DIR/Tools/autotest"

exec sim_vehicle.py \
    -v ArduCopter \
    -f gazebo-iris \
    --model JSON \
    --console \
    --out=127.0.0.1:14555 \
    --out=192.168.125.89:14550 \
    --out=udp:127.0.0.1:14550
