# Contributing

This project is shared by the team via GitHub. Everyone works on their own
machine (the simulation stack — PX4 / ROS 2 / Gazebo) runs locally; **this repo
holds only the custom ROS 2 code**.

## Golden rules
1. **Never commit build artifacts** — `build/`, `install/`, `log/` are gitignored.
2. **Pull before you start, push before you stop.**
3. **Work on a branch**, not directly on `main`.
4. Keep commits small and descriptive.

## Everyday workflow
```bash
# Start of session — get latest
git checkout main
git pull

# Start a feature branch
git checkout -b feature/your-task-name

# ... edit files ...

# Save your work
git add -A
git commit -m "Add: short description of change"

# Share it
git push -u origin feature/your-task-name
```

## Team review via Pull Request
1. Push your branch (above).
2. On GitHub, open a **Pull Request** from your branch → `main`.
3. A teammate reviews; **CI must pass** (it builds the ROS 2 package automatically).
4. Merge into `main`, then clean up:
   ```bash
   git checkout main
   git pull
   git branch -d feature/your-task-name
   ```

## If CI fails
CI builds the package on Ubuntu 24.04 + ROS 2 Jazzy (the same version we use).
- A **build** failure means a syntax/import error — fix locally, push again.
- A **lint** failure means style issues — run `flake8` locally before pushing.

## Pinning the stack
The heavy components (PX4, ROS 2, Gazebo, XRCE-DDS agent) are **not** in this
repo. If you upgrade any of them, update `setup.sh` **and** note it here so
everyone stays in sync:

| Component | Version | Notes |
| :--- | :--- | :--- |
| ROS 2 | Jazzy | Ubuntu 24.04 |
| PX4 | _TBD_ | set in setup.sh |
| Gazebo | _TBD_ | set in setup.sh |
