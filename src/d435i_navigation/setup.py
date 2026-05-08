import os
from glob import glob
from setuptools import setup

package_name = 'd435i_navigation'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch fajlok regisztralasa
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        # Config fajlok regisztralasa
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robi772',
    maintainer_email='robi772@users.noreply.github.com',
    description='ROS2 Kilted Kaiju D435i navigation package',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_yaw_to_odom = d435i_navigation.imu_yaw_to_odom:main',
        ],
    },
)
