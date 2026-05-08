FROM osrf/ros:humble-desktop

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-colcon-common-extensions \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    ros-humble-realsense2-camera \
    ros-humble-depthimage-to-laserscan \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY src /ws/src
COPY config /ws/config
COPY launch /ws/launch

RUN source /opt/ros/humble/setup.bash && colcon build --symlink-install

CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && source /ws/install/setup.bash && ros2 launch d435i_navigation navigation.launch.py"]
