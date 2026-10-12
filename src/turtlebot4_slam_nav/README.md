# Bài thực hành 04 – TurtleBot 4 Simulation, SLAM và Navigation

Môi trường thực tế: **Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic (gz-sim 8)**,
Python hệ thống 3.12. Workspace mặc định `~/tb4_ws`, package `turtlebot4_slam_nav`.
Bài này sử dụng simulator, robot, bridge, controller và cấu hình SLAM/AMCL/Nav2
chính thức đã cài bằng apt. Không cần build simulator từ source.

## 1. Các chế độ

| Launch | Simulator | SLAM Toolbox | Map server + AMCL | Nav2 | RViz fixed frame |
|---|---|---|---|---|---|
| `simulation.launch.py` | Có | Không | Không | Không | `odom` |
| `mapping.launch.py` | Có | Có, synchronous | Không | Không | `map` |
| `localization.launch.py` | Có | Không | Có | Không | `map` |
| `navigation.launch.py` | Có | Không | Có | Có | `map` |

**Bốn chế độ thay thế nhau.** Trước khi chuyển chế độ, dừng teleop bằng `k`,
rồi `Ctrl+C`; dừng launch ở terminal A bằng `Ctrl+C`, chờ các tiến trình thoát.
Không chạy hai launch đồng thời. Mỗi launch tự tạo một simulator và một RViz2.
Server và GUI Gazebo chạy thành hai tiến trình chính thức riêng biệt, cùng
`GZ_PARTITION`; GUI là client của server, không tạo thêm simulator.
Giữ nguyên `world`, `model`, `x`, `y`, `z`, `yaw` giữa các lần chạy.
Mặc định: `world:=depot model:=standard x:=0.0 y:=0.0 z:=0.0 yaw:=0.0`.
Đổi world bằng `world:=maze` hoặc `world:=warehouse`, rồi tạo bản đồ cho world đó.

Sensor mặc định dùng `sensor_render_engine:=ogre2`. Trên máy này engine `ogre`
của Create 3 cho toàn bộ scan bằng `0.164 m`; cờ Gazebo chính thức
`--render-engine-server ogre2` đã sửa được bằng kiểm tra dữ liệu thực tế.
Wrapper giữ model/world/controller/bridge chính thức, chỉ bổ sung cờ này vào
tiến trình Gazebo. Không sửa file trong `/opt/ros`. Máy khác cần engine cũ có
thể truyền `sensor_render_engine:=ogre`, nhưng phải kiểm tra chất lượng scan.

GUI Gazebo mặc định `gui_render_engine:=ogre`. Trên máy này cả GUI Ogre và
Ogre2 đã có lần crash trong plugin `MinimalScene`; chưa coi lỗi GUI là đã sửa.
Wrapper tách GUI khỏi server để crash/đóng GUI không dừng SLAM/Nav2.
`gazebo_gui:=false` chạy server và RViz, là cách đã kiểm tra Nav2 active.
Có thể thử `gui_render_engine:=ogre2`; sensor vẫn dùng Ogre2 nên cờ GUI không
làm thay đổi phép đo LiDAR. Để dừng toàn bộ phiên, luôn `Ctrl+C` ở terminal A.

RViz có RobotModel, LaserScan và TF; mapping có Map; localization có Map và
particle cloud; navigation thêm path/costmap và công cụ Nav2 Goal.
LaserScan dùng QoS Best Effort/Volatile, Map dùng Reliable/Transient Local.

## 2. Dependency và môi trường terminal

Các gói chính đã có trên máy khi triển khai. Nếu máy khác thiếu gói, cài:

```bash
sudo apt update
sudo apt install ros-jazzy-turtlebot4-simulator ros-jazzy-irobot-create-nodes \
  ros-jazzy-turtlebot4-navigation ros-jazzy-nav2-bringup ros-jazzy-slam-toolbox \
  ros-jazzy-rviz2 ros-jazzy-teleop-twist-keyboard ros-jazzy-tf2-ros \
  ros-jazzy-rmw-fastrtps-cpp \
  python3-colcon-common-extensions python3-yaml python3-pytest
```

