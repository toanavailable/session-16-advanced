# Bài tập Python Session 15 - Các hàm xử lý chuỗi & list

Tổng hợp 6 bài tập về **các hàm xử lý chuỗi (String)** và **list** kết hợp với **Function**, trong bối cảnh phần mềm bệnh viện Rikkei Hospital: sửa lỗi tính bất biến của chuỗi và tham chiếu list, xây dựng các hệ thống quản lý dữ liệu dạng list lồng nhau và list chứa chuỗi có ký tự phân cách.

## Thứ tự bài tập

| STT | Bài tập | Dạng bài | Kiến thức trọng tâm |
|---|---|---|---|
| 1 | [Lỗi chuẩn hóa dữ liệu bệnh án điện tử](bai-1-loi-chuan-hoa-du-lieu-benh-an-dien-tu/) | Sửa lỗi (legacy) | Chuỗi bất biến (phải gán lại kết quả `strip`, `title`); `append()` vs `extend()` |
| 2 | [Lỗi tham chiếu bộ nhớ và cập nhật đơn thuốc](bai-2-loi-tham-chieu-bo-nho-cap-nhat-don-thuoc/) | Sửa lỗi (legacy) | Aliasing (`b = a`), tạo bản sao `copy()` / `[:]` / `list()`; `replace()` rồi gán lại vào index |
| 3 | [Hệ thống quản lý bệnh nhân nội trú](bai-3-quan-ly-benh-nhan-noi-tru/) | Vận dụng chuyên sâu | List lồng nhau, helper `validate_gender`, `find_patient_index`; tìm kiếm không phân biệt hoa/thường |
| 4 | [Phân tích hệ thống quản lý hồ sơ bệnh án](bai-4-phan-tich-quan-ly-ho-so-benh-an/) | Phân tích | List chứa chuỗi `-`; `split` / `join`, `startswith`, cập nhật chuỗi bất biến, báo cáo theo độ tuổi |
| 5 | [Hệ thống phân loại & theo dõi sinh hiệu cấp cứu (ER Triage)](bai-5-phan-loai-theo-doi-sinh-hieu-cap-cuu/) | Sáng tạo | Chuỗi `\|`, bóc tách `"HR:115"` bằng `split(":")` → `float`; báo động đỏ; không dùng dict |
| 6 | [Hệ thống quản lý kho máu (Blood Bank)](bai-6-quan-ly-kho-mau/) | BTTH | CRUD trên list chứa chuỗi; xử lý nhóm máu âm (`O-`) trùng ký tự phân cách |

Mỗi thư mục bài có mã nguồn Python và `README.md` riêng (đề bài, phân tích, mã nguồn, kết quả chạy thử). Hai bài sửa lỗi có cả `script_legacy.py` (code lỗi gốc) và `script.py` (code đã sửa).

## Cách chạy

Yêu cầu Python 3.x. Vào thư mục bài cần chạy, ví dụ:

```bash
cd bai-1-loi-chuan-hoa-du-lieu-benh-an-dien-tu
python script.py

cd ../bai-6-quan-ly-kho-mau
python blood_bank.py
```
