import math

import rclpy
from geometry_msgs.msg import Quaternion, TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf2_ros import TransformBroadcaster


class ImuYawToOdom(Node):
    def __init__(self):
        super().__init__('imu_yaw_to_odom')
        self.publisher_ = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.subscription = self.create_subscription(Imu, '/camera/imu', self.imu_callback, 10)
        self.last_stamp = None
        self.yaw = 0.0

    def imu_callback(self, msg: Imu):
        if self.last_stamp is not None:
            dt = (msg.header.stamp.sec - self.last_stamp.sec) + \
                 (msg.header.stamp.nanosec - self.last_stamp.nanosec) / 1e9
            self.yaw += msg.angular_velocity.z * dt
        self.last_stamp = msg.header.stamp

        odom = Odometry()
        odom.header = msg.header
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.orientation = self.yaw_to_quaternion(self.yaw)
        self.publisher_.publish(odom)

        transform = TransformStamped()
        transform.header = odom.header
        transform.child_frame_id = odom.child_frame_id
        transform.transform.rotation = odom.pose.pose.orientation
        self.tf_broadcaster.sendTransform(transform)

    @staticmethod
    def yaw_to_quaternion(yaw: float) -> Quaternion:
        q = Quaternion()
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q


def main(args=None):
    rclpy.init(args=args)
    node = ImuYawToOdom()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
