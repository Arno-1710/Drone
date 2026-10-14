#!/usr/bin/env bash
# Launch the drone-sim Docker container with GUI (Gazebo) working on a
# Wayland host. Run this from anywhere on THIS machine.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PX4_DIR="${PX4_DIR:-$HOME/PX4-Autopilot}"

echo "==> Repo:    $REPO_DIR"
echo "==> PX4 dir: $PX4_DIR"

# --- Allow the container to use your X display ------------------------------
# On Wayland (Ubuntu default) Gazebo still needs the X11 socket (XWayland).
xhost +local:docker >/dev/null 2>&1 || echo "    (xhost failed — is Xwayland running?)"

# --- Build the image if needed ----------------------------------------------
cd "$REPO_DIR/docker"
if ! docker image inspect drone-sim:jazzy >/dev/null 2>&1; then
    echo "==> Building drone-sim:jazzy image (first run only, be patient)..."
    docker compose build
fi

# --- Launch ------------------------------------------------------------------
export PX4_DIR
echo "==> Starting container (Ctrl-D to exit, image keeps running)..."
docker compose run --rm sim
