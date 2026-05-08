FROM osrf/ros:kilted-desktop

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# NVIDIA OpenGL support (RViz2-hoz)
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute
ENV __NV_PRIME_RENDER_OFFLOAD=1
ENV __GLX_VENDOR_LIBRARY_NAME=nvidia

RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    udev \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    ros-kilted-navigation2 \
    ros-kilted-nav2-bringup \
    ros-kilted-slam-toolbox \
    ros-kilted-realsense2-camera \
    ros-kilted-depthimage-to-laserscan \
    ros-kilted-rviz2 \
    ros-kilted-tf2-ros \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY src /ws/src
COPY config /ws/config
COPY launch /ws/launch

RUN source /opt/ros/kilted/setup.bash \
    && colcon build --symlink-install

CMD ["bash", "-c", \
    "source /opt/ros/kilted/setup.bash && \
     source /ws/install/setup.bash && \
     ros2 launch d435i_navigation navigation.launch.py"]
