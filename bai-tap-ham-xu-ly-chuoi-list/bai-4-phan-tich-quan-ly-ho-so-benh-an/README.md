# Bài 4 - Phân tích hệ thống quản lý hồ sơ bệnh án Rikkei Hospital

## Đề bài

Phòng Kế hoạch Tổng hợp cần phần mềm terminal quản lý hồ sơ bệnh án. Trưởng phòng IT yêu cầu **tuyệt đối không viết code dồn cục**: mọi nghiệp vụ phải là hàm riêng. Để tối ưu bộ nhớ, danh sách bệnh nhân là **list chứa các chuỗi**; mỗi chuỗi là một hồ sơ, các trường ngăn cách bằng dấu `-` theo cấu trúc **Mã BN - Tên BN - Năm sinh - Chẩn đoán**.

```python
patient_records = [
    "BN001-Nguyen Van A-1985-Viem Phoi",
    "BN002-Tran Thi B-1990-Sot Xuat Huyet",
    "BN003-Le Van C-2015-Viem Phe Quan"
]
```

### Menu

```
===== HỆ THỐNG QUẢN LÝ HỒ SƠ BỆNH ÁN RIKKEI HOSPITAL =====
1. Xem danh sách hồ sơ bệnh án
2. Thêm hồ sơ bệnh nhân mới
3. Cập nhật chẩn đoán theo Mã BN
4. Báo cáo phân loại theo độ tuổi
5. Thoát chương trình
==================================================
Chọn chức năng (1-5):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Xem danh sách | `display_records(records)` | Tách chuỗi bằng `split("-")`, in bảng căn lề; rỗng: "Hệ thống hiện chưa có hồ sơ nào." |
| 2. Thêm hồ sơ | `add_patient(records)` | Mã: viết hoa, xóa khoảng trắng; Tên: Title case; Chẩn đoán: Capitalize; dấu `-` người dùng nhập được đổi thành khoảng trắng; ghép bằng `"-".join()` rồi `append()` |
| 3. Cập nhật chẩn đoán | `update_diagnosis(records)` | Tách chuỗi thành list → sửa phần tử cuối → ghép lại → gán đè vào vị trí cũ |
| 4. Báo cáo độ tuổi | `generate_age_report(records)` | Tuổi = năm hiện tại − năm sinh; < 16 Trẻ em, 16-60 Trưởng thành, > 60 Người cao tuổi |
| 5. Thoát | `main()` | "Cảm ơn bác sĩ đã sử dụng hệ thống!" |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 | Năm sinh có chữ (`19a0`), < 1900 hoặc > năm hiện tại (`1800`, `2030`) | `isdigit()` + kiểm tra khoảng; "Năm sinh không hợp lệ, vui lòng nhập lại!" |
| Bẫy 2 | Trùng mã BN | Duyệt chuỗi, `startswith("BN001-")`; "Mã bệnh nhân đã tồn tại!" |
| Bẫy 3 | Cập nhật mã `BN999` không tồn tại | "Không tìm thấy bệnh nhân mang mã BN999!" |

## (1) Phân tích thiết kế hàm

### Hàm `find_patient_index(records, patient_id)` (helper dùng chung cho chức năng 2 và 3)
- **Input:** `records`: list các chuỗi; `patient_id`: `str` đã chuẩn hóa.
- **Output:** `int`: vị trí hồ sơ trong list, hoặc `-1` nếu không có.
- **Pseudocode:**
```
VỚI MỖI (index, record) trong records:
    NẾU record.startswith(patient_id + "-"): TRẢ VỀ index
TRẢ VỀ -1
```
- So khớp cả dấu `-` phía sau để `BN00` không bị nhận nhầm là `BN001`.

### Hàm `display_records(records)`
- **Input:** `records`: list các chuỗi.
- **Output:** `None` (chỉ in ra màn hình).
- **Pseudocode:**
```
NẾU records rỗng: in "Hệ thống hiện chưa có hồ sơ nào."; KẾT THÚC
VỚI MỖI (stt, record):
    mã, tên, năm_sinh, chẩn_đoán ← record.split("-")
    in "stt. [mã] tên(căn lề 15) | Năm sinh: ... | Chẩn đoán: ..."
