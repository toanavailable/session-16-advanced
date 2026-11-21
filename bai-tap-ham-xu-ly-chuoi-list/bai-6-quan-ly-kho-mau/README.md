# Bài 6 - BTTH: Hệ thống quản lý kho máu (Blood Bank Management System)

## Mục tiêu

- **Function:** chia nhỏ chương trình thành các hàm độc lập để tái sử dụng và quản lý logic nghiệp vụ.
- **CRUD với List:** Thêm (`append`), Xem (duyệt `for`), Sửa (gán đè qua index), Xóa (`pop`).
- **Xử lý chuỗi:** `.split()`, `.join()`, `.upper()`, `.title()`, `.strip()` để chuẩn hóa và bóc tách dữ liệu.
- **Tính bất biến của String:** cập nhật một chuỗi trong danh sách bằng cách tách → sửa → ghép → gán đè.
- **Control Flow:** menu tương tác console.

## Đề bài

Khoa Huyết học Bệnh viện Rikkei cần phần mềm terminal quản lý kho máu dự trữ. Dữ liệu là **list các chuỗi**; mỗi chuỗi là một túi máu, các trường nối bằng dấu `-` theo thứ tự: **Mã túi máu - Tên người hiến - Nhóm máu - Thể tích (ml) - Ngày hết hạn**. Mỗi chức năng là một hàm riêng; `main()` chỉ hiển thị menu và gọi hàm.

```python
blood_inventory = [
    "BL001-Nguyen Van A-O+-250-31/12/2026",
    "BL002-Tran Thi B-A--350-15/11/2026",
    "BL003-Le Van C-AB+-250-20/10/2026"
]
```

### Menu

