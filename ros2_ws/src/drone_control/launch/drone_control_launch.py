"""Launch both drone_control nodes together."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='drone_control',
            executable='position_node',
            name='position_node',
            output='screen',
        ),
        Node(
            package='drone_control',
            executable='command_node',
            name='command_node',
            output='screen',
        ),
    ])
