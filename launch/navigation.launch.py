from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation clock'
        ),

        # ── RealSense D435i driver ────────────────────────────────────────────
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
                'unite_imu_method': 2,   # linear interpolation
                'publish_tf': True,
                'use_sim_time': use_sim_time,
            }]
        ),

        # ── Depth → LaserScan ────────────────────────────────────────────────
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
            parameters=['/ws/config/depth_to_scan.yaml']
        ),

        # ── IMU → minimal odometry ───────────────────────────────────────────
        Node(
            package='d435i_navigation',
            executable='imu_yaw_to_odom',
            name='imu_yaw_to_odom',
            output='screen'
        ),

        # ── SLAM Toolbox ─────────────────────────────────────────────────────
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                '/ws/config/slam_toolbox.yaml',
                {'use_sim_time': use_sim_time}
            ]
        ),

        # ── Nav2 bringup ──────────────────────────────────────────────────────
        Node(
            package='nav2_bringup',
            executable='bringup_launch.py',
            name='nav2_bringup',
            output='screen',
            parameters=[
                '/ws/config/nav2_params.yaml',
                {'use_sim_time': use_sim_time}
            ]
        ),
    ])