```
=== HỆ THỐNG QUẢN LÝ KHO MÁU RIKKEI ===
1. Xem danh sách túi máu trong kho
2. Nhập túi máu mới
3. Gia hạn / Sửa ngày hết hạn
4. Xuất / Hủy túi máu
5. Thoát chương trình
=======================================
Chọn chức năng (1-5):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Xem kho | `display_inventory(inventory)` | Bóc tách chuỗi, in bảng, cộng dồn **tổng thể tích máu**; rỗng: "Kho máu hiện chưa có túi máu nào." |
| 2. Nhập túi máu | `add_blood_bag(inventory)` | Mã túi & nhóm máu: xóa khoảng trắng, in hoa (`o+` → `O+`); tên: Title case (`lê văn d` → `Lê Văn D`); mã không trùng; ghép bằng `join()` |
| 3. Gia hạn | `update_expiry(inventory)` | Tách chuỗi → đổi ngày hết hạn (phần tử cuối, index 4) → ghép → gán đè |
| 4. Xuất / Hủy | `remove_blood_bag(inventory)` | Tìm mã, xóa bằng `pop()`; không thấy thì báo lỗi |
| 5. Thoát | `main()` | "Cảm ơn bác sĩ đã sử dụng hệ thống. Hẹn gặp lại!" |

## Phân tích và thiết kế

### Vấn đề cốt lõi: nhóm máu âm chứa chính ký tự phân cách

Dữ liệu mẫu `"BL002-Tran Thi B-A--350-15/11/2026"` có nhóm máu `A-`. Dấu `-` của nhóm máu **trùng với dấu phân cách**, nên `split("-")` không cho ra 5 phần mà là 6:

```python
"BL005-Pham Thi Hoa-O--350-12/12/2026".split("-")
# ['BL005', 'Pham Thi Hoa', 'O', '', '350', '12/12/2026']   <- 6 phần, nhóm máu bị vỡ
```

Nếu làm theo cách đơn giản là sửa `parts[4]` để gia hạn, chương trình sẽ ghi ngày mới đè vào **thể tích** của túi máu nhóm âm, gây sai dữ liệu nghiêm trọng. Hàm `parse_record` giải quyết như sau:
- Mã túi (`parts[0]`) và tên (`parts[1]`) luôn ở đầu; thể tích (`parts[-2]`) và ngày hết hạn (`parts[-1]`) luôn ở cuối.
- **Phần ở giữa** (`parts[2:-2]`) ghép lại bằng `"-".join(...)` chính là nhóm máu: `['O', '']` → `"O-"`, `['O+']` → `"O+"`.

```python
parse_record("BL005-Pham Thi Hoa-O--350-12/12/2026")
# ['BL005', 'Pham Thi Hoa', 'O-', '350', '12/12/2026']        <- luôn đúng 5 phần
```

Sau đó `build_record(fields)` = `"-".join(fields)` ghép lại chính xác. Tương tự, dấu `-` trong tên người hiến được đổi thành khoảng trắng trước khi lưu.

### Input / Output các hàm

| Hàm | Input | Output | Ghi chú |
|---|---|---|---|
| `parse_record(record)` | `str` | `list[str]` 5 phần tử | Tách an toàn với nhóm máu âm |
| `build_record(fields)` | `list[str]` | `str` | `"-".join(fields)` |
| `normalize_code(raw_code)` | `str` | `str` | Xóa khoảng trắng, in hoa (mã túi, nhóm máu) |
| `find_bag_index(inventory, bag_id)` | `list[str]`, `str` | `int` index / -1 | `startswith(bag_id + "-")` |
| `is_valid_date(date_text)` | `str` | `bool` | Định dạng DD/MM/YYYY |
| `read_bag_id(prompt)` | `str` | `str` (`""` nếu trống) | In lỗi khi trống |
| `display_inventory(inventory)` | `list[str]` | `None` | Chức năng 1 |
| `add_blood_bag(inventory)` | `list[str]` | `None` | Chức năng 2, `append()` |
| `update_expiry(inventory)` | `list[str]` | `None` | Chức năng 3, gán đè `inventory[i]` |
| `remove_blood_bag(inventory)` | `list[str]` | `None` | Chức năng 4, `pop(i)` |
| `main()` | không | `None` | Chỉ menu và gọi hàm |

### Cập nhật chuỗi trong list (chức năng 3)

```
fields ← parse_record(inventory[i])     # chuỗi bất biến -> list tạm 5 phần tử
fields[4] ← ngày_mới                    # sửa phần tử cuối
inventory[i] ← build_record(fields)     # join thành chuỗi mới, gán đè đúng vị trí
```

## Triển khai code

File: [`blood_bank.py`](blood_bank.py)

Mã nguồn có **11 hàm**: `main` + 4 hàm chức năng + `display_menu` + 5 hàm phụ trợ.

```python
"""Blood Bank Management System - Hệ thống quản lý kho máu Rikkei.

Mỗi túi máu là MỘT chuỗi: "Mã túi-Tên người hiến-Nhóm máu-Thể tích-Ngày hết hạn".
"""

SEPARATOR = "-"
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


# =====================================================================
# CÁC HÀM PHỤ TRỢ
# =====================================================================
def parse_record(record):
    """Tách chuỗi túi máu thành list 5 phần tử [mã, tên, nhóm máu, thể tích, ngày hết hạn].

    Nhóm máu âm ("O-", "AB-") chứa chính dấu "-" nên split("-") sinh thêm phần tử rỗng.
    Vì vậy lấy mã, tên ở đầu; thể tích, ngày ở cuối; phần còn lại ghép lại là nhóm máu.
    Trả về: list[str] gồm đúng 5 phần tử
    """
    parts = record.split(SEPARATOR)
    blood_group = SEPARATOR.join(parts[2:-2])
    return [parts[0], parts[1], blood_group, parts[-2], parts[-1]]


def build_record(fields):
    """Ghép list 5 phần tử thành chuỗi lưu trữ bằng join(). Trả về str."""
    return SEPARATOR.join(fields)


def normalize_code(raw_code):
    """Xóa mọi khoảng trắng và viết hoa (dùng cho mã túi và nhóm máu). Trả về str."""
    return "".join(raw_code.split()).upper()


