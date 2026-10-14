"""Position node: reads the drone's live position over ROS 2.

Subscribes to the PX4 odometry topic (relayed by the Micro XRCE-DDS agent)
and prints the current local position (x, y, z in metres).
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class PositionNode(Node):
    def __init__(self):
        super().__init__('position_node')
        # PX4 publishes odometry over uXRCE-DDS. Adjust the topic to match
        # your setup (check `ros2 topic list`).
        self.subscription = self.create_subscription(
            Odometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            10,
        )
        self.get_logger().info('position_node started, listening for odometry...')

    def odom_callback(self, msg: Odometry):
        p = msg.pose.pose.position
        self.get_logger().info(f'Position -> x: {p.x:.2f}  y: {p.y:.2f}  z: {p.z:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = PositionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
