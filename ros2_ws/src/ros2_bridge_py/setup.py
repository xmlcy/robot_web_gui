from setuptools import setup
import os
from glob import glob

package_name = 'ros2_bridge_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('lib', package_name), glob('ros2_bridge_py/*.dat')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chase',
    maintainer_email='lcy5656@qq.com',
    description='a simple demo for ros2 bridge to websocket',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bridge_websocket = ros2_bridge_py.bridge_websocket:main',
            'bridge_video = ros2_bridge_py.bridge_video:main',
            'bridge_dlib = ros2_bridge_py.bridge_dlib:main',
            'bridge_remote = ros2_bridge_py.bridge_remote:main'
        ],
    },
)