def find_bag_index(inventory, bag_id):
    """Tìm vị trí túi máu có mã bag_id. Trả về index, hoặc -1 nếu không có."""
    for index, record in enumerate(inventory):
        if record.startswith(bag_id + SEPARATOR):
            return index
    return -1


def is_valid_date(date_text):
    """Kiểm tra ngày dạng DD/MM/YYYY (đúng vị trí dấu "/" và các phần còn lại là số)."""
    parts = date_text.split("/")
    return (len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4
            and "".join(parts).isdigit()
            and 1 <= int(parts[0]) <= 31 and 1 <= int(parts[1]) <= 12)


def read_bag_id(prompt):
    """Nhập và chuẩn hóa mã túi máu; in lỗi và trả về "" nếu để trống."""
    bag_id = normalize_code(input(prompt))
    if bag_id == "":
        print("\nLỗi: Mã túi máu không được để trống!")
    return bag_id


# =====================================================================
# CÁC HÀM NGHIỆP VỤ
# =====================================================================
def display_menu():
    """In menu và trả về lựa chọn (str)."""
    print("\n=== HỆ THỐNG QUẢN LÝ KHO MÁU RIKKEI ===")
    print("1. Xem danh sách túi máu trong kho")
    print("2. Nhập túi máu mới")
    print("3. Gia hạn / Sửa ngày hết hạn")
    print("4. Xuất / Hủy túi máu")
    print("5. Thoát chương trình")
    print("=" * 39)
    return input("Chọn chức năng (1-5): ").strip()


def display_inventory(inventory):
    """Chức năng 1: in bảng túi máu và tổng thể tích máu đang có. Trả về None."""
    if len(inventory) == 0:
        print("Kho máu hiện chưa có túi máu nào.")
        return
    print("--- DANH SÁCH KHO MÁU ---")
    print(f"{'Mã Túi':<7}| {'Người Hiến':<17}| {'Nhóm Máu':<9}| {'Thể Tích':<9}| Ngày Hết Hạn")
    print("-" * 64)
    total_volume = 0
    for record in inventory:
        bag_id, donor, blood_group, volume, expiry = parse_record(record)
        total_volume += int(volume)
        print(f"{bag_id:<7}| {donor:<17}| {blood_group:<9}| {volume + ' ml':<9}| {expiry}")
    print("-" * 64)
    print(f"Tổng thể tích máu trong kho: {total_volume} ml.")


def add_blood_bag(inventory):
    """Chức năng 2: nhập, chuẩn hóa, ghép bằng join() rồi append vào inventory."""
    print("\n--- NHẬP TÚI MÁU MỚI ---")
    bag_id = read_bag_id("Nhập mã túi máu mới: ")
    if bag_id == "":
        return
    if find_bag_index(inventory, bag_id) != -1:
        print(f"\nLỗi: Mã túi máu {bag_id} đã tồn tại! Vui lòng nhập mã khác.")
        return

    donor = " ".join(input("Nhập tên người hiến: ").replace(SEPARATOR, " ").split()).title()
    if donor == "":
        print("\nLỗi: Tên người hiến không được để trống!")
        return

    blood_group = normalize_code(input("Nhập nhóm máu: "))
    if blood_group not in BLOOD_GROUPS:
        print("\nLỗi: Nhóm máu không hợp lệ (A+, A-, B+, B-, AB+, AB-, O+, O-)!")
        return

    volume = input("Nhập thể tích (ml): ").strip()
    if not volume.isdigit() or int(volume) <= 0:
        print("\nLỗi: Thể tích phải là số nguyên lớn hơn 0!")
        return
    volume = str(int(volume))                       # bỏ số 0 thừa ở đầu, ví dụ "0250"

    expiry = input("Nhập ngày hết hạn (DD/MM/YYYY): ").strip()
    if not is_valid_date(expiry):
        print("\nLỗi: Ngày hết hạn phải đúng định dạng DD/MM/YYYY!")
        return

    new_record = build_record([bag_id, donor, blood_group, volume, expiry])
    inventory.append(new_record)
    print(f"\nThành công: Đã nhập túi máu {bag_id} vào kho!")
    print("\nSau khi chuẩn hóa, dữ liệu được lưu vào list là:")
    print(new_record)


