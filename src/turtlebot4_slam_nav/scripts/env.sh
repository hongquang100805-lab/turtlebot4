#!/usr/bin/env bash
# Source file nay trong moi terminal; khong sua .bashrc.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    echo 'Hay dung: source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh' >&2
    exit 2
fi

export TB4_LAB_WS="${TB4_LAB_WS:-$HOME/tb4_ws}"
# Dung Python he thong va bo overlay cua cac workspace khac trong terminal nay.
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH CMAKE_PREFIX_PATH PYTHONPATH LD_LIBRARY_PATH
unset PYTHONHOME VIRTUAL_ENV
# Bo bien GUI ke thua tu VS Code Snap gay loi libpthread tren may nay.
unset GTK_PATH GTK_EXE_PREFIX GTK_IM_MODULE_FILE GIO_MODULE_DIR LOCPATH
export XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
export QT_QPA_PLATFORM=xcb
source /opt/ros/jazzy/setup.bash
if [[ -f "$TB4_LAB_WS/install/local_setup.bash" ]]; then
    source "$TB4_LAB_WS/install/local_setup.bash"
fi

export ROS_DOMAIN_ID="${TB4_LAB_DOMAIN_ID:-74}"
export ROS_AUTOMATIC_DISCOVERY_RANGE=SYSTEM_DEFAULT
export ROS_STATIC_PEERS=''
# Profile loopback tranh gioi han 32 participant cua LOCALHOST trong Jazzy.
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export FASTRTPS_DEFAULT_PROFILES_FILE="$(realpath "$(dirname "${BASH_SOURCE[0]}")/../config/fastdds_local.xml")"
export FASTDDS_DEFAULT_PROFILES_FILE="$FASTRTPS_DEFAULT_PROFILES_FILE"
unset ROS_LOCALHOST_ONLY ROS_DISCOVERY_SERVER FASTDDS_BUILTIN_TRANSPORTS
export GZ_PARTITION="tb4_ws_lab_${ROS_DOMAIN_ID}"
export GZ_FUEL_CACHE_PATH="$TB4_LAB_WS/log/gz_fuel"
export ROS_LOG_DIR="$TB4_LAB_WS/log/ros"
mkdir -p "$ROS_LOG_DIR" "$GZ_FUEL_CACHE_PATH"
echo "Moi truong Jazzy: workspace=$TB4_LAB_WS; domain=$ROS_DOMAIN_ID; GZ_PARTITION=$GZ_PARTITION"
