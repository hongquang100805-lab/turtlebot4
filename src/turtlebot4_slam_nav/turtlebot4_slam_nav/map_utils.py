"""Kiem tra ban do truoc khi khoi chay map server."""

from pathlib import Path

import yaml


def validate_map(filename):
    """Tra ve duong dan YAML va anh, hoac bao loi co cach khac phuc."""
    path = Path(filename).expanduser().resolve()
    if not path.is_file():
        raise ValueError(
            f'Khong tim thay ban do: {path}. Chay mapping.launch.py, '
            'khao sat va ros2 run turtlebot4_slam_nav save_map.sh; '
            'hoac truyen map:=/duong/dan/map.yaml hop le.')
    try:
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict) or not isinstance(data.get('image'), str):
            raise ValueError('YAML phai co truong image dang chuoi.')
        image = Path(data['image']).expanduser()
        if not image.is_absolute():
            image = path.parent / image
        image = image.resolve()
        if not image.is_file() or image.stat().st_size == 0:
            raise ValueError(f'Anh ban do khong ton tai hoac rong: {image}')
        if float(data['resolution']) <= 0:
            raise ValueError('resolution phai lon hon 0.')
        if len(data['origin']) != 3:
            raise ValueError('origin phai co 3 gia tri.')
        for value in data['origin']:
            float(value)
        if not 0 <= float(data['free_thresh']) < float(data['occupied_thresh']) <= 1:
            raise ValueError('Nguong free_thresh/occupied_thresh khong hop le.')
        if data['negate'] not in (0, 1):
            raise ValueError('negate phai la 0 hoac 1.')
    except (OSError, yaml.YAMLError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f'Ban do khong hop le ({path}): {exc}') from exc
    return path, image