def update_expiry(inventory):
    """Chức năng 3: tách chuỗi -> sửa ngày hết hạn (index 4) -> join() -> gán đè vào inventory."""
    print("\n--- GIA HẠN / SỬA NGÀY HẾT HẠN ---")
    bag_id = read_bag_id("Nhập mã túi máu cần cập nhật: ")
    if bag_id == "":
        return
    index = find_bag_index(inventory, bag_id)
    if index == -1:
        print(f"\nLỗi: Không tìm thấy túi máu {bag_id} trong kho!")
        return

    new_expiry = input("Nhập ngày hết hạn mới: ").strip()
    if not is_valid_date(new_expiry):
        print("\nLỗi: Ngày hết hạn phải đúng định dạng DD/MM/YYYY!")
        return
    fields = parse_record(inventory[index])      # chuỗi bất biến -> tách ra list tạm
    fields[4] = new_expiry                       # sửa phần tử cuối (ngày hết hạn)
    inventory[index] = build_record(fields)      # ghép lại, ghi đè vị trí cũ
    print(f"\nThành công: Đã cập nhật ngày hết hạn cho túi máu {bag_id}!")


def remove_blood_bag(inventory):
    """Chức năng 4: xóa túi máu khỏi kho bằng pop(index)."""
    print("--- XUẤT / HỦY TÚI MÁU ---")
    bag_id = read_bag_id("Nhập mã túi máu cần xuất/hủy: ")
    if bag_id == "":
        return
    index = find_bag_index(inventory, bag_id)
    if index == -1:
        print(f"\nLỗi: Không tìm thấy túi máu {bag_id} trong kho!")
        return
    inventory.pop(index)
    print(f"\nThành công: Đã xuất túi máu {bag_id} khỏi kho!")


# =====================================================================
# HÀM MAIN: chỉ hiển thị menu và gọi các hàm chức năng
# =====================================================================
def main():
    blood_inventory = [
        "BL001-Nguyen Van A-O+-250-31/12/2026",
        "BL002-Tran Thi B-A--350-15/11/2026",
        "BL003-Le Van C-AB+-250-20/10/2026",
    ]
    while True:
        choice = display_menu()
        if choice == "1":
            display_inventory(blood_inventory)
        elif choice == "2":
            add_blood_bag(blood_inventory)
        elif choice == "3":
            update_expiry(blood_inventory)
        elif choice == "4":
            remove_blood_bag(blood_inventory)
        elif choice == "5":
            print("Cảm ơn bác sĩ đã sử dụng hệ thống. Hẹn gặp lại!")
            break
        else:
            print("\nLựa chọn không hợp lệ, vui lòng nhập số từ 1-5!")


if __name__ == "__main__":
    main()
```

## Kết quả

Chạy thử toàn bộ chức năng và các tình huống lỗi *(ẩn menu lặp lại)*:

```
Chọn chức năng (1-5): 1
--- DANH SÁCH KHO MÁU ---
Mã Túi | Người Hiến       | Nhóm Máu | Thể Tích | Ngày Hết Hạn
----------------------------------------------------------------
BL001  | Nguyen Van A     | O+       | 250 ml   | 31/12/2026
BL002  | Tran Thi B       | A-       | 350 ml   | 15/11/2026
BL003  | Le Van C         | AB+      | 250 ml   | 20/10/2026
----------------------------------------------------------------
Tổng thể tích máu trong kho: 850 ml.

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: bl004
Nhập tên người hiến: lê văn d
Nhập nhóm máu: b+
Nhập thể tích (ml): 250
Nhập ngày hết hạn (DD/MM/YYYY): 01/01/2027

Thành công: Đã nhập túi máu BL004 vào kho!

Sau khi chuẩn hóa, dữ liệu được lưu vào list là:
BL004-Lê Văn D-B+-250-01/01/2027

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL001

