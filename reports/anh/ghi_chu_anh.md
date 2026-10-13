# Ảnh minh chứng nhận ngày 13/10/2026

Ba ảnh có đường dẫn đã được sao chép nguyên bản vào thư mục này, không cắt,
chỉnh màu, sửa chữ hoặc thêm trạng thái. Tên file giữ thời điểm chụp để đối chiếu.

| File | Vị trí đề xuất | Chú thích có thể dùng | Giới hạn của bằng chứng |
|---|---|---|---|
| `teleop_2026-10-12_23-07-05.png` | Mục 3.2, Hình 4(a) | Giao diện điều khiển TurtleBot 4 bằng teleop và thay đổi giá trị đặt tốc độ. | Chứng minh giao diện teleop hoạt động; không chứng minh robot đã nhận `/cmd_vel` hoặc chạy đúng tốc độ hiển thị. |
| `localization_rviz_2026-10-12_23-30-06.png` | Mục 5.2, Hình 9(a) | RViz hiển thị bản đồ, mô hình robot, dữ liệu LiDAR và tập hạt AMCL trong chế độ localization. | Có `Global Status: Ok`; vẫn cần đối chiếu vị trí/hướng với Gazebo, không kết luận pose đã chính xác chỉ từ ảnh này. |
| `navigation_reached_2026-10-12_23-35-20.png` | Mục 6.2, Hình 11(a) tạm thời | Giao diện Nav2 với Navigation và Localization active, Feedback hiển thị reached sau một goal. | Minh chứng một lần có Feedback reached; chưa xác định số thứ tự/UUID của goal, không đại diện cho ba goal hoặc chứng minh không va chạm. |

## Hai ảnh terminal trong tin nhắn

Hai ảnh sau được xem trực tiếp trong hội thoại nhưng chưa có đường dẫn file
để sao chép vào báo cáo:

- **Ảnh đo tần số:** các dòng average rate khoảng 15.2 Hz. Phần lệnh gọi không
  có trong khung ảnh, chưa xác định đó là `/scan` hay `/odom`. Không gán kết quả
  cho một topic cụ thể trước khi người thực hiện xác nhận.
- **Ảnh odometry:** frame `odom`, tọa độ gần 0 và quaternion gần `(0, 0, 0, 1)`.
  Các pose liên tiếp gần như không thay đổi. Có thể minh chứng dữ liệu odometry
  khi đứng yên; chưa chứng minh odometry thay đổi khi robot di chuyển.

## Ảnh/bằng chứng cần bổ sung

1. Gazebo hiển thị robot và world rõ màu, không lỗi trắng/đen; thêm ảnh Gazebo
   cùng trạng thái với ảnh localization để đối chiếu pose.
2. `/scan` có tên lệnh, kiểu/header và dữ liệu khoảng cách. Ảnh tần số cần giữ
   cả lệnh `ros2 topic hz /scan` hoặc `ros2 topic hz /odom` trong khung ảnh.
3. `/odom` trước/sau khi robot di chuyển, nhìn rõ sự thay đổi position/orientation.
4. `/cmd_vel` thực tế dạng TwistStamped với vận tốc khác 0 khi nhấn phím; không
   chỉ dùng ảnh giao diện teleop thay cho dữ liệu topic.
5. Map khi đang khảo sát và map sau khảo sát; ảnh/log lưu YAML + PGM thành công.
6. Hai goal khác ở khu vực khác nhau; xác nhận goal nào ứng với ảnh reached đã có.
   Ưu tiên log `SUCCEEDED`/`status: 4` đúng UUID hoặc video/mốc thời gian.
7. Video để kiểm chứng quá trình tự di chuyển, không điều khiển thủ công và
   không va chạm; ảnh cuối một goal không thể hiện đầy đủ những điều này.

Các số thời gian/khoảng cách trên Navigation 2 panel là giá trị hiển thị tại
thời điểm chụp. Chỉ đưa vào bảng thực nghiệm khi đã đối chiếu đúng goal và
xác định cách đo; không tự suy ra thời gian chạy thực tế của cả quá trình.
