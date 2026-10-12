"""Chay simulator, SLAM Toolbox va RViz2."""

from turtlebot4_slam_nav.launch_helpers import make_launch


def generate_launch_description():
    """Tao che do mapping, khong bat AMCL hoac Nav2."""
    return make_launch('mapping')