Lỗi: Mã túi máu BL001 đã tồn tại! Vui lòng nhập mã khác.

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới:    bl005
Nhập tên người hiến: phạm thị hoa
Nhập nhóm máu:    o-
Nhập thể tích (ml): 350
Nhập ngày hết hạn (DD/MM/YYYY): 12/12/2026

Thành công: Đã nhập túi máu BL005 vào kho!

Sau khi chuẩn hóa, dữ liệu được lưu vào list là:
BL005-Phạm Thị Hoa-O--350-12/12/2026

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới:  

Lỗi: Mã túi máu không được để trống!

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL006
Nhập tên người hiến:  

Lỗi: Tên người hiến không được để trống!

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL006
Nhập tên người hiến: Nguyen Van E
Nhập nhóm máu: A+
Nhập thể tích (ml): hai trăm năm mươi

Lỗi: Thể tích phải là số nguyên lớn hơn 0!

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL006
Nhập tên người hiến: Nguyen Van E
Nhập nhóm máu: A+
Nhập thể tích (ml): 0

Lỗi: Thể tích phải là số nguyên lớn hơn 0!

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL006
Nhập tên người hiến: Nguyen Van E
Nhập nhóm máu: C+

Lỗi: Nhóm máu không hợp lệ (A+, A-, B+, B-, AB+, AB-, O+, O-)!

Chọn chức năng (1-5): 2

--- NHẬP TÚI MÁU MỚI ---
Nhập mã túi máu mới: BL006
Nhập tên người hiến: Nguyen Van E
Nhập nhóm máu: A+
Nhập thể tích (ml): 250
Nhập ngày hết hạn (DD/MM/YYYY): 2026-12-31

Lỗi: Ngày hết hạn phải đúng định dạng DD/MM/YYYY!

Chọn chức năng (1-5): 1
--- DANH SÁCH KHO MÁU ---
Mã Túi | Người Hiến       | Nhóm Máu | Thể Tích | Ngày Hết Hạn
----------------------------------------------------------------
BL001  | Nguyen Van A     | O+       | 250 ml   | 31/12/2026
BL002  | Tran Thi B       | A-       | 350 ml   | 15/11/2026
BL003  | Le Van C         | AB+      | 250 ml   | 20/10/2026
BL004  | Lê Văn D         | B+       | 250 ml   | 01/01/2027
BL005  | Phạm Thị Hoa     | O-       | 350 ml   | 12/12/2026
----------------------------------------------------------------
Tổng thể tích máu trong kho: 1450 ml.

Chọn chức năng (1-5): 3

--- GIA HẠN / SỬA NGÀY HẾT HẠN ---
Nhập mã túi máu cần cập nhật: BL001
Nhập ngày hết hạn mới: 15/01/2027

Thành công: Đã cập nhật ngày hết hạn cho túi máu BL001!

Chọn chức năng (1-5): 3

--- GIA HẠN / SỬA NGÀY HẾT HẠN ---
Nhập mã túi máu cần cập nhật: bl003
Nhập ngày hết hạn mới: 25/12/2026

Thành công: Đã cập nhật ngày hết hạn cho túi máu BL003!

Chọn chức năng (1-5): 3

--- GIA HẠN / SỬA NGÀY HẾT HẠN ---
Nhập mã túi máu cần cập nhật: BL999

Lỗi: Không tìm thấy túi máu BL999 trong kho!

Chọn chức năng (1-5): 3

--- GIA HẠN / SỬA NGÀY HẾT HẠN ---
Nhập mã túi máu cần cập nhật:  

Lỗi: Mã túi máu không được để trống!

Chọn chức năng (1-5): 3

--- GIA HẠN / SỬA NGÀY HẾT HẠN ---
Nhập mã túi máu cần cập nhật: bl005
Nhập ngày hết hạn mới: 1/1/27

Lỗi: Ngày hết hạn phải đúng định dạng DD/MM/YYYY!

Chọn chức năng (1-5): 4
--- XUẤT / HỦY TÚI MÁU ---
Nhập mã túi máu cần xuất/hủy: BL002

