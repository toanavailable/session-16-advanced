# Bài 2 - Lỗi tham chiếu bộ nhớ và cập nhật đơn thuốc bệnh nhân

## Đề bài

Hệ thống "Quản lý Đơn thuốc Nội trú" có tính năng "Sao chép đơn thuốc": lấy đơn hôm qua làm đơn hôm nay rồi chỉnh sửa. Hàm `update_prescription` cần:
1. **Thay thế chuỗi:** đổi `"Panadol"` thành `"Paracetamol"` (tên gốc theo quy định Bộ Y tế).
2. **Cập nhật list:** thêm `"Oresol"` vào cuối đơn hôm nay.

**Yêu cầu quan trọng:** đơn thuốc hôm qua phải được giữ nguyên vẹn để làm lịch sử bệnh án. Kết quả đúng:

```
Đơn thuốc hôm qua: ['Panadol', 'Vitamin C', 'Amoxicillin']
Đơn thuốc hôm nay: ['Paracetamol', 'Vitamin C', 'Amoxicillin', 'Oresol']
```

## Mã nguồn lỗi (Legacy Code)

File: [`script_legacy.py`](script_legacy.py)

```python
# Danh sách thuốc ngày hôm qua (Lịch sử bệnh án cần giữ nguyên)
yesterday_prescription = ["Panadol", "Vitamin C", "Amoxicillin"]

# Hàm tạo và cập nhật đơn thuốc cho ngày mới
def update_prescription(old_prescription):
    # Lập trình viên cố gắng sao chép đơn thuốc sang ngày mới
    new_prescription = old_prescription
    # Cố gắng đổi tên thuốc ở vị trí đầu tiên (index 0) từ Panadol thành Paracetamol
    new_prescription[0].replace("Panadol", "Paracetamol")
    # Thêm thuốc mới cho ngày hôm nay
    new_prescription.append("Oresol")
    return new_prescription

# Hệ thống chạy cấp thuốc cho ngày hôm nay
today_prescription = update_prescription(yesterday_prescription)
print("Đơn thuốc hôm qua:", yesterday_prescription)
print("Đơn thuốc hôm nay:", today_prescription)
```

Kết quả chạy:

```
Đơn thuốc hôm qua: ['Panadol', 'Vitamin C', 'Amoxicillin', 'Oresol']
Đơn thuốc hôm nay: ['Panadol', 'Vitamin C', 'Amoxicillin', 'Oresol']
```

Hai vấn đề: thuốc "Oresol" bị chèn trái phép vào đơn **hôm qua** (hỏng dữ liệu lịch sử), và "Panadol" ở đơn hôm nay vẫn chưa đổi thành "Paracetamol".

## (1) Phân tích lỗi

**Câu 1. Tại sao `new_prescription.append("Oresol")` lại làm thay đổi `yesterday_prescription` ở ngoài hàm? Bản chất của `new_prescription = old_prescription` là gì?**

Biến trong Python là **"nhãn" trỏ tới đối tượng** trong bộ nhớ. Khi gọi hàm, `old_prescription` trỏ tới **chính list** `yesterday_prescription`. Lệnh gán `new_prescription = old_prescription` **không tạo list mới**: nó chỉ gắn thêm một nhãn thứ hai lên cùng list đó (hiện tượng **aliasing - tham chiếu**). Cả ba tên `yesterday_prescription`, `old_prescription`, `new_prescription` đều trỏ vào **cùng một vùng nhớ**. List là kiểu **mutable**, nên `append()` qua bất kỳ nhãn nào cũng sửa chính list đó, và đơn hôm qua bị thêm "Oresol".

```python
a = ["Panadol"]
b = a
print(a is b)   # True: cùng một đối tượng
```

**Câu 2. Để tạo bản sao độc lập, dùng những cách nào? (ít nhất 2 cách)**

```python
new_prescription = old_prescription.copy()   # Cách 1: phương thức copy()
new_prescription = old_prescription[:]       # Cách 2: slicing toàn bộ list
new_prescription = list(old_prescription)    # Cách 3: hàm list()
```

Cả ba cách tạo **list mới** chứa cùng các phần tử, nên `new_prescription is old_prescription` là `False`. Thêm hay xóa phần tử trên bản sao không ảnh hưởng list gốc. (Đây là bản sao "nông". Với list chứa các chuỗi bất biến như đơn thuốc thì như vậy là đủ.)

**Câu 3. Tại sao `new_prescription[0].replace("Panadol", "Paracetamol")` không có tác dụng?**

`new_prescription[0]` là chuỗi `"Panadol"`, mà chuỗi là **bất biến**. `replace()` không sửa chuỗi đó mà **trả về chuỗi mới** `"Paracetamol"`. Kết quả này không được gán vào đâu nên bị bỏ đi, phần tử index 0 của list vẫn là `"Panadol"`.

**Câu 4. Cần sửa cú pháp câu 3 thế nào để phần tử index 0 thực sự được cập nhật?**

Gán chuỗi mới ngược lại vào **đúng vị trí index 0** của list (list cho phép gán đè phần tử):

```python
new_prescription[0] = new_prescription[0].replace("Panadol", "Paracetamol")
```

## (2) Sửa lỗi

File: [`script.py`](script.py)

```python
"""Quản lý đơn thuốc nội trú - sao chép và cập nhật đơn thuốc (bản đã sửa lỗi)."""

# Danh sách thuốc ngày hôm qua (Lịch sử bệnh án cần giữ nguyên)
yesterday_prescription = ["Panadol", "Vitamin C", "Amoxicillin"]


def update_prescription(old_prescription):
    """Tạo đơn thuốc ngày mới từ đơn cũ mà không làm thay đổi đơn cũ.

    old_prescription (list): đơn thuốc ngày hôm qua
    Trả về: list đơn thuốc mới (đã đổi Panadol -> Paracetamol và thêm Oresol)
    """
    # Sửa lỗi 1: tạo bản sao độc lập thay vì chỉ gán thêm một "nhãn" cho cùng list
    new_prescription = old_prescription.copy()
    # Sửa lỗi 2: replace() trả về chuỗi mới -> gán lại vào đúng vị trí index 0
    new_prescription[0] = new_prescription[0].replace("Panadol", "Paracetamol")
    # Thêm thuốc mới cho ngày hôm nay (chỉ ảnh hưởng bản sao)
    new_prescription.append("Oresol")
    return new_prescription


# Hệ thống chạy cấp thuốc cho ngày hôm nay
today_prescription = update_prescription(yesterday_prescription)
print("Đơn thuốc hôm qua:", yesterday_prescription)
print("Đơn thuốc hôm nay:", today_prescription)
```

## Kết quả

```
Đơn thuốc hôm qua: ['Panadol', 'Vitamin C', 'Amoxicillin']
Đơn thuốc hôm nay: ['Paracetamol', 'Vitamin C', 'Amoxicillin', 'Oresol']
```

Lịch sử đơn thuốc hôm qua được giữ nguyên; đơn hôm nay đã đổi tên thuốc và thêm thuốc mới thành công, console in đúng 2 dòng như yêu cầu.
