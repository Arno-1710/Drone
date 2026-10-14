#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Start the full drone sim stack INSIDE the container.
#
# Runs, in order:
#   1. PX4 SITL + Gazebo (x500 quadcopter)   -> spawns drone in the 3D world
#   2. Micro XRCE-DDS Agent                  -> bridges PX4 <-> ROS 2
#   3. Your drone_control nodes              -> read position / send commands
#
# Usage (inside the container):
#   ./start_sim.sh              # full stack
#   ./start_sim.sh --no-nodes   # sim + bridge only, no your-nodes
# ---------------------------------------------------------------------------
set -euo pipefail

PX4_DIR=/workspace/PX4-Autopilot
DRONE_WS=/workspace/drone-sim/ros2_ws
ROS_SETUP=/opt/ros/jazzy/setup.bash

source "$ROS_SETUP"

echo "==> [1/3] Launching PX4 SITL + Gazebo (x500)..."
# PX4's own gz_x500 target spawns the drone AND the Gazebo GUI.
(cd "$PX4_DIR" && make px4_sitl gz_x500) &
PX4_PID=$!

echo "==> [2/3] Starting Micro XRCE-DDS Agent (udp4 port 8888)..."
sleep 5   # give PX4 a moment to come up
# v3.0.2 installs the binary as MicroXRCEAgent (v2 called it micro-xrce-dds-agent)
if command -v MicroXRCEAgent >/dev/null 2>&1; then
    MicroXRCEAgent udp4 -p 8888 &
elif command -v micro-xrce-dds-agent >/dev/null 2>&1; then
    micro-xrce-dds-agent udp4 -p 8888 &
else
    echo "    ERROR: XRCE agent binary not found"; exit 1
fi
AGENT_PID=$!

# --- Your ROS 2 nodes --------------------------------------------------------
if [[ "${1:-}" != "--no-nodes" ]]; then
    echo "==> [3/3] Building + launching drone_control nodes..."
    (cd "$DRONE_WS" && colcon build && source install/setup.bash) || \
        echo "    (colcon build failed — check your package)"
    sleep 2
    ros2 launch drone_control drone_control_launch.py &
    NODES_PID=$!
else
    echo "==> [3/3] Skipping nodes (--no-nodes)."
fi

echo ""
echo "=========================================================="
echo "  Sim stack is up."
echo "  - Gazebo 3D view should be open on your desktop."
echo "  - Position + command nodes are running."
echo "  - Type into command_node to fly:  takeoff / x 1 / y 5 / z 2"
echo "  Press Ctrl-C to tear everything down."
echo "=========================================================="

trap 'echo "Shutting down..."; kill 0 2>/dev/null; wait 2>/dev/null' INT TERM
wait