Thành công: Đã xuất túi máu BL002 khỏi kho!

Chọn chức năng (1-5): 4
--- XUẤT / HỦY TÚI MÁU ---
Nhập mã túi máu cần xuất/hủy: bl003

Thành công: Đã xuất túi máu BL003 khỏi kho!

Chọn chức năng (1-5): 4
--- XUẤT / HỦY TÚI MÁU ---
Nhập mã túi máu cần xuất/hủy: BL999

Lỗi: Không tìm thấy túi máu BL999 trong kho!

Chọn chức năng (1-5): 4
--- XUẤT / HỦY TÚI MÁU ---
Nhập mã túi máu cần xuất/hủy:  

Lỗi: Mã túi máu không được để trống!

Chọn chức năng (1-5): 1
--- DANH SÁCH KHO MÁU ---
Mã Túi | Người Hiến       | Nhóm Máu | Thể Tích | Ngày Hết Hạn
----------------------------------------------------------------
BL001  | Nguyen Van A     | O+       | 250 ml   | 15/01/2027
BL004  | Lê Văn D         | B+       | 250 ml   | 01/01/2027
BL005  | Phạm Thị Hoa     | O-       | 350 ml   | 12/12/2026
----------------------------------------------------------------
Tổng thể tích máu trong kho: 850 ml.

Chọn chức năng (1-5): 9

Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Chọn chức năng (1-5): abc

Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Chọn chức năng (1-5): 

Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Chọn chức năng (1-5): 5
Cảm ơn bác sĩ đã sử dụng hệ thống. Hẹn gặp lại!
```

Kho rỗng (gọi trực tiếp `display_inventory([])`):

```
Kho máu hiện chưa có túi máu nào.
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Xem kho mẫu | Chọn 1 | 3 túi, tổng 850 ml (khớp đề) |
| Nhập hợp lệ | `bl004`, `lê văn d`, `b+`, 250, 01/01/2027 | `BL004-Lê Văn D-B+-250-01/01/2027` (khớp đề) |
| Trùng mã | `BL001` | Lỗi: Mã túi máu BL001 đã tồn tại! (khớp đề) |
| Mã có khoảng trắng, nhóm máu âm | `   bl005`, `   o-` | Lưu BL005 nhóm `O-` (khớp đề) |
| Mã / tên rỗng | khoảng trắng | Lỗi: ... không được để trống! (khớp đề) |
| Thể tích là chữ / bằng 0 | `hai trăm năm mươi`, `0` | Lỗi: Thể tích phải là số nguyên lớn hơn 0! (khớp đề) |
| Nhóm máu sai / ngày sai định dạng | `C+`; `2026-12-31` | Báo lỗi |
| Xem kho sau khi nhập | Chọn 1 | 5 túi, BL005 hiển thị đúng `O-`, tổng 1450 ml |
| Gia hạn | `BL001` → 15/01/2027; `bl003` → 25/12/2026 | Thành công (khớp đề) |
| Gia hạn mã sai / rỗng / ngày sai | `BL999`; khoảng trắng; `1/1/27` | Báo lỗi (khớp đề) |
| Xuất túi máu | `BL002`, `bl003` | Thành công (khớp đề) |
| Xuất mã sai / rỗng | `BL999`, khoảng trắng | Báo lỗi (khớp đề) |
| Xem kho cuối | Chọn 1 | 3 túi, BL001 đã gia hạn, tổng 850 ml |
| Menu sai | `9`, `abc`, rỗng | Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5! (khớp đề) |

## Ghi chú

- Đề không yêu cầu kiểm tra nhóm máu và định dạng ngày; chương trình bổ sung (8 nhóm máu chuẩn, ngày dạng DD/MM/YYYY) để kho máu không chứa dữ liệu sai.
- Tên người hiến giữ nguyên dấu tiếng Việt và viết hoa chữ cái đầu bằng `.title()`, đúng ví dụ `lê văn d` → `Lê Văn D`.
