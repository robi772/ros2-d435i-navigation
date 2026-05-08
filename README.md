# ROS2 D435i Navigation

Dockerized **ROS2 Kilted Kaiju** application for navigation using Intel RealSense D435i.

## Features
- RealSense D435i camera driver integration
- Depth image to LaserScan conversion
- SLAM with slam_toolbox
- Nav2 stack for autonomous navigation
- Dockerized, runs on Ubuntu 24.04 Noble base

## Structure
```
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── src/d435i_navigation/
│   ├── package.xml
│   ├── setup.py
│   └── d435i_navigation/
│       ├── __init__.py
│       └── imu_yaw_to_odom.py
├── config/
│   ├── depth_to_scan.yaml
│   ├── slam_toolbox.yaml
│   └── nav2_params.yaml
└── launch/
    └── navigation.launch.py
```

## Quick Start
```bash
git clone https://github.com/robi772/ros2-d435i-navigation.git
cd ros2-d435i-navigation

# Allow Docker to use X11 display (for RViz2)
xhost +local:docker

docker compose up --build
```

## Requirements
- Docker & Docker Compose v2
- Intel RealSense D435i connected via USB3
- Host: Linux (Ubuntu 22.04 / 24.04 recommended)

## Notes
- Base image: `osrf/ros:kilted-desktop` (Ubuntu 24.04 Noble)
- Uses `rmw_fastrtps_cpp` middleware
- IMU-based yaw odometry is minimal — integrate a wheel encoder or VIO for production use
- Topic names follow `realsense2_camera` defaults
