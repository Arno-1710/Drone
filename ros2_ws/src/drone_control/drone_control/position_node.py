"""Position node: reads the drone's live position over ROS 2.

Subscribes to PX4's VehicleOdometry (relayed by the Micro XRCE-DDS agent)
and prints the current local position in metres.

Note: PX4 reports position in the NED frame (North-East-Down):
    x = North, y = East, z = Down (so altitude is NEGATIVE z).
"""

import rclpy
from rclpy.node import Node
from px4_msgs.msg import VehicleOdometry


class PositionNode(Node):
    def __init__(self):
        super().__init__('position_node')
        # PX4 publishes odometry over uXRCE-DDS on this topic.
        self.subscription = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.odom_callback,
            10,
        )
        self.get_logger().info('position_node started, listening for VehicleOdometry...')

    def odom_callback(self, msg: VehicleOdometry):
        # position is float32[3] in NED metres: [north, east, down]
        x, y, z = msg.position
        # altitude = -down
        self.get_logger().info(
            f'NED x: {x:.2f}  y: {y:.2f}  z: {z:.2f}  (alt {-z:.2f} m)'
        )


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
