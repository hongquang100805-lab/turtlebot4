# Báo cáo TurtleBot 4 — mã LaTeX đầy đủ

File chính: **main.tex**. Biên dịch bằng **XeLaTeX**, không dùng pdfLaTeX vì
báo cáo sử dụng `fontspec` và tiếng Việt Unicode.

## Dùng trên Overleaf

1. Tạo project bằng cách tải file ZIP `bao_cao_tb4_latex.zip`.
2. Chọn main document là `main.tex`, compiler là **XeLaTeX**.
3. Biên dịch; giữ thư mục `figures/` cùng cấp với `main.tex`.
4. Sửa các macro thông tin ở đầu `main.tex`: trường, khoa, học phần, giảng viên,
   họ tên, mã sinh viên, lớp và địa điểm.
5. Sửa `\linkGithub` và `\linkVideo`. Với liên kết thật, dùng ví dụ:

```latex
\newcommand{\linkGithub}{\url{https://github.com/ten-tai-khoan/ten-repo}}
\newcommand{\linkVideo}{\url{https://drive.google.com/duong-dan-video}}
```

Không dán thêm hai dòng định nghĩa nếu macro đã có; thay nội dung dòng cũ.

## Biên dịch trên máy có TeX Live/XeLaTeX

Chạy tại thư mục chứa `main.tex`:

```bash
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Hoặc:

```bash
latexmk -xelatex main.tex
```

Lần biên dịch thứ hai cập nhật mục lục và tham chiếu hình/bảng.
Nếu Times New Roman chưa có, source tự dùng Liberation Serif hoặc TeX Gyre
Termes. Các sơ đồ đã xuất thành PDF vector; không cần Graphviz để biên dịch.

## Nội dung và ảnh

Báo cáo gồm bìa, mục lục, bảy chương, bảng kết quả và tài liệu tham khảo.
Các ảnh screenshot được giữ nguyên nội dung. Hình bản đồ được dựng trực tiếp
từ `depot_02.pgm` theo resolution/origin của YAML. Thư mục `maps/` lưu bản sao
cặp map dùng để dựng hình.

Bộ minh chứng hiện có xác nhận một ảnh Nav2 có Feedback reached. Source đã
viết nội dung hoàn chỉnh theo bằng chứng này, **không tự khẳng định ba goal
thành công hoặc toàn bộ quá trình không va chạm**. Hai goal còn lại được ghi
là chưa có minh chứng đính kèm, không phải kết luận chưa thực hiện.

Trước khi nộp, bổ sung ảnh/log/video còn thiếu rồi cập nhật bảng goal và đoạn
kết luận tương ứng. Nếu thay file hình, cập nhật đúng đường dẫn trong source.
Ảnh tần số và odometry gửi trực tiếp trong chat chưa có file gốc trong bộ
ảnh, nên chỉ được mô tả trong phần nhận xét, không gán topic chưa xác nhận.

## Các file chính

- `main.tex`: toàn bộ mã LaTeX.
- `figures/*.pdf`: năm sơ đồ vector và hình bản đồ.
- `figures/*.png`: ba screenshot gốc và bản PNG của hình map.
- `maps/depot_02.{yaml,pgm}`: map thực nghiệm dùng trong báo cáo.
- `README_LATEX.md`: hướng dẫn sử dụng source.

Nếu có `main.pdf`, xem `BUILD_STATUS.md` để biết cách kiểm tra/biên dịch đã
thực hiện. Các kiểm tra source tĩnh không thay thế kiểm tra PDF sau biên dịch.
