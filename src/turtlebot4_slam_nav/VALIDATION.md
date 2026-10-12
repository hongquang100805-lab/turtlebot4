# Kết quả kiểm tra ngày 09/10/2026

Thực hiện trực tiếp trong `~/tb4_ws`, Ubuntu 24.04, ROS 2 Jazzy, Python hệ thống
3.12.3, Gazebo Harmonic 8.11.0. Không chỉnh `~/ur_ws`, `/opt/ros`, `.bashrc`
hoặc nâng cấp hệ thống. Các dependency cần thiết đã cài sẵn.

## Kiểm tra package

- `colcon build --symlink-install --packages-select turtlebot4_slam_nav`: thành công.
- Cú pháp Python (`compileall`) và hai script shell (`bash -n`): đạt.
- `colcon test`: 7 test, 0 lỗi, 0 thất bại, 1 skipped. Sáu test chạy thành công;
  test copyright có sẵn trong package khung được đánh dấu skip.
- ROS 2 nhận diện package; cả bốn launch đọc được bằng `--show-args`.
- Build khi `maps/` chưa có YAML/PGM: thành công. Không có map giả trong source.
- Thiếu map ở localization/navigation: báo cách tạo/truyền map trước khi bật Gazebo.
- Script lưu map: báo lỗi có mã thoát khi không có `/map`; từ chối ghi đè map cũ;
  đã lưu thành công bản đồ SLAM thật và xác nhận `image: map.pgm`.

## Kiểm tra mô phỏng và dữ liệu

Các phiên thử dùng domain riêng 174–179, cùng partition Gazebo riêng của bài.
Lệnh vận tốc và undock chỉ gửi trong những phiên mô phỏng này.

- `/clock`, `/scan`, `/odom` có dữ liệu. Laser có 640 mẫu, frame thực tế
  `turtlebot4/rplidar_link/rplidar`.
- Với sensor Ogre2, scan depot có khoảng cách khác nhau (mẫu kiểm tra Nav2:
  min khoảng 1.482 m, max khoảng 11.937 m); không còn toàn bộ 0.164 m.
- TF `odom → base_link → rplidar_link → turtlebot4/rplidar_link/rplidar` hoạt động.
- `/cmd_vel` là `geometry_msgs/msg/TwistStamped`, `motion_control` nhận lệnh.
  Thử tiến chậm trong world maze: odometry thay đổi khoảng 0.045 m; sau thử
  đã gửi lệnh vận tốc bằng 0. Không gửi goal điều hướng trong phép thử này.
- Action Create 3 `/undock` đã trả `SUCCEEDED`, `/dock_status` báo không còn dock.
- World Depot chính thức đã được tải và cache dưới `log/gz_fuel/`.
- Launch simulation cuối cùng đã chạy đúng một server và một GUI client riêng.
  Sau khi chủ động dừng GUI của phiên thử, server tiếp tục publish clock, scan,
  odom và TF; đọc được clock ở 134.799 giây mô phỏng.
  Bằng chứng: `log/lab_simulation_split_probe.log`, `log/lab_simulation_final_split.log`.

## SLAM và bản đồ thật dùng để kiểm tra

SLAM Toolbox đã nhận scan, publish `/map` và TF `map → odom`. Một bản đồ thật,
chỉ quan sát vùng ban đầu, được lưu ở:

```text
~/tb4_ws/log/validation_map_depot_udp/map.yaml
~/tb4_ws/log/validation_map_depot_udp/map.pgm
```

Bản đồ có 418 × 301 ô, độ phân giải 0.05 m/ô. Đây là bản đồ thử nghiệm giới
hạn, chưa khảo sát toàn depot, chưa phải bản đồ nộp bài và không được chép vào
`src/turtlebot4_slam_nav/maps/`. Cần tự lái khảo sát và lưu map của bài ở đó.

Log liên quan: `log/lab_save_map_depot_udp_final.log`,
`log/lab_undock_depot_confirmed.log`, `log/lab_mapping_depot_udp.log`.

## Localization và Nav2

- Chế độ localization: map server và AMCL tải bản đồ thử nghiệm thật và active;
  không chạy SLAM Toolbox.
- Chế độ navigation chạy server không GUI (`gazebo_gui:=false`) và RViz:
  map server, AMCL, controller server, planner server, BT navigator và collision
  monitor đều đã trả lifecycle `active` sau khi publish initial pose để kiểm tra.
- AMCL publish `/amcl_pose`; đã đọc được TF `map → odom`, `map → base_link`
  và `base_link → turtlebot4/rplidar_link/rplidar`.
- `/navigate_to_pose` có action server. Không gửi navigation goal;
  chưa xác nhận robot tự đến đích hoặc ba goal thành công.
- Trước initial pose, Nav2 có thể chờ TF/map và chưa active đầy đủ. Đây là
  bước còn thiếu đầu vào, cần đặt **2D Pose Estimate** sau undock mỗi lần chạy.

Bằng chứng: `log/lab_navigation_probe.log`,
`log/lab_navigation_depot_profile.log`, `log/lab_localization_depot_profile.log`.

## Lỗi môi trường đã xử lý và giới hạn còn lại

- Biến GUI từ VS Code Snap gây lỗi `libpthread / GLIBC_PRIVATE`: `env.sh` làm
  sạch môi trường trong terminal của bài; GUI đã khởi động được sau đó.
- RMW Jazzy ở discovery `LOCALHOST` đặt dải cổng discovery cho 32 participant;
  simulator và Nav2 có nhiều tiến trình hơn. Profile Fast DDS riêng dùng UDP
  loopback và dải 128, được env/launch sử dụng; lifecycle đã active sau thay đổi.
- Sensor Ogre cho scan cố định 0.164 m trên máy này: cờ render engine server
  Ogre2 đã sửa bằng đo dữ liệu. Model, world và controller chính thức giữ nguyên.
- **GUI Gazebo vẫn có lỗi crash `MinimalScene` trên máy này**, từng xảy ra với
  cả Ogre và Ogre2. Server và GUI nay chạy riêng, để mất GUI không mất SLAM/Nav2.
  Có thể chạy `gazebo_gui:=false` và thao tác qua RViz.
- RViz đã khởi động, nhận robot/map/scan và cấu hình QoS; có thông báo shader
  map khi vẽ lần đầu. Chưa xác nhận toàn bộ hiển thị bằng quan sát trực tiếp;
  cần kiểm tra Map/LaserScan status và LiDAR chồng lên tường trên máy.
- Log chính thức còn cảnh báo chu kỳ controller 0.001 s so với bước mô phỏng
  0.003 s và service HMI `stop_motor`/`oakd/stop_camera` không khả dụng.
  Controller vẫn active, dữ liệu và các kiểm tra trên vẫn hoạt động; không
  thay cấu hình controller để che các cảnh báo này.
- Không tự sửa driver hoặc package cài hệ thống. Cache/log và bản đồ thử nghiệm
  ở `log/`, không đưa vào Git.

## Phần người thực hiện hoàn thành

1. Khảo sát đầy đủ depot bằng teleop, xem bản đồ cập nhật và lưu YAML/PGM.
2. Dừng mapping, load đúng map cùng world, undock và đặt initial pose trong RViz.
3. Kiểm tra LiDAR khớp tường; chọn ba goal ở ba khu vực đã khảo sát và ghi nhận
   từng `SUCCEEDED`. Sau khi gửi goal không điều khiển thủ công.
4. Quay video theo README, bổ sung GitHub/Google Drive và commit map thật.
