# Drone Sim runtime: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + XRCE-DDS agent
# Runs the full stack in a container so it works even on Ubuntu 26.04 hosts.
FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive

# Gazebo Harmonic + ROS<->Gazebo bridge + build tools + PX4 deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        gz-harmonic \
        ros-jazzy-ros-gz \
        ros-jazzy-ros-gz-bridge \
        ros-jazzy-geometry-msgs \
        ros-jazzy-nav-msgs \
        python3-colcon-common-extensions \
        python3-pip \
        git \
        wget \
        lsb-release \
        ca-certificates \
        vim \
    && rm -rf /var/lib/apt/lists/*

# Micro XRCE-DDS Agent (connects PX4 <-> ROS 2)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-jazzy-micro-xrce-dds-agent \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Source ROS 2 + mount-point for the repos (overridden by docker-compose)
CMD ["bash", "-lc", "source /opt/ros/jazzy/setup.bash && exec bash"]
