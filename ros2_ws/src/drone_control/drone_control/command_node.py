"""Command node: fly the drone with simple keyboard commands.

Type commands like:
    x 1      -> move 1 m forward  (relative)
    y 5      -> move 5 m left     (relative)
    z 2      -> climb 2 m         (relative)
    takeoff
    land
    hold

Publishes position setpoints to PX4 over ROS 2 (via the XRCE-DDS agent).
"""

import sys

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

# Simple in-memory target; starts at origin.
TARGET = {'x': 0.0, 'y': 0.0, 'z': 0.0}


class CommandNode(Node):
    def __init__(self):
        super().__init__('command_node')
        # PX4 accepts position setpoints on this uXRCE-DDS topic.
        # Adjust to your setup (check `ros2 topic list`).
        self.pub = self.create_publisher(
            PoseStamped, '/fmu/in/vehicle_local_position_setpoint', 10
        )
        self.timer = self.create_timer(0.1, self.publish_setpoint)  # 10 Hz
        self.get_logger().info(
            'command_node ready. Commands: x <m>, y <m>, z <m>, takeoff, land, hold'
        )

    def publish_setpoint(self):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = TARGET['x']
        msg.pose.position.y = TARGET['y']
        msg.pose.position.z = TARGET['z']
        msg.pose.orientation.w = 1.0
        self.pub.publish(msg)

    def handle(self, line: str):
        parts = line.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()
        try:
            if cmd in ('x', 'y', 'z') and len(parts) == 2:
                delta = float(parts[1])
                TARGET[cmd] += delta
                self.get_logger().info(
                    f'{cmd} += {delta:.2f} -> target ({TARGET["x"]:.2f}, '
                    f'{TARGET["y"]:.2f}, {TARGET["z"]:.2f})'
                )
            elif cmd == 'takeoff':
                TARGET['z'] = 2.0
                self.get_logger().info('Takeoff -> z = 2.0 m')
            elif cmd == 'land':
                TARGET['z'] = 0.0
                self.get_logger().info('Land -> z = 0.0 m')
            elif cmd == 'hold':
                self.get_logger().info(
                    f'Hold at ({TARGET["x"]:.2f}, {TARGET["y"]:.2f}, {TARGET["z"]:.2f})'
                )
            else:
                self.get_logger().warn(f'Unknown command: {line!r}')
        except ValueError:
            self.get_logger().warn(f'Bad number in command: {line!r}')


def main(args=None):
    rclpy.init(args=args)
    node = CommandNode()

    # Read commands from stdin on a background thread so rclpy can spin.
    import threading

    def reader():
        for line in sys.stdin:
            node.handle(line)

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
