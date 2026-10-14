"""Command node: fly the drone with simple keyboard commands (PX4 Offboard).

PX4 Offboard mode requires:
  1. A stream of OffboardControlMode  (>2 Hz, else PX4 rejects offboard)
  2. A stream of TrajectorySetpoint   (the target position)
  3. VehicleCommand messages to ARM and to switch into Offboard mode

Type commands (NED metres):
    x 1      -> move 1 m North  (relative)
    y 5      -> move 5 m East   (relative)
    z -2     -> climb 2 m       (up is negative z in NED!)
    arm
    offboard
    takeoff   (arm + offboard + climb to 2 m)
    land
    hold

Note: PX4 uses the NED frame — z is DOWN, so to climb you command z negative.
"""

import sys
import threading

import rclpy
from rclpy.node import Node
from px4_msgs.msg import (
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleCommand,
    VehicleOdometry,
)


class CommandNode(Node):
    def __init__(self):
        super().__init__('command_node')

        # Latest known position (NED) — starts at origin.
        self.pos = [0.0, 0.0, 0.0]
        self.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry', self._odom_cb, 10
        )

        # PX4 offboard publishers.
        self.pub_offboard_mode = self.create_publisher(
            OffboardControlMode, '/fmu/in/offboard_control_mode', 10
        )
        self.pub_trajectory = self.create_publisher(
            TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10
        )
        self.pub_command = self.create_publisher(
            VehicleCommand, '/fmu/in/vehicle_command', 10
        )

        # PX4 requires offboard streams at >2 Hz; we use 20 Hz.
        self.timer = self.create_timer(0.05, self._publish_setpoint)

        self.get_logger().info(
            'command_node ready. Commands: arm / offboard / takeoff / land / '
            'hold / x <m> / y <m> / z <m>   (NED: up = -z)'
        )

    def _odom_cb(self, msg: VehicleOdometry):
        self.pos = list(msg.position)

    def _publish_setpoint(self):
        # 1) OffboardControlMode — we command position only.
        mode = OffboardControlMode()
        mode.position = True
        mode.velocity = False
        mode.acceleration = False
        mode.attitude = False
        mode.body_rate = False
        mode.thrust_and_torque = False
        mode.direct_actuator = False
        mode.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.pub_offboard_mode.publish(mode)

        # 2) TrajectorySetpoint — current target position.
        sp = TrajectorySetpoint()
        sp.position = [float(self.pos[0]), float(self.pos[1]), float(self.pos[2])]
        sp.velocity = [float('nan')] * 3          # leave uncontrolled
        sp.acceleration = [float('nan')] * 3
        sp.yawspeed = float('nan')
        sp.timestamp = mode.timestamp
        self.pub_trajectory.publish(sp)

    def _send_command(self, command: int, param1=0.0, param2=0.0):
        cmd = VehicleCommand()
        cmd.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        cmd.command = command
        cmd.param1 = float(param1)
        cmd.param2 = float(param2)
        cmd.target_system = 1
        cmd.target_component = 1
        cmd.source_system = 1
        cmd.source_component = 1
        cmd.from_external = True
        self.pub_command.publish(cmd)

    def arm(self):
        # VEHICLE_CMD_COMPONENT_ARM_DISARM = 400, param1=1 to arm
        self._send_command(400, param1=1.0)
        self.get_logger().info('Arming...')

    def offboard(self):
        # VEHICLE_CMD_DO_SET_MODE = 176; PX4 Offboard = custom_main_mode 6
        self._send_command(176, param1=1.0, param2=6.0)
        self.get_logger().info('Requesting Offboard mode...')

    def takeoff(self):
        self.arm()
        self.offboard()
        self.pos[2] = -2.0   # climb to 2 m (up is -z in NED)
        self.get_logger().info('Takeoff -> altitude 2 m')

    def land(self):
        self.pos[2] = 0.0
        self.get_logger().info('Land -> altitude 0 m')

    def handle(self, line: str):
        parts = line.strip().split()
        if not parts:
            return
        cmd = parts[0].lower()
        try:
            if cmd in ('x', 'y', 'z') and len(parts) == 2:
                axis = {'x': 0, 'y': 1, 'z': 2}[cmd]
                delta = float(parts[1])
                self.pos[axis] += delta
                self.get_logger().info(
                    f'{cmd} += {delta:.2f} -> target '
                    f'({self.pos[0]:.2f}, {self.pos[1]:.2f}, {self.pos[2]:.2f})'
                )
            elif cmd == 'arm':
                self.arm()
            elif cmd == 'offboard':
                self.offboard()
            elif cmd == 'takeoff':
                self.takeoff()
            elif cmd == 'land':
                self.land()
            elif cmd == 'hold':
                self.get_logger().info(
                    f'Hold at ({self.pos[0]:.2f}, {self.pos[1]:.2f}, {self.pos[2]:.2f})'
                )
            else:
                self.get_logger().warn(f'Unknown command: {line!r}')
        except ValueError:
            self.get_logger().warn(f'Bad number in command: {line!r}')


def main(args=None):
    rclpy.init(args=args)
    node = CommandNode()

    def reader():
        for line in sys.stdin:
            node.handle(line)

    threading.Thread(target=reader, daemon=True).start()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
