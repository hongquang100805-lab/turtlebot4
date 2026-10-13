# Kiểm tra mã LaTeX và PDF

- Đã biên dịch thành công `main.tex` bằng Tectonic 0.17.0 (engine XeTeX).
- `main.pdf`: 19 trang A4, có bìa, mục lục, 7 phần nội dung và tài liệu tham khảo.
- Đã kiểm tra cặp environment, đường dẫn hình, label/ref và citation/bibitem.
- Đã kiểm tra cú pháp shell trong các listing.
- Log cuối không có `Overfull`, `Missing character` hay tham chiếu `undefined`.
- Đã xem các trang đại diện: bìa, phần mapping, hình bản đồ và ảnh navigation.
- Hình bản đồ trong báo cáo dùng PNG từ PGM thật để tránh lỗi nhúng ảnh bên
  trong PDF trung gian của trình biên dịch tạm. File PDF riêng của map vẫn
  được cung cấp; sơ đồ kiến trúc dùng PDF vector.

Còn các cảnh báo không chặn biên dịch: Underfull ở một số bảng, deprecation
của package trong bundle và khác phiên bản PDF của sơ đồ so với PDF đầu ra.
Font hệ thống được dùng khi biên dịch; máy khác có thể dùng font dự phòng
được định nghĩa trong source, nên phân trang có thể khác đôi chút.

Các công cụ/cache biên dịch tạm được đặt dưới `/tmp`; không cài TeX vào hệ
thống và không thay đổi cấu hình shell toàn cục. Đây là kiểm tra tài liệu,
không phải kiểm tra lại robot/SLAM/Nav2.

Nội dung kết quả chỉ dựa trên map, log kiểm tra đã lưu và các ảnh người thực
hiện cung cấp. Cần bổ sung thông tin cá nhân, liên kết nộp bài và minh chứng
hai goal khác trước khi coi báo cáo là bản nghiệm thu đầy đủ.
