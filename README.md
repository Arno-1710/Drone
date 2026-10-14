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

### A. Run the sim locally (this machine — Ubuntu 26.04, no GPU)
The full stack runs in **Docker** (Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic
+ XRCE-DDS agent), so it works even though the host OS is too new for native
Jazzy packages. PX4 is expected at `~/PX4-Autopilot`.

```bash
# One-time: allow the container to draw the Gazebo GUI
xhost +local:docker

# Build + enter the container (first run builds the image)
./docker/run.sh

# --- inside the container ---
./start_sim.sh          # boots PX4 + Gazebo + XRCE agent + your nodes
# then type into the command node:  takeoff / x 1 / y 5 / z 2
```

> Note: no NVIDIA GPU here, so Gazebo uses **software rendering** — it works,
> just not as smooth as on a GPU machine.

### B. Collaborate with the team (via GitHub)
Your custom code lives in `ros2_ws/` and is shared through GitHub. CI builds the
ROS 2 package on every push (on Ubuntu 24.04), so the whole team gets automatic
pass/fail without needing a working local sim. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git checkout main && git pull      # start of session
git checkout -b feature/my-task    # work on a branch
git add -A && git commit -m "..."  # save
git push -u origin feature/my-task # open a PR on GitHub
```

### C. Heavy components (not in this repo)
The `setup.sh` bootstrap script documents/pins the third-party stack (PX4, ROS 2,
Gazebo, XRCE-DDS agent) so every machine ends up identical. If you upgrade any of
them, update `setup.sh` and note it in [CONTRIBUTING.md](CONTRIBUTING.md).

## Notes
- This repo tracks **only your custom code** — the sim runtime lives in Docker
  (`docker/`) and PX4 lives outside the repo (`~/PX4-Autopilot`).
- Keep large binary assets (Gazebo models, maps) under **Git LFS**.
- Document any version bumps to PX4 / ROS 2 / Gazebo so all machines stay in sync.
