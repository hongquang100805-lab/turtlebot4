"""Chay simulator, map server, AMCL, Nav2 va RViz2."""

from turtlebot4_slam_nav.launch_helpers import make_launch


def generate_launch_description():
    """Tao che do navigation voi ban do da luu."""
    return make_launch('navigation')