```

### Hàm `add_patient(records)`
- **Input:** `records`: list các chuỗi (được sửa trực tiếp).
- **Output:** `None`.
- **Pseudocode:**
```
mã ← "".join(input().split()).upper()        # xóa mọi khoảng trắng, viết hoa
NẾU mã rỗng → lỗi; NẾU find_patient_index(records, mã) ≠ -1 → "Mã bệnh nhân đã tồn tại!"
tên ← clean_text(input()).title()             # clean_text: "-" → " ", gộp khoảng trắng
LẶP: năm ← input(); NẾU năm.isdigit() VÀ 1900 ≤ năm ≤ năm_hiện_tại: thoát; ngược lại báo lỗi
chẩn_đoán ← clean_text(input()).capitalize()
records.append("-".join([mã, tên, năm, chẩn_đoán]))
```

### Hàm `update_diagnosis(records)`
- **Input:** `records`: list các chuỗi.
- **Output:** `None`.
- **Pseudocode:**
```
mã ← chuẩn hóa; i ← find_patient_index(records, mã)
NẾU i == -1: "Không tìm thấy bệnh nhân mang mã <mã>!"; KẾT THÚC
parts ← records[i].split("-")            # chuỗi bất biến -> tách thành list
in tên (parts[1]) và chẩn đoán hiện tại (parts[3])
parts[-1] ← clean_text(input()).capitalize()
records[i] ← "-".join(parts)              # ghép thành chuỗi mới, gán đè vị trí cũ
```

### Hàm `generate_age_report(records)`
- **Input:** `records`: list các chuỗi.
- **Output:** `None` (in báo cáo).
- **Pseudocode:**
```
NẾU rỗng: thông báo; KẾT THÚC
trẻ_em ← trưởng_thành ← cao_tuổi ← 0
VỚI MỖI record: tuổi ← năm_hiện_tại − int(record.split("-")[2])
    tuổi < 16 → trẻ_em += 1; tuổi ≤ 60 → trưởng_thành += 1; còn lại → cao_tuổi += 1
in 3 con số
```

### Các hàm phụ trợ khác

| Hàm | Input | Output |
|---|---|---|
| `normalize_id(raw_id)` | `str` | `str`: xóa mọi khoảng trắng, viết hoa |
| `clean_text(raw_text)` | `str` | `str`: đổi `-` thành khoảng trắng, gộp khoảng trắng thừa |
| `is_empty(records)` | `list` | `bool` (in thông báo nếu rỗng) |
| `display_menu()` | không | `str` |

### Vì sao phải đổi dấu `-` thành khoảng trắng?

Dấu `-` là **ký tự phân cách** của hệ thống. Nếu tên `nguyen-van-e` được lưu nguyên, chuỗi hồ sơ sẽ thành `BN005-nguyen-van-e-1998-...` và `split("-")` sẽ cắt ra 6 phần thay vì 4: tên bị vỡ, năm sinh và chẩn đoán lệch vị trí. Vì vậy hàm `clean_text` thay `-` bằng khoảng trắng **trước khi** ghép chuỗi: `nguyen-van-e` → `Nguyen Van E`, `viem-gan-b` → `Viem gan b`.

## (2) Triển khai code

File: [`quan_ly_ho_so_benh_an.py`](quan_ly_ho_so_benh_an.py)

```python
"""Hệ thống quản lý hồ sơ bệnh án Rikkei Hospital.

Mỗi hồ sơ là MỘT chuỗi: "Mã BN-Tên BN-Năm sinh-Chẩn đoán" (ngăn cách bằng dấu "-").
"""
import datetime

CURRENT_YEAR = datetime.date.today().year     # Năm hiện tại (dùng tính tuổi, kiểm tra năm sinh)
SEPARATOR = "-"


# =====================================================================
# CÁC HÀM PHỤ TRỢ
# =====================================================================
def normalize_id(raw_id):
    """Chuẩn hóa mã BN: xóa mọi khoảng trắng, viết hoa. Trả về str."""
    return "".join(raw_id.split()).upper()


def clean_text(raw_text):
    """Đổi ký tự phân cách "-" thành khoảng trắng và gộp khoảng trắng thừa. Trả về str."""
    return " ".join(raw_text.replace(SEPARATOR, " ").split())


def find_patient_index(records, patient_id):
    """Tìm vị trí hồ sơ có mã patient_id (so bằng startswith "Mã-").

    Trả về: index (int), hoặc -1 nếu không có
    """
    for index, record in enumerate(records):
        if record.startswith(patient_id + SEPARATOR):
            return index
    return -1


