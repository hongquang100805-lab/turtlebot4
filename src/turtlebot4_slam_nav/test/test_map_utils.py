"""Kiem tra loi duong dan va tham chieu anh cua ban do."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
import pytest
from turtlebot4_slam_nav.map_utils import validate_map
import yaml


def test_missing_map_explains_mapping(tmp_path):
    """Ban do chua tao phai co huong dan mapping."""
    with pytest.raises(ValueError, match='mapping.launch.py'):
        validate_map(tmp_path / 'missing.yaml')


def test_official_map_and_relative_image():
    """Dung ban do chinh thuc chi de kiem tra doc YAML."""
    share = Path(get_package_share_directory('turtlebot4_navigation'))
    path, image = validate_map(share / 'maps/depot.yaml')
    assert path.is_file()
    assert image.is_file()
    assert image.parent == path.parent


def test_missing_image_is_rejected(tmp_path):
    """YAML tro toi anh khong ton tai phai bi tu choi."""
    path = tmp_path / 'invalid.yaml'
    path.write_text(yaml.safe_dump({'image': 'missing.pgm'}))
    with pytest.raises(ValueError, match='Anh ban do khong ton tai'):
        validate_map(path)


def test_invalid_yaml_is_rejected(tmp_path):
    """YAML loi phai co thong bao de doc."""
    path = tmp_path / 'invalid.yaml'
    path.write_text('image: [')
    with pytest.raises(ValueError, match='Ban do khong hop le'):
        validate_map(path)
