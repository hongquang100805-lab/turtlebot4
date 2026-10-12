"""Chay simulator, map server, AMCL va RViz2."""

from turtlebot4_slam_nav.launch_helpers import make_launch


def generate_launch_description():
    """Tao che do localization, khong bat SLAM hoac Nav2."""
    return make_launch('localization')
