import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'drone_control'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Python nodes to read drone position and send fly commands over ROS 2.',
    license='MIT',
    entry_points={
        'console_scripts': [
            'position_node = drone_control.position_node:main',
            'command_node = drone_control.command_node:main',
        ],
    },
)
