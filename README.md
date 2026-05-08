# ROS2 D435i Navigation

Dockerized ROS2 Humble application for navigation using Intel RealSense D435i.

## Features
- RealSense D435i camera driver integration
- Depth image to LaserScan conversion
- SLAM with slam_toolbox
- Nav2 stack for autonomous navigation
- Example launch files for Docker deployment

## Structure
- `docker/` - Dockerfile and compose config
- `src/d435i_navigation/` - ROS2 Python package
- `config/` - Nav2, SLAM, and sensor configs
- `launch/` - Launch files

## Quick start
```bash
git clone https://github.com/robi772/ros2-d435i-navigation.git
cd ros2-d435i-navigation
docker compose up --build
```

## Notes
- Requires access to `/dev/video*` and USB devices.
- Tuned for ROS2 Humble on Ubuntu 22.04 base image.
- Topic remaps assume `realsense2_camera` default topic names.
