from glob import glob

from setuptools import find_packages, setup

package_name = 'turtlebot4_slam_nav'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml', 'README.md', 'VALIDATION.md', 'LICENSE']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml') + glob('config/*.xml')),
        ('share/' + package_name + '/rviz', glob('rviz/*.rviz')),
        ('share/' + package_name + '/scripts', ['scripts/env.sh']),
        ('share/' + package_name + '/maps',
         glob('maps/*.yaml') + glob('maps/*.pgm') + glob('maps/*.png')),
    ],
    scripts=['scripts/save_map.sh'],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lenovo',
    maintainer_email='hongquang100805@gmail.com',
    description='TurtleBot 4 Jazzy simulation, SLAM, localization and navigation lab',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
