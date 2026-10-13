# Kiểm tra bản dành cho pdfLaTeX

- Đã biên dịch thành công `main.tex` bằng **pdfLaTeX**, pdfTeX 1.40.29 / TeX Live 2026.
- Đã chạy hai lượt để cập nhật mục lục, tham chiếu và liên kết PDF.
- `main.pdf`: **21 trang A4**, có bìa, mục lục, 7 phần nội dung và tài liệu tham khảo.
- Tiếng Việt dùng UTF-8, font encoding T5, Babel và Latin Modern.
- Source không dùng `fontspec`, `polyglossia` hoặc font hệ thống.
- Log cuối không có lỗi, cảnh báo `Overfull`, `Missing character`, tham chiếu
  `undefined` hoặc cảnh báo thay thế font.
- Đã kiểm tra văn bản tiếng Việt trích từ PDF, bìa, đường dẫn hình và cặp label/ref.
- Còn một số cảnh báo Underfull ở bảng; không chặn biên dịch.

Bản pdfLaTeX thay thế bản XeLaTeX trước đó. Số trang có thể khác giữa các phiên
bản TeX Live; các ảnh và nội dung thực nghiệm được giữ nguyên.

Công cụ TinyTeX kiểm tra được giải nén dưới `/tmp`, kiểm tra checksum chính
thức trước khi chạy; các gói bổ sung cũng nằm trong bản TinyTeX tạm. Không cài
TeX vào hệ thống và không thay đổi cấu hình shell toàn cục.

Đây là kiểm tra tài liệu, không phải kiểm tra lại robot/SLAM/Nav2. Nội dung kết
quả chỉ dựa trên bản đồ, log đã lưu và ảnh người thực hiện cung cấp. Trước khi
nộp cần bổ sung thông tin cá nhân, liên kết và minh chứng hai goal khác.
