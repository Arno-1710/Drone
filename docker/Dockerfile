# Drone Sim runtime: Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic + XRCE-DDS agent
# Runs the full stack in a container so it works even on Ubuntu 26.04 hosts.
FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive

# --- OSRF Gazebo repo (gz-harmonic is NOT in the Ubuntu/ROS repos) ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget lsb-release ca-certificates gnupg \
    && wget -q https://packages.osrfoundation.org/gazebo.gpg \
        -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
        > /etc/apt/sources.list.d/pkgs-osrf-archive-keyring.list \
    && rm -rf /var/lib/apt/lists/*

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

# --- Micro XRCE-DDS Agent v3.0.2 (connects PX4 <-> ROS 2) -------------------
# Not packaged for Jazzy in apt; build from source. v3 matches PX4's
# UXRCE_DDS_CLIENT_USE_DDS_V3 client (see boards/px4/sitl/default.px4board).
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake git ca-certificates \
        ros-jazzy-rosidl-default-generators ros-jazzy-rosidl-default-runtime \
        libasio-dev libtinyxml2-dev \
    && git clone -q -b v3.0.2 --depth 1 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git \
    && cmake -S Micro-XRCE-DDS-Agent -B Micro-XRCE-DDS-Agent/build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build Micro-XRCE-DDS-Agent/build -j"$(nproc)" \
    && cmake --install Micro-XRCE-DDS-Agent/build \
    && rm -rf Micro-XRCE-DDS-Agent /var/lib/apt/lists/*

WORKDIR /workspace

# Source ROS 2 + mount-point for the repos (overridden by docker-compose)
CMD ["bash", "-lc", "source /opt/ros/jazzy/setup.bash && exec bash"]
