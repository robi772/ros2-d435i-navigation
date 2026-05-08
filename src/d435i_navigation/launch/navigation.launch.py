import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    launch_rviz = LaunchConfiguration('launch_rviz')
    pkg_share = get_package_share_directory('d435i_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    config_dir = os.path.join(pkg_share, 'config')
    rviz_config = os.path.join(pkg_share, 'config', 'nav2_default.rviz')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument(
            'launch_rviz',
            default_value='true',
            description='Inditsa-e az RViz2-t'
        ),

        # RealSense D435i driver
        # unite_imu_method=1 (copy) stabilabb mint 2 (interpolate) frame timeout ellen
        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            name='realsense_camera',
            output='screen',
            parameters=[{
                'enable_depth': True,
                'enable_color': True,
                'enable_infra1': False,
                'enable_infra2': False,
                'enable_gyro': True,
                'enable_accel': True,
                'unite_imu_method': 1,        # copy: stabilabb mint interpolate
                'publish_tf': True,
                'use_sim_time': use_sim_time,
                'depth_fps': 15,              # 30->15 FPS: csokkenti USB bandwidth-et
                'color_fps': 15,
                'gyro_fps': 200,
                'accel_fps': 63,
            }]
        ),

        # Depth -> LaserScan
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depth_to_scan',
            output='screen',
            remappings=[
                ('depth', '/camera/depth/image_rect_raw'),
                ('depth_camera_info', '/camera/depth/camera_info'),
                ('scan', '/scan'),
            ],
            parameters=[os.path.join(config_dir, 'depth_to_scan.yaml')]
        ),

        # IMU -> minimal odometry
        Node(
            package='d435i_navigation',
            executable='imu_yaw_to_odom',
            name='imu_yaw_to_odom',
            output='screen'
        ),

        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                os.path.join(config_dir, 'slam_toolbox.yaml'),
                {'use_sim_time': use_sim_time}
            ]
        ),

        # Nav2 bringup
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
            ),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'params_file': os.path.join(config_dir, 'nav2_params.yaml'),
            }.items()
        ),

        # RViz2
        Node(
            condition=IfCondition(launch_rviz),
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config],
        ),
    ])