Gazebo Harmonic đã có (`gz sim --versions` cho biết `8.11.0`). Nếu chưa có,
theo hướng dẫn [cài Harmonic](https://gazebosim.org/docs/harmonic/install_ubuntu/)
và cài `gz-harmonic` từ repository chính thức. Không chạy nâng cấp toàn hệ thống.

**Trong mọi terminal A/B/C của bài**, chạy trước:

```bash
source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh
```

Script này chỉ thay đổi terminal đang source: chọn Python hệ thống, source
`/opt/ros/jazzy/setup.bash` và overlay của bài, loại overlay workspace khác,
bỏ các biến GUI kế thừa từ VS Code Snap gây lỗi `libpthread` trên máy này.
Không sửa `.bashrc`. Nếu Conda đang active, hãy `conda deactivate` đến khi thoát
môi trường trước khi source. Xác nhận:

```bash
echo "$ROS_DISTRO"
command -v python3
python3 --version
ros2 pkg prefix turtlebot4_gz_bringup
gz sim --versions
```

Kết quả mong đợi: `jazzy`, `/usr/bin/python3`, Python 3.12 và Gazebo 8.
Script đặt `ROS_DOMAIN_ID=74`, `ROS_AUTOMATIC_DISCOVERY_RANGE=SYSTEM_DEFAULT`,
`ROS_STATIC_PEERS=''`, `GZ_PARTITION=tb4_ws_lab_74`, log ROS trong `~/tb4_ws/log/ros`.
Cache model Gazebo Fuel của bài nằm trong `~/tb4_ws/log/gz_fuel`;
model Depot chính thức đã được tải trong phiên triển khai này.
Script và launch dùng `config/fastdds_local.xml` với `rmw_fastrtps_cpp`:
UDP trên loopback `127.0.0.1`, `maxInitialPeersRange=128`. Chỉ dùng môi trường
này trong terminal của bài. `SYSTEM_DEFAULT` ở đây lấy profile của bài,
giao tiếp vẫn giới hạn trên máy. Không dùng chế độ `LOCALHOST` của RMW Jazzy
vì [source RMW](https://github.com/ros2/rmw_fastrtps/blob/jazzy/rmw_fastrtps_shared_cpp/src/participant.cpp)
đặt dải discovery 32 participant, ít hơn số tiến trình của simulator + Nav2.
Xem [cấu hình transport Fast DDS](https://fast-dds.docs.eprosima.com/en/2.14.x/fastdds/xml_configuration/transports.html).
Đây là nguyên nhân đã đối chiếu source của hiện tượng topic có nhưng một số
node không nhận dữ liệu/service trong phiên kiểm tra.
Dùng cùng môi trường ở mọi terminal để tránh lẫn robot thật hoặc dự án ROS khác.
Nếu domain 74 đang có phiên khác, chọn domain trống ở **tất cả** terminal:

```bash
export TB4_LAB_DOMAIN_ID=75
source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh
```

Workspace ở vị trí khác: đặt `TB4_LAB_WS` trước khi source script. Khi đó truyền
`map:=...` và đường dẫn lưu map tương ứng; mặc định map vẫn theo `~/tb4_ws`.

## 3. Build – terminal A

```bash
source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh
cd ~/tb4_ws
/usr/bin/python3 -m colcon build --symlink-install --packages-select turtlebot4_slam_nav
source install/local_setup.bash
ros2 pkg prefix turtlebot4_slam_nav
ros2 launch turtlebot4_slam_nav simulation.launch.py --show-args
```

`setup.py` cài launch, RViz, YAML trong config nếu có, map nếu có và script lưu.
`config/fastdds_local.xml` được cả launch và `scripts/env.sh` sử dụng;
SLAM/AMCL/Nav2 vẫn dùng YAML chính thức, chưa cần YAML riêng.
`maps/` ban đầu rỗng: build vẫn hoạt động, không có bản đồ giả hay bản đồ mẫu
được đổi tên thành bản đồ bài làm. `.gitignore` không loại `map.yaml`/`map.pgm`.

## 4. Simulation và kiểm tra sensor

**Terminal A**, giữ mở:

```bash
ros2 launch turtlebot4_slam_nav simulation.launch.py
```

Gazebo mở world depot và robot; RViz dùng fixed frame `odom` vì chưa có `map`.
Nếu clock chưa chạy, kiểm tra nút Play/Pause của Gazebo. Lần đầu world depot tải
model chính thức từ Gazebo Fuel; có thể mất vài phút. Đợi world tải xong trước
khi thao tác. Nếu spawn báo timeout, tải model trước rồi khởi động lại launch:

```bash
# Terminal C, sau khi dừng launch ở A:
gz fuel download -u https://fuel.gazebosim.org/1.0/OpenRobotics/models/Depot
# Sau khi tải thành công, terminal A chạy lại simulation.launch.py.
```

**Terminal C**, source `scripts/env.sh`, kiểm tra từng lệnh:

```bash
ros2 node list --no-daemon --spin-time 5
ros2 topic list --no-daemon
ros2 topic echo /clock rosgraph_msgs/msg/Clock --once
ros2 topic echo /scan sensor_msgs/msg/LaserScan --once --field header --qos-reliability best_effort
ros2 topic echo /odom nav_msgs/msg/Odometry --once --field header
ros2 topic info /scan -v
ros2 topic info /cmd_vel -v
ros2 run tf2_ros tf2_echo odom base_link --ros-args -p use_sim_time:=true
```

Các lệnh echo/TF cần terminal A đang chạy; `Ctrl+C` để dừng lệnh chờ hoặc TF.
Kiểm tra tần số bằng `ros2 topic hz /scan` và `ros2 topic hz /odom`.
Frame cấu hình chính thức: `odom`, `base_link`, `rplidar_link`; scan bridge của
robot standard không namespace dùng frame `turtlebot4/rplidar_link/rplidar`.
Đọc `header.frame_id` thực tế của `/scan`, rồi kiểm tra:

```bash
ros2 run tf2_ros tf2_echo base_link rplidar_link --ros-args -p use_sim_time:=true
ros2 run tf2_ros tf2_echo base_link turtlebot4/rplidar_link/rplidar \
  --ros-args -p use_sim_time:=true
ros2 param get /robot_state_publisher use_sim_time --no-daemon --spin-time 5
ros2 param get /motion_control use_sim_time --no-daemon --spin-time 5
ros2 param get /rviz2 use_sim_time --no-daemon --spin-time 5
```

Các node xử lý dữ liệu mô phỏng dùng `use_sim_time=true`. Simulation chưa có
`map → odom`; mapping do SLAM Toolbox cung cấp; localization/navigation do AMCL
cung cấp sau initial pose. Không chạy SLAM và AMCL đồng thời.

## 5. Undock và teleoperation – terminal B

Sau khi robot spawn, robot bắt đầu trên dock. **Mỗi lần khởi động lại simulator**,
kiểm tra và undock trước khi di chuyển:

```bash
source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh
ros2 topic echo /dock_status irobot_create_msgs/msg/DockStatus --once
ros2 action list -t
ros2 interface show irobot_create_msgs/action/Undock
ros2 action send_goal /undock irobot_create_msgs/action/Undock '{}' --feedback
```

Đợi action thành công và `is_docked: false`. Dùng action Create 3 `/undock`,
khác action Nav2 `/undock_robot`. Nếu đã undock thì không cần gọi lại.
Nếu action bị từ chối và log ghi `Robot already undocked`, kiểm tra lại
`/dock_status`; đây là trạng thái đã rời dock, không phải lỗi kiểu action.

Trong bản Jazzy đang cài, `/cmd_vel` nhận **`geometry_msgs/msg/TwistStamped`**,
subscriber chính là `motion_control`. Teleop chính thức có tùy chọn `stamped`:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args \
  -p stamped:=true -p use_sim_time:=true -p frame_id:=base_link \
  -p speed:=0.30 -p turn:=1.0
```

Lệnh này đặt tốc độ tiến/lùi 0.30 m/s và tốc độ quay 1.0 rad/s, gấp đôi
mức ban đầu của bài. Nếu đang mở teleop cũ, nhấn `k`, rồi `Ctrl+C` và chạy lại
lệnh trên; các tham số `speed`/`turn` của teleop đang cài là read-only.

Giữ B mở, đặt focus vào B: `i` tiến, `,` lùi, `j/l` quay, `k` dừng;
`q/z` tăng/giảm cả hai tốc độ, `w/x` tăng/giảm tốc tuyến tính,
`e/c` tăng/giảm tốc quay; `Ctrl+C` thoát.
Vì teleop này gửi khi nhấn phím, nhấn/giữ phím để tiếp tục cập nhật vận tốc.
Quan sát robot trong Gazebo và `/odom`; đây là kiểm tra khả năng nhận `/cmd_vel`.
Không gửi Twist thường và không remap vào `diffdrive_controller/cmd_vel`
vì phải đi qua bộ điều khiển chính thức.

Luồng Nav2 trong bản đang cài:
`controller_server/behavior_server → /cmd_vel_nav → velocity_smoother →
/cmd_vel_smoothed → collision_monitor → /cmd_vel → motion_control →
/diffdrive_controller/cmd_vel → Gazebo bridge`.

## 6. Mapping, khảo sát và lưu map

1. Dừng teleop B và simulation A như mục 1.
2. **A**, chạy và giữ mở:

   ```bash
   ros2 launch turtlebot4_slam_nav mapping.launch.py world:=depot
   ```

3. **B**, undock robot mới rồi chạy lại teleop ở mục 5. Khảo sát chậm, đi qua
   các lối đi, quay để quét đủ tường và trở lại vùng đã đi để đóng vòng.
   Quan sát Map cập nhật trong RViz; không cần Nav2 ở giai đoạn này.
4. **C**, kiểm tra rồi lưu trong khi A vẫn chạy:

   ```bash
   source ~/tb4_ws/src/turtlebot4_slam_nav/scripts/env.sh
   ros2 lifecycle get /slam_toolbox
   ros2 param get /slam_toolbox use_sim_time
   ros2 topic echo /map nav_msgs/msg/OccupancyGrid --once --field info --qos-durability transient_local
   ros2 run tf2_ros tf2_echo map odom --ros-args -p use_sim_time:=true
   # Ctrl+C de dung tf2_echo, sau do:
   ros2 run turtlebot4_slam_nav save_map.sh
   ls -lh ~/tb4_ws/src/turtlebot4_slam_nav/maps/map.{yaml,pgm}
   cat ~/tb4_ws/src/turtlebot4_slam_nav/maps/map.yaml
   ```

Mặc định lưu `~/tb4_ws/src/turtlebot4_slam_nav/maps/map.yaml` và `map.pgm`.
Script tạo thư mục, dùng Nav2 `map_saver_cli` với QoS Transient Local, kiểm tra
mã thoát và xác nhận `image:` trong YAML trỏ đúng PGM. Khi `/map` chưa có,
script báo lỗi sau thời gian chờ hữu hạn. Script từ chối ghi đè bản đồ cũ;
để lưu phiên mới hãy chọn tên khác:

```bash
ros2 run turtlebot4_slam_nav save_map.sh "$HOME/tb4_ws/src/turtlebot4_slam_nav/maps/depot_02"
ros2 run turtlebot4_slam_nav save_map.sh "$HOME/tb4_ws/maps/khao sat/map"
```

Tên tương đối lưu theo thư mục hiện tại; đường dẫn có dấu cách phải đặt trong
dấu ngoặc kép. Chuyển cả YAML và PGM cùng nhau nếu di chuyển bản đồ.
Bản đồ occupancy YAML/PGM dùng cho AMCL, không phải pose graph để tiếp tục SLAM.

## 7. Localization trên bản đồ vừa tạo

Sau khi lưu thành công, dừng B rồi A. **A** chạy lại cùng world:

```bash
ros2 launch turtlebot4_slam_nav localization.launch.py world:=depot \
  map:="$HOME/tb4_ws/src/turtlebot4_slam_nav/maps/map.yaml"
```

Giữ A mở. **B** undock theo mục 5. Trong RViz, dùng **2D Pose Estimate**:
nhấn tại vị trí robot trên bản đồ đã khảo sát và kéo mũi tên theo hướng robot.
Vị trí spawn trong tọa độ Gazebo không nhất thiết là cùng tọa độ trên bản đồ
SLAM; dùng đặc điểm tường và vị trí lúc bắt đầu khảo sát để xác định.
Sau undock, robot đã lùi khỏi dock nên đặt pose theo vị trí hiện tại.

**C**, kiểm tra:

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 param get /amcl use_sim_time --no-daemon --spin-time 5
ros2 topic echo /amcl_pose geometry_msgs/msg/PoseWithCovarianceStamped --once
ros2 run tf2_ros tf2_echo map odom --ros-args -p use_sim_time:=true
```

Map server và AMCL phải `active`; LiDAR chồng lên các tường của bản đồ.
Nếu chưa khớp, đặt lại initial pose. Có thể quay chậm bằng teleop trong bước
localization để AMCL cập nhật, rồi dừng B. Không có Nav2 trong chế độ này.

## 8. Navigation – thực hiện ít nhất 3 goal

Dừng localization ở A và teleop ở B trước khi chạy **A**:

```bash
ros2 launch turtlebot4_slam_nav navigation.launch.py world:=depot \
  map:="$HOME/tb4_ws/src/turtlebot4_slam_nav/maps/map.yaml"
```

Giữ A mở. Robot mới: undock và đặt lại **2D Pose Estimate** như mục 7.
**Thoát teleop B trước khi gửi goal; sau khi gửi goal không điều khiển thủ công.**
Chờ Nav2 active; trong **C** có thể kiểm tra:

```bash
ros2 lifecycle get /controller_server
ros2 lifecycle get /bt_navigator
ros2 lifecycle get /collision_monitor
ros2 action info /navigate_to_pose
ros2 topic echo /navigate_to_pose/_action/status action_msgs/msg/GoalStatusArray
```

Trong RViz dùng **Nav2 Goal**, nhấn vào vùng trống trên bản đồ rồi kéo để chọn
hướng đích. Chọn ba vùng khác nhau đã được map, tránh sát tường và vùng xám.
Gửi từng goal, chờ trạng thái `SUCCEEDED` (action status `4`) và robot đến đích
rồi mới gửi goal tiếp theo. Theo dõi đường `/plan`, local/global costmap và
Navigation 2 panel. Nếu goal thất bại (`ABORTED`, status `6`), đọc log và điều
chỉnh initial pose/goal khi cần; không ghi nhận nó là goal thành công.

| Goal | Vùng/đặc điểm | Tọa độ nếu ghi lại | Kết quả | Mốc thời gian video |
|---|---|---|---|---|
| 1 | Tự bổ sung | | | |
| 2 | Tự bổ sung | | | |
| 3 | Tự bổ sung | | | |

## 9. Map trong source, install và đường dẫn tùy chọn

Không cần build lại khi truyền trực tiếp `map:="$HOME/tb4_ws/src/.../map.yaml"`.
Argument `map` cũng nhận đường dẫn tuyệt đối khác hoặc đường dẫn tương đối
theo thư mục chạy lệnh. Khi không truyền `map`, wrapper ưu tiên
`~/tb4_ws/src/turtlebot4_slam_nav/maps/map.yaml`; nếu không có, dùng bản
`share/turtlebot4_slam_nav/maps/map.yaml` đã được cài nếu tồn tại.
Thiếu YAML/ảnh hoặc YAML sai sẽ báo lỗi trước khi bật simulator.

Để đưa bản đồ mới vào install cho việc phân phối, build lại sau khi lưu
(ngay cả `--symlink-install` cần chạy build để nhận file mới):

```bash
cd ~/tb4_ws
/usr/bin/python3 -m colcon build --symlink-install --packages-select turtlebot4_slam_nav
source install/local_setup.bash
ros2 launch turtlebot4_slam_nav navigation.launch.py \
  map:="$(ros2 pkg prefix --share turtlebot4_slam_nav)/maps/map.yaml"
```

## 10. Lỗi thường gặp

| Hiện tượng | Kiểm tra/xử lý |
|---|---|
| `libpthread.so.0`, `GLIBC_PRIVATE` từ `/snap/core20` | Source `scripts/env.sh` hoặc mở terminal hệ thống. Script bỏ biến GTK/GIO từ Snap cho phiên này. |
| Gazebo GUI crash trong `MinimalScene` | Server tiếp tục chạy vì GUI là tiến trình riêng. Dùng `gazebo_gui:=false` để làm bài qua RViz; có thể thử `gui_render_engine:=ogre2`. Cả hai GUI engine từng crash trên máy này. Không đổi sensor về Ogre. |
| Gazebo chờ world, `Requesting list of world names`, controller timeout | Tải Depot bằng `gz fuel download` trước, chờ thành công, dừng và chạy lại launch. Xem kết nối Fuel/S3; không thay world rồi dùng map depot. |
| Không có `/clock` | World phải tải xong, simulator đang Play; kiểm tra `ros2 topic echo /clock rosgraph_msgs/msg/Clock --once`. |
| CLI báo Node not found dù node đang chạy | Dùng `ros2 param get /ten_node use_sim_time --no-daemon --spin-time 5` để chờ discovery. |
| Topic có nhưng node không nhận dữ liệu, lifecycle chờ service | Source cùng env.sh/domain/profile ở mọi terminal. Không đổi lại discovery về LOCALHOST (giới hạn 32 participant trong Jazzy). Dừng rồi khởi động lại toàn bộ chế độ sau khi đổi profile. |
| LiDAR không hiện trong RViz | `ros2 topic info /scan -v`, đọc frame scan, kiểm tra TF; LaserScan QoS Best Effort/Volatile. |
| Tất cả scan bằng `0.164 m`, map chỉ là ô nhỏ | Dùng mặc định `sensor_render_engine:=ogre2`; xem [issue Create 3](https://github.com/iRobotEducation/create3_sim/issues/240). Không dùng map đó để làm bài. |
| Robot không chạy | Undock, kiểm tra `/dock_status`, `/cmd_vel` phải TwistStamped, teleop focus đúng terminal. |
| Mapping báo không có map frame | Chờ SLAM active, `/scan` và odom/TF phải hoạt động; fixed frame mapping là map. |
| Map không xuất hiện | Kiểm tra map server active, đường dẫn YAML và `image`, QoS Map Transient Local. |
| RViz báo shader `active samplers ... same texture image unit` | Đã thấy trong phiên kiểm tra; [issue RViz](https://github.com/ros2/rviz/issues/463) ghi nhận lỗi khi vẽ map lần đầu. Kiểm tra hiển thị thực tế và Map status; không xem thông báo này là bằng chứng map đã hỏng. |
| AMCL chưa có `map → odom` | Đặt 2D Pose Estimate; kiểm tra scan, `/amcl_pose` và use_sim_time. |
| Nav2 không di chuyển/goal thất bại | Kiểm tra AMCL, lifecycle Nav2, costmap, `/cmd_vel` và log; goal phải nằm vùng trống đã map. |
| Hai simulator/node trùng tên ngoài dự kiến | Dừng phiên cũ ở terminal đã chạy; không `pkill` toàn bộ ROS/Gazebo của các dự án khác. |

Tắt RViz khi cần bằng `rviz:=false`; `gazebo_gui:=false` tắt GUI Gazebo nhưng
vẫn chạy server với sensor rendering. Đóng GUI Gazebo không dừng server;
`Ctrl+C` ở A dừng toàn bộ phiên. Launch không tự chọn bản đồ mẫu nếu bản đồ
bài làm còn thiếu.

## 11. Kiểm tra mã nguồn

```bash
cd ~/tb4_ws
source src/turtlebot4_slam_nav/scripts/env.sh
/usr/bin/python3 -m compileall -q src/turtlebot4_slam_nav
bash -n src/turtlebot4_slam_nav/scripts/env.sh
bash -n src/turtlebot4_slam_nav/scripts/save_map.sh
/usr/bin/python3 -m colcon test --packages-select turtlebot4_slam_nav
/usr/bin/python3 -m colcon test-result --verbose
for mode in simulation mapping localization navigation; do
  ros2 launch turtlebot4_slam_nav "$mode.launch.py" --show-args
done
```

Kết quả kiểm tra thực tế của phiên triển khai được ghi trong [VALIDATION.md](VALIDATION.md).
Không xem build/launch argument thành công là bằng chứng mapping hay navigation
đã hoàn thành. Người thực hiện cần khảo sát, lưu map thật, đặt initial pose và
chọn ba goal để nghiệm thu.

## 12. Checklist quay video và nộp bài

- [ ] Gazebo world depot và TurtleBot 4; `/clock`, `/scan`, `/odom` có dữ liệu.
- [ ] Teleoperation sau undock; RViz hiển thị robot và LiDAR.
- [ ] Mapping: lái khảo sát, bản đồ cập nhật, đóng vòng và đủ các vùng cần đi.
- [ ] Lưu map thật; quay `map.yaml`, `map.pgm` và bản đồ hoàn chỉnh.
- [ ] Dừng mapping, khởi động lại cùng world; load bản đồ, SLAM đã tắt.
- [ ] 2D Pose Estimate, LiDAR khớp map, AMCL có `map → odom`.
- [ ] Navigation: ba goal ở ba vùng khác nhau, từng goal `SUCCEEDED`.
- [ ] Sau khi gửi goal không điều khiển robot thủ công.
- [ ] Đưa source, map YAML/PGM và hướng dẫn vào Git; kiểm tra link nộp bài.

Link GitHub: **[tự bổ sung]**

Link Google Drive video: **[tự bổ sung]**

## 13. Tài liệu đối chiếu

- [Simulator – mục Jazzy](https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_simulator.html)
- [Source simulator nhánh jazzy](https://github.com/turtlebot/turtlebot4_simulator/tree/jazzy)
- [Tạo bản đồ – mục Jazzy](https://turtlebot.github.io/turtlebot4-user-manual/tutorials/generate_map.html)
- [Navigation – mục Jazzy](https://turtlebot.github.io/turtlebot4-user-manual/tutorials/navigation.html)
- [Keyboard driving – mục Jazzy, stamped velocity](https://turtlebot.github.io/turtlebot4-user-manual/tutorials/driving.html)

Đã đọc source và `--show-args` của launch **đang cài**, không lấy tham số Humble
để áp dụng cho Jazzy. Wrapper lấy các action của `sim.launch.py` chính thức,
giữ resource path/GUI plugin path/clock bridge và dùng Gazebo include chính thức
cho server `-s` và GUI client `-g` riêng, thêm cờ render engine; rồi include
`turtlebot4_spawn.launch.py` với SLAM,
localization, Nav2 và RViz đều tắt. Sau đó include đúng thành phần của
`turtlebot4_navigation` theo chế độ. `params` của SLAM/localization và
`params_file` của Nav2 giữ nguyên cấu hình chính thức. Bốn cấu hình RViz được
rút gọn từ `turtlebot4_viz/rviz/navigation.rviz` (Clearpath, Apache-2.0).
