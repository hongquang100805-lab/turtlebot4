#!/usr/bin/env bash
# Luu ban do dang duoc publish, khong tao ban do mau.
set -euo pipefail

if [[ $# -gt 1 ]]; then
    echo 'Su dung: save_map.sh [ten_hoac_duong_dan_khong_co_duoi]' >&2
    exit 2
fi
if ! command -v ros2 >/dev/null; then
    echo 'Loi: chua source /opt/ros/jazzy/setup.bash va workspace.' >&2
    exit 1
fi

target="${1:-$HOME/tb4_ws/src/turtlebot4_slam_nav/maps/map}"
if [[ "$target" == '~/'* ]]; then
    target="$HOME/${target:2}"
fi
target="${target%.yaml}"
target="${target%.pgm}"
mkdir -p -- "$(dirname -- "$target")"
target="$(realpath -m -- "$target")"
if [[ -e "$target.yaml" || -e "$target.pgm" ]]; then
    echo "Loi: dich da ton tai: $target. Chon ten moi de giu ban do cu." >&2
    exit 1
fi

echo "Dang luu /map thanh $target.yaml va $target.pgm ..."
if timeout --signal=INT --kill-after=5s 35s \
    ros2 run nav2_map_server map_saver_cli -t /map -f "$target" --fmt pgm \
    --ros-args -p use_sim_time:=true -p map_subscribe_transient_local:=true \
    -p save_map_timeout:=10.0; then
    :
else
    status=$?
    echo "Loi: map_saver_cli that bai (ma $status). Giu mapping dang chay, kiem tra /clock va /map." >&2
    echo 'Kiem tra: ros2 topic info /map -v; ros2 lifecycle get /slam_toolbox' >&2
    exit "$status"
fi

/usr/bin/python3 - "$target" <<'PY'
import sys
from pathlib import Path
from turtlebot4_slam_nav.map_utils import validate_map

try:
    prefix = Path(sys.argv[1])
    path, image = validate_map(str(prefix) + '.yaml')
    expected = Path(str(prefix) + '.pgm')
    if image != expected or not expected.is_file():
        raise ValueError('YAML image khong tro toi dung file PGM vua luu.')
except ValueError as exc:
    print(f'Loi: {exc}', file=sys.stderr)
    sys.exit(1)
print(f'Da luu YAML: {path}')
print(f'Da luu PGM:  {image}')
PY