def is_empty(records):
    """In thông báo và trả về True nếu chưa có hồ sơ nào."""
    if len(records) == 0:
        print("Hệ thống hiện chưa có hồ sơ nào.")
        return True
    return False


# =====================================================================
# CÁC HÀM NGHIỆP VỤ
# =====================================================================
def display_menu():
    """In menu và trả về lựa chọn (str)."""
    print("\n===== HỆ THỐNG QUẢN LÝ HỒ SƠ BỆNH ÁN RIKKEI HOSPITAL =====")
    print("1. Xem danh sách hồ sơ bệnh án")
    print("2. Thêm hồ sơ bệnh nhân mới")
    print("3. Cập nhật chẩn đoán theo Mã BN")
    print("4. Báo cáo phân loại theo độ tuổi")
    print("5. Thoát chương trình")
    print("=" * 50)
    return input("Chọn chức năng (1-5): ").strip()


def display_records(records):
    """Chức năng 1: tách từng chuỗi bằng split("-") và in dạng bảng. Trả về None."""
    if is_empty(records):
        return
    print("--- DANH SÁCH BỆNH NHÂN " + "-" * 50)
    for stt, record in enumerate(records, start=1):
        patient_id, name, birth_year, diagnosis = record.split(SEPARATOR)
        print(f"{stt}. [{patient_id}] {name:<15}| Năm sinh: {birth_year} | Chẩn đoán: {diagnosis}")
    print("-" * 74)


def add_patient(records):
    """Chức năng 2: nhập, chuẩn hóa, ghép 4 thông tin bằng join() rồi append vào records."""
    print("--- THÊM HỒ SƠ BỆNH NHÂN MỚI ---")
    patient_id = normalize_id(input("Nhập mã bệnh nhân: "))
    if patient_id == "":
        print("\nMã bệnh nhân không được để trống!")
        return
    if find_patient_index(records, patient_id) != -1:                       # Bẫy 2
        print("\nMã bệnh nhân đã tồn tại!")
        return

    name = clean_text(input("Nhập tên bệnh nhân: ")).title()
    if name == "":
        print("\nTên bệnh nhân không được để trống!")
        return

    while True:                                                             # Bẫy 1
        birth_year = input("Nhập năm sinh: ").strip()
        if birth_year.isdigit() and 1900 <= int(birth_year) <= CURRENT_YEAR:
            break
        print("\nNăm sinh không hợp lệ, vui lòng nhập lại!")

    diagnosis = clean_text(input("Nhập chẩn đoán: ")).capitalize()
    if diagnosis == "":
        print("\nChẩn đoán không được để trống!")
        return

    new_record = SEPARATOR.join([patient_id, name, birth_year, diagnosis])
    records.append(new_record)
    print("\nThêm hồ sơ bệnh nhân thành công!")
    print("Sau khi chuẩn hóa, dữ liệu được lưu là:")
    print(new_record)


def update_diagnosis(records):
    """Chức năng 3: tách chuỗi -> sửa phần tử cuối -> ghép lại -> ghi đè vào records[index]."""
    print("--- CẬP NHẬT CHẨN ĐOÁN THEO MÃ BN ---")
    patient_id = normalize_id(input("Nhập mã bệnh nhân cần cập nhật: "))
    index = find_patient_index(records, patient_id)
    if index == -1:                                                          # Bẫy 3
        print(f"\nKhông tìm thấy bệnh nhân mang mã {patient_id}!")
        return

    parts = records[index].split(SEPARATOR)          # chuỗi bất biến -> tách ra list
    print(f"\nTìm thấy bệnh nhân: {parts[1]}")
    print(f"Chẩn đoán hiện tại: {parts[3]}")
    new_diagnosis = clean_text(input("Nhập chẩn đoán mới: ")).capitalize()
    if new_diagnosis == "":
        print("\nChẩn đoán không được để trống!")
        return
    parts[-1] = new_diagnosis                        # sửa phần tử cuối của list
    records[index] = SEPARATOR.join(parts)           # ghép lại và gán đè vào vị trí cũ
    print("\nCập nhật chẩn đoán thành công!")
    print("Dữ liệu mới được lưu:")
    print(records[index])


