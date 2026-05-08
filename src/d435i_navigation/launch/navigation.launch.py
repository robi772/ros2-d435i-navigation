import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    pkg_share = get_package_share_directory('d435i_navigation')
    config_dir = os.path.join(pkg_share, 'config')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock'
        ),

        Node(
            package='realsense2_camera',
            executable='realsense2_camera_node',
            name='realsense_camera',
            output='screen',
            parameters=[{
                'enable_depth': True,
                'enable_color': False,
                'enable_infra1': False,
                'enable_infra2': False,
                'enable_gyro': True,
                'enable_accel': True,
                'unite_imu_method': 2,
                'publish_tf': True,
                'use_sim_time': use_sim_time,
            }]
        ),

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

        Node(
            package='d435i_navigation',
            executable='imu_yaw_to_odom',
            name='imu_yaw_to_odom',
            output='screen'
        ),

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

        Node(
            package='nav2_bringup',
            executable='bringup_launch.py',
            name='nav2_bringup',
            output='screen',
            parameters=[
                os.path.join(config_dir, 'nav2_params.yaml'),
                {'use_sim_time': use_sim_time}
            ]
        ),
    ])
