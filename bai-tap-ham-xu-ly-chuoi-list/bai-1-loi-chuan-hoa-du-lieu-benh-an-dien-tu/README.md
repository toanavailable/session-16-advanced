# Bài 1 - Lỗi chuẩn hóa dữ liệu bệnh án điện tử

## Đề bài

Bệnh viện Đa khoa Rikkei triển khai hệ thống Bệnh án điện tử (EMR). Bác sĩ nhập "chẩn đoán bệnh" thường sai định dạng (thừa khoảng trắng, hoa/thường lộn xộn). Hàm `add_diagnosis` cần:
1. **Chuẩn hóa chuỗi:** xóa khoảng trắng thừa hai đầu, viết hoa chữ cái đầu mỗi từ (`"  vIEm phE QUan  "` → `"Viem Phe Quan"`).
2. **Cập nhật danh sách:** thêm chẩn đoán đã chuẩn hóa vào danh sách bệnh lý của bệnh nhân.

Kết quả đúng cần hiển thị:

```
Hồ sơ bệnh án (Các chẩn đoán): ['Sốt Xuất Huyết', 'Viem Phe Quan']
```

## Mã nguồn lỗi (Legacy Code)

File: [`script_legacy.py`](script_legacy.py)

```python
# Danh sách chẩn đoán hiện tại của bệnh nhân Nguyễn Văn A
patient_diagnoses = ["Sốt Xuất Huyết"]
# Hàm chuẩn hóa tên bệnh và thêm vào hồ sơ
def add_diagnosis(raw_diagnosis, current_list):
    # Cố gắng chuẩn hóa tên bệnh
    raw_diagnosis.strip()
    raw_diagnosis.title()
    # Thêm chẩn đoán vào danh sách bệnh án
    current_list.extend(raw_diagnosis)
    return current_list

# Bác sĩ nhập thêm một chẩn đoán mới bị lỗi định dạng
new_diagnosis = "  vIEm phE QUan  "

# Gọi hàm để xử lý và cập nhật hồ sơ
updated_diagnoses = add_diagnosis(new_diagnosis, patient_diagnoses)
print("Hồ sơ bệnh án (Các chẩn đoán):", updated_diagnoses)
```

Kết quả chạy:

```
Hồ sơ bệnh án (Các chẩn đoán): ['Sốt Xuất Huyết', ' ', ' ', 'v', 'I', 'E', 'm', ' ', 'p', 'h', 'E', ' ', 'Q', 'U', 'a', 'n', ' ', ' ']
```

Chương trình gặp 2 vấn đề: tên chẩn đoán vẫn thừa khoảng trắng và sai hoa/thường; thay vì thêm cả cụm tên bệnh, hồ sơ bị nhồi hàng loạt chữ cái và dấu cách rời rạc.

## (1) Phân tích lỗi

**Câu 1. Tại sao `raw_diagnosis.strip()` và `raw_diagnosis.title()` trong hàm không làm thay đổi giá trị của `raw_diagnosis`?**

Vì chuỗi (`str`) trong Python là kiểu **bất biến (immutable)**: một chuỗi đã tạo thì không sửa được nội dung. `strip()` và `title()` không sửa chuỗi gốc mà **tạo ra một chuỗi mới** rồi trả về. Hai dòng lệnh này không gán kết quả cho biến nào nên chuỗi mới bị bỏ đi, còn `raw_diagnosis` vẫn là `"  vIEm phE QUan  "`.

**Câu 2. Để kết quả xử lý chuỗi được lưu lại, cần sửa cú pháp gán biến thế nào?**

Gán kết quả trả về cho biến (gán lại chính biến đó hoặc biến mới). Có thể nối các phương thức trong một dòng:

```python
raw_diagnosis = raw_diagnosis.strip().title()
# hoặc
clean_diagnosis = raw_diagnosis.strip().title()
```

**Câu 3. `extend()` hoạt động thế nào khi tham số là một chuỗi? Vì sao kết quả có các ký tự `'v'`, `'I'`, `'E'`, `'m'` rời rạc?**

`extend(iterable)` **duyệt từng phần tử** của đối tượng được truyền vào và thêm lần lượt từng phần tử vào cuối list. Chuỗi cũng là một iterable, mà phần tử của chuỗi là **từng ký tự**. Vì vậy `extend("  vIEm phE QUan  ")` thêm 17 phần tử: 2 dấu cách đầu, `'v'`, `'I'`, `'E'`, `'m'`, dấu cách... Và vì chuỗi chưa được chuẩn hóa (câu 1), các ký tự vẫn giữ nguyên hoa/thường lộn xộn.

**Câu 4. Để thêm nguyên vẹn chuỗi `"Viem Phe Quan"` vào list, thay `extend()` bằng phương thức nào?**

Dùng **`append()`**: thêm **nguyên đối tượng** làm **một phần tử duy nhất** ở cuối list.

```python
current_list.append(clean_diagnosis)   # ['Sốt Xuất Huyết', 'Viem Phe Quan']
```

|  | `append(x)` | `extend(x)` |
|---|---|---|
| Thêm vào list | `x` là **1 phần tử** | **Từng phần tử** bên trong `x` |
| `x = "Viem"` | `[..., 'Viem']` | `[..., 'V', 'i', 'e', 'm']` |
| `x = [1, 2]` | `[..., [1, 2]]` | `[..., 1, 2]` |

## (2) Sửa lỗi

File: [`script.py`](script.py)

```python
"""Hồ sơ bệnh án điện tử - chuẩn hóa và thêm chẩn đoán (bản đã sửa lỗi)."""

# Danh sách chẩn đoán hiện tại của bệnh nhân Nguyễn Văn A
patient_diagnoses = ["Sốt Xuất Huyết"]


def add_diagnosis(raw_diagnosis, current_list):
    """Chuẩn hóa tên chẩn đoán và thêm vào danh sách bệnh án.

    raw_diagnosis (str): tên chẩn đoán bác sĩ nhập (có thể thừa khoảng trắng, sai hoa/thường)
    current_list (list): danh sách chẩn đoán hiện tại của bệnh nhân
    Trả về: list chẩn đoán sau khi thêm
    """
    # Sửa lỗi 1: chuỗi bất biến -> phải gán kết quả lại cho biến
    clean_diagnosis = raw_diagnosis.strip().title()
    # Sửa lỗi 2: append thêm NGUYÊN chuỗi là 1 phần tử (extend sẽ tách từng ký tự)
    current_list.append(clean_diagnosis)
    return current_list


# Bác sĩ nhập thêm một chẩn đoán mới bị lỗi định dạng
new_diagnosis = "  vIEm phE QUan  "

# Gọi hàm để xử lý và cập nhật hồ sơ
updated_diagnoses = add_diagnosis(new_diagnosis, patient_diagnoses)
print("Hồ sơ bệnh án (Các chẩn đoán):", updated_diagnoses)
```

## Kết quả

```
Hồ sơ bệnh án (Các chẩn đoán): ['Sốt Xuất Huyết', 'Viem Phe Quan']
```

Tên chẩn đoán đã được chuẩn hóa và thêm đúng **một phần tử** vào hồ sơ, console in đúng 1 dòng như yêu cầu.