def generate_age_report(records):
    """Chức năng 4: đếm số bệnh nhân Trẻ em (<16), Trưởng thành (16-60), Người cao tuổi (>60)."""
    if is_empty(records):
        return
    children = adults = seniors = 0
    for record in records:
        age = CURRENT_YEAR - int(record.split(SEPARATOR)[2])
        if age < 16:
            children += 1
        elif age <= 60:
            adults += 1
        else:
            seniors += 1
    print("\n--- BÁO CÁO PHÂN LOẠI THEO ĐỘ TUỔI ---")
    print(f"Trẻ em: {children} bệnh nhân")
    print(f"Trưởng thành: {adults} bệnh nhân")
    print(f"Người cao tuổi: {seniors} bệnh nhân")
    print("-" * 38)


# =====================================================================
# CHƯƠNG TRÌNH CHÍNH
# =====================================================================
def main():
    """Vòng lặp menu, điều hướng tới các hàm nghiệp vụ."""
    patient_records = [
        "BN001-Nguyen Van A-1985-Viem Phoi",
        "BN002-Tran Thi B-1990-Sot Xuat Huyet",
        "BN003-Le Van C-2015-Viem Phe Quan",
    ]
    while True:
        choice = display_menu()
        if choice == "1":
            display_records(patient_records)
        elif choice == "2":
            add_patient(patient_records)
        elif choice == "3":
            update_diagnosis(patient_records)
        elif choice == "4":
            generate_age_report(patient_records)
        elif choice == "5":
            print("Cảm ơn bác sĩ đã sử dụng hệ thống!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!")


if __name__ == "__main__":
    main()
```

## Kết quả

Chạy thử toàn bộ chức năng và bẫy dữ liệu *(ẩn menu lặp lại; năm hiện tại khi chạy là 2026)*:

```
Chọn chức năng (1-5): 1
--- DANH SÁCH BỆNH NHÂN --------------------------------------------------
1. [BN001] Nguyen Van A   | Năm sinh: 1985 | Chẩn đoán: Viem Phoi
2. [BN002] Tran Thi B     | Năm sinh: 1990 | Chẩn đoán: Sot Xuat Huyet
3. [BN003] Le Van C       | Năm sinh: 2015 | Chẩn đoán: Viem Phe Quan
--------------------------------------------------------------------------

Chọn chức năng (1-5): 4

--- BÁO CÁO PHÂN LOẠI THEO ĐỘ TUỔI ---
Trẻ em: 1 bệnh nhân
Trưởng thành: 2 bệnh nhân
Người cao tuổi: 0 bệnh nhân
--------------------------------------

Chọn chức năng (1-5): 2
--- THÊM HỒ SƠ BỆNH NHÂN MỚI ---
Nhập mã bệnh nhân:    bn004
Nhập tên bệnh nhân: le van d
Nhập năm sinh: 2001
Nhập chẩn đoán: dau da day

Thêm hồ sơ bệnh nhân thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
BN004-Le Van D-2001-Dau da day

Chọn chức năng (1-5): 2
--- THÊM HỒ SƠ BỆNH NHÂN MỚI ---
Nhập mã bệnh nhân: bn005
Nhập tên bệnh nhân: nguyen-van-e
Nhập năm sinh: 1998
Nhập chẩn đoán: viem-gan-b

Thêm hồ sơ bệnh nhân thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
BN005-Nguyen Van E-1998-Viem gan b

Chọn chức năng (1-5): 2
--- THÊM HỒ SƠ BỆNH NHÂN MỚI ---
Nhập mã bệnh nhân: bn001

Mã bệnh nhân đã tồn tại!

Chọn chức năng (1-5): 2
--- THÊM HỒ SƠ BỆNH NHÂN MỚI ---
Nhập mã bệnh nhân: BN006
Nhập tên bệnh nhân: Pham Van F
Nhập năm sinh: 19a0

Năm sinh không hợp lệ, vui lòng nhập lại!
Nhập năm sinh: 1800

Năm sinh không hợp lệ, vui lòng nhập lại!
Nhập năm sinh: 2030

Năm sinh không hợp lệ, vui lòng nhập lại!
Nhập năm sinh: 1950
Nhập chẩn đoán: tang huyet ap

Thêm hồ sơ bệnh nhân thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
BN006-Pham Van F-1950-Tang huyet ap

Chọn chức năng (1-5): 3
--- CẬP NHẬT CHẨN ĐOÁN THEO MÃ BN ---
Nhập mã bệnh nhân cần cập nhật: bn001

