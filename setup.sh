#!/usr/bin/env bash
# =============================================================================
# Drone Simulation - Environment Bootstrap
#
# Installs / pins the heavy third-party stack (PX4, XRCE-DDS agent, Gazebo)
# that is NOT stored in this repo, so every machine ends up identical.
#
# Your CUSTOM code lives in ros2_ws/ and IS tracked by git.
# =============================================================================
set -euo pipefail

echo "==> Drone sim environment bootstrap"
echo "    (Review each step; some require sudo or network access.)"

# --- 1. ROS 2 Jazzy ---------------------------------------------------------
# Assumes Ubuntu 24.04 (Noble). Follow the official guide if not installed:
#   https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
echo "==> Checking for ROS 2 Jazzy..."
if ! command -v ros2 >/dev/null 2>&1; then
    echo "    ROS 2 not found. Install it first:"
    echo "      sudo apt update && sudo apt install ros-jazzy-desktop"
    echo "    (plus ros-dev-tools: sudo apt install ros-dev-tools)"
else
    echo "    ROS 2 found: $(ros2 --version 2>/dev/null || echo 'installed')"
fi

# --- 2. Build tools ---------------------------------------------------------
echo "==> Ensuring build tools are present..."
sudo apt-get update -qq
sudo apt-get install -y -qq git cmake ninja-build build-essential \
    python3-venv python3-pip pipx

# --- 3. PX4-Autopilot -------------------------------------------------------
PX4_DIR="$HOME/PX4-Autopilot"
if [ ! -d "$PX4_DIR" ]; then
    echo "==> Cloning PX4-Autopilot (this is large)..."
    git clone https://github.com/PX4/PX4-Autopilot.git --recursive
    cd "$PX4_DIR"
    # Pin a known-good tag here so everyone matches, e.g.:
    #   git checkout v1.15.2 && git submodule update --init --recursive
else
    echo "==> PX4-Autopilot already present at $PX4_DIR"
fi

# --- 4. Micro XRCE-DDS Agent -----------------------------------------------
if ! command -v micro-xrce-dds-agent >/dev/null 2>&1; then
    echo "==> Micro XRCE-DDS Agent not found."
    echo "    Install per: https://github.com/eProsima/Micro-XRCE-DDS-Agent"
    echo "    (typically: sudo apt install ros-jazzy-micro-xrce-dds-agent)"
else
    echo "    XRCE-DDS agent found."
fi

# --- 5. Gazebo (Harmonic) ---------------------------------------------------
if ! command -v gz >/dev/null 2>&1; then
    echo "==> Gazebo (gz) not found. Install Gazebo Harmonic:"
    echo "      sudo apt-get install gz-harmonic"
else
    echo "    Gazebo found: $(gz sim --versions 2>/dev/null | head -1)"
fi

# --- 6. Build the custom ROS 2 workspace -----------------------------------
echo "==> Building ros2_ws (colcon)..."
cd "$(dirname "$0")/ros2_ws"
if command -v colcon >/dev/null 2>&1; then
    colcon build
    echo "    Build complete. To use it:"
    echo "      source install/setup.bash"
    echo "      ros2 launch drone_control drone_control_launch.py"
else
    echo "    colcon not found. Install: sudo apt install python3-colcon-common-extensions"
fi

echo "==> Bootstrap finished."
