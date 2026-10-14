# Drone Simulation Pipeline

A full drone simulation stack on Ubuntu: **ROS 2 (Jazzy) + PX4 + Micro XRCE-DDS Agent + Gazebo**.

```
┌────────────┐   XRCE-DDS   ┌─────────┐   MAVLink   ┌────────────┐
│   PX4      │◄────────────►│  Agent  │◄───────────►│  Gazebo    │
│ (autopilot)│              │ (bridge)│             │ (physics)  │
└─────┬──────┘              └─────────┘             └────────────┘
      │ uXRCE-DDS
      ▼
┌────────────┐
│  ROS 2     │  ← your Python nodes live here
│  (Jazzy)   │
└────────────┘
```

## What works
- Simulated drone takes off and lands
- A Python node reads the drone's live position over ROS 2
- Fly the drone with custom commands: `x 1`, `y 5`, `z 2`

## Repository layout
```
drone-sim/
├── setup.sh                  # one-time environment bootstrap (see below)
├── ros2_ws/
│   └── src/
│       └── drone_control/    # custom ROS 2 Python package
│           ├── drone_control/
│           │   ├── position_node.py   # subscribes to drone pose
│           │   └── command_node.py    # sends fly commands
│           ├── launch/
│           ├── package.xml
│           ├── setup.py
│           └── setup.cfg
└── README.md
```

## Prerequisites (Ubuntu 24.04)
- ROS 2 Jazzy
- PX4-Autopilot (source, with Gazebo Harmonic tools)
- Micro XRCE-DDS Agent
- Gazebo (Harmonic)

> The heavy third-party components (PX4, ROS 2, Gazebo, XRCE agent) are **not**
> stored in this repo. `setup.sh` installs/pins them so everyone gets the same
> environment.

## Quick start
```bash
# 1. Build the environment (once)
./setup.sh

# 2. Start the sim stack (PX4 + Gazebo + XRCE agent)
#    (see setup.sh output for the exact launch commands)

# 3. Build your ROS 2 workspace
cd ros2_ws
colcon build
source install/setup.bash

# 4. Run your nodes
ros2 run drone_control position_node
ros2 run drone_control command_node
```

## Collaboration
- Push/pull via GitHub (private repo).
- Keep large binary assets (Gazebo models, maps) under **Git LFS**.
- Document any version bumps to PX4 / ROS 2 / Gazebo here so both machines stay in sync.
