"""Chay simulator va RViz2 voi fixed frame odom."""

from turtlebot4_slam_nav.launch_helpers import make_launch


def generate_launch_description():
    """Tao che do kiem tra sensor va teleoperation."""
    return make_launch('simulation')