Tìm thấy bệnh nhân: Nguyen Van A
Chẩn đoán hiện tại: Viem Phoi
Nhập chẩn đoán mới: viem phoi nang

Cập nhật chẩn đoán thành công!
Dữ liệu mới được lưu:
BN001-Nguyen Van A-1985-Viem phoi nang

Chọn chức năng (1-5): 3
--- CẬP NHẬT CHẨN ĐOÁN THEO MÃ BN ---
Nhập mã bệnh nhân cần cập nhật: BN002

Tìm thấy bệnh nhân: Tran Thi B
Chẩn đoán hiện tại: Sot Xuat Huyet
Nhập chẩn đoán mới: sot-cao-kem-met-moi

Cập nhật chẩn đoán thành công!
Dữ liệu mới được lưu:
BN002-Tran Thi B-1990-Sot cao kem met moi

Chọn chức năng (1-5): 3
--- CẬP NHẬT CHẨN ĐOÁN THEO MÃ BN ---
Nhập mã bệnh nhân cần cập nhật: BN999

Không tìm thấy bệnh nhân mang mã BN999!

Chọn chức năng (1-5): 1
--- DANH SÁCH BỆNH NHÂN --------------------------------------------------
1. [BN001] Nguyen Van A   | Năm sinh: 1985 | Chẩn đoán: Viem phoi nang
2. [BN002] Tran Thi B     | Năm sinh: 1990 | Chẩn đoán: Sot cao kem met moi
3. [BN003] Le Van C       | Năm sinh: 2015 | Chẩn đoán: Viem Phe Quan
4. [BN004] Le Van D       | Năm sinh: 2001 | Chẩn đoán: Dau da day
5. [BN005] Nguyen Van E   | Năm sinh: 1998 | Chẩn đoán: Viem gan b
6. [BN006] Pham Van F     | Năm sinh: 1950 | Chẩn đoán: Tang huyet ap
--------------------------------------------------------------------------

Chọn chức năng (1-5): 4

--- BÁO CÁO PHÂN LOẠI THEO ĐỘ TUỔI ---
Trẻ em: 1 bệnh nhân
Trưởng thành: 4 bệnh nhân
Người cao tuổi: 1 bệnh nhân
--------------------------------------

Chọn chức năng (1-5): x
Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Chọn chức năng (1-5): 5
Cảm ơn bác sĩ đã sử dụng hệ thống!
```

Danh sách rỗng (gọi trực tiếp `display_records([])`, `generate_age_report([])`):

```
Hệ thống hiện chưa có hồ sơ nào.
Hệ thống hiện chưa có hồ sơ nào.
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Danh sách mẫu | Chọn 1 | 3 hồ sơ, cột thẳng hàng (khớp đề) |
| Báo cáo độ tuổi mẫu | Chọn 4 | Trẻ em 1, Trưởng thành 2, Cao tuổi 0 (khớp đề) |
| Thêm hợp lệ | `   bn004`, `le van d`, 2001, `dau da day` | `BN004-Le Van D-2001-Dau da day` (khớp đề) |
| Tên / chẩn đoán có `-` | `nguyen-van-e`, `viem-gan-b` | `BN005-Nguyen Van E-1998-Viem gan b` (khớp đề) |
| Bẫy 2 - trùng mã | `bn001` | Mã bệnh nhân đã tồn tại! (khớp đề) |
| Bẫy 1 - năm sinh sai | `19a0`, `1800`, `2030` | Năm sinh không hợp lệ, nhập lại (khớp đề) |
| Cập nhật chẩn đoán | `bn001` → `viem phoi nang` | Thành công (khớp đề) |
| Chẩn đoán mới có `-` | `BN002` → `sot-cao-kem-met-moi` | `BN002-Tran Thi B-1990-Sot cao kem met moi` (khớp đề) |
| Bẫy 3 | `BN999` | Không tìm thấy bệnh nhân mang mã BN999! (khớp đề) |
| Báo cáo sau khi thêm | Chọn 4 | Trẻ em 1, Trưởng thành 4, Cao tuổi 1 (BN006 sinh 1950) |

## Ghi chú

- Năm hiện tại lấy từ `datetime.date.today().year`, nên báo cáo độ tuổi và giới hạn năm sinh luôn đúng theo thời điểm chạy chương trình.
- Đề không nêu thông báo khi mã / tên / chẩn đoán để trống; chương trình báo "... không được để trống!" và quay lại menu.
