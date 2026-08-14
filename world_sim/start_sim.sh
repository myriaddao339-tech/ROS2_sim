#!/usr/bin/env bash
# Sentinel V1 sim – opens Gazebo and ArduPilot SITL, each in its own
# terminal window (they were too cluttered when run together).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="${ROS2_SIM_WS:-$HOME/Desktop/ROS2_sim}"

# pick an available terminal emulator
TERM_CMD=""
for t in gnome-terminal konsole xterm x-terminal-emulator; do
    if command -v "$t" >/dev/null 2>&1; then
        TERM_CMD="$t"
        break
    fi
done

if [ -z "$TERM_CMD" ]; then
    echo "No terminal emulator found (tried gnome-terminal, konsole, xterm)." >&2
    echo "Run start_gazebo.sh and start_sitl.sh manually in separate terminals." >&2
    exit 1
fi

open_terminal() {
    local script="$1"
    case "$TERM_CMD" in
        gnome-terminal)
            "$TERM_CMD" -- bash -c "bash '$script'; exec bash" &
            ;;
        konsole)
            "$TERM_CMD" -e bash -c "bash '$script'; exec bash" &
            ;;
        *)
            "$TERM_CMD" -e bash "$script" &
            ;;
    esac
}

echo "Opening Gazebo and ArduPilot SITL in separate terminals…"
open_terminal "$SCRIPT_DIR/start_gazebo.sh"
sleep 2
open_terminal "$SCRIPT_DIR/start_sitl.sh"

echo ""
echo "Once both are up, start the ROS stack:"
echo "  cd $WS && source install/setup.bash"
echo "  ros2 launch sentinel_oda oda_live_test.launch.py"
echo "  (the launch file also enables the Gazebo camera stream)"
