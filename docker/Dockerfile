FROM osrf/ros:kilted-desktop

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# RealSense SDK + udev szabalyok + ROS2 csomagok
RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    python3-pip \
    udev \
    ros-kilted-navigation2 \
    ros-kilted-nav2-bringup \
    ros-kilted-slam-toolbox \
    ros-kilted-realsense2-camera \
    ros-kilted-depthimage-to-laserscan \
    ros-kilted-rviz2 \
    ros-kilted-tf2-ros \
    && rm -rf /var/lib/apt/lists/*

# librealsense udev szabalyok masolasa a kontenerbe
RUN mkdir -p /etc/udev/rules.d && \
    find /opt/ros/kilted -name '99-realsense-libusb.rules' \
         -exec cp {} /etc/udev/rules.d/ \; 2>/dev/null || true

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
