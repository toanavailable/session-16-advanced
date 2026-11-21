# Bài 3 - Hệ thống quản lý bệnh nhân nội trú Rikkei Hospital

## Đề bài

Khoa Nội tổng hợp cần phần mềm terminal quản lý bệnh nhân nằm viện. Code cũ gom tất cả vào một vòng `while` dài hàng trăm dòng (spaghetti code). Nhiệm vụ: "đập đi xây lại" bằng **Function**, **String** và **List**. Mỗi bệnh nhân là **một list con** 4 phần tử theo thứ tự: Mã BN, Tên BN, Giới tính, Chẩn đoán.

```python
patients = [
    ["BN001", "Nguyen Van A", "Nam", "Viem Phoi"],
    ["BN002", "Tran Thi B", "Nu", "Sot Xuat Huyet"]
]
```

### Menu

```
===== HỆ THỐNG QUẢN LÝ BỆNH NHÂN RIKKEI =====
1. Hiển thị danh sách bệnh nhân
2. Tiếp nhận bệnh nhân mới
3. Cập nhật chẩn đoán bệnh theo mã BN
4. Tìm kiếm và thống kê theo tên bệnh
5. Thoát chương trình
---------------------------------------------
Nhập lựa chọn của bạn:
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Hiển thị danh sách | `display_patients(patient_list)` | In danh sách; rỗng thì "Hiện không có bệnh nhân nào đang điều trị." |
| 2. Tiếp nhận bệnh nhân | `add_patient(patient_list)` | Nhập Mã, Tên, Giới tính, Chẩn đoán. Mã: strip + upper; Tên: bỏ khoảng trắng thừa + Title case; Chẩn đoán: Capitalize. Gói 4 thông tin thành list con, `append()` |
| 3. Cập nhật chẩn đoán | `update_diagnosis(patient_list)` | Tìm bằng `find_patient_index`; cập nhật phần tử index 3; không thấy: "Không tìm thấy hồ sơ mang mã [Mã BN]!" |
| 4. Tìm kiếm theo tên bệnh | `search_by_disease(patient_list)` | Dùng `in` + `.lower()` để tìm không phân biệt hoa/thường; in kết quả và "Có tổng cộng X bệnh nhân mắc bệnh liên quan đến 'từ khóa'." |
| 5. Thoát | `main()` | "Cảm ơn bác sĩ đã sử dụng hệ thống!" |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 | Trùng mã BN | `find_patient_index` kiểm tra trước: "Mã bệnh nhân đã tồn tại trong hệ thống, vui lòng kiểm tra lại!" |
| Bẫy 2 | Giới tính linh tinh ("Bê đê", "Không rõ", " nam ") | `validate_gender` chặn, yêu cầu nhập lại (" nam " hợp lệ sau khi strip) |
| Bẫy 3 | Mã / tên / chẩn đoán / từ khóa toàn khoảng trắng | Kiểm tra chuỗi rỗng sau `.strip()`, báo "... không được để trống!" |
| Bẫy 4 | Menu ngoài 1-5 hoặc chữ | "Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!" |

## (1) Phân tích và thiết kế giải pháp

### Input / Output của từng hàm

| Hàm | Tham số (Input) | Trả về (Output) | Ghi chú |
|---|---|---|---|
| `validate_gender(gender_input)` | `str` | `bool` | Helper: `strip().lower()` thuộc `["nam", "nu"]` |
| `find_patient_index(patient_list, patient_id)` | `list[list]`, `str` | `int`: index hoặc -1 | Helper: chuẩn hóa mã (strip + upper) trước khi so sánh; dùng chung cho chức năng 2 và 3 |
| `print_patient(stt, patient, name_width)` | `int`, `list`, `int` | `None` | Helper in một dòng, dùng chung cho chức năng 1 và 4 |
| `display_menu()` | không | `str` | Lựa chọn menu |
| `display_patients(patient_list)` | `list[list]` | `None` | Chỉ in |
| `add_patient(patient_list)` | `list[list]` | `None` | Sửa list bằng `append()` |
| `update_diagnosis(patient_list)` | `list[list]` | `None` | Sửa `patient[3]` trực tiếp |
| `search_by_disease(patient_list)` | `list[list]` | `None` | Chỉ đọc và in |
| `main()` | không | `None` | Vòng lặp `while` gọi các hàm |

### String và List tương tác với nhau thế nào?

- **String** là dữ liệu của từng trường (mã, tên, giới tính, chẩn đoán). Vì chuỗi **bất biến**, mọi bước chuẩn hóa (`strip`, `upper`, `title`, `capitalize`, `split` + `join` để gộp khoảng trắng) đều tạo chuỗi mới và phải **gán lại** cho biến.
- **List** là "khung" chứa dữ liệu: list ngoài chứa các bệnh nhân, list con chứa 4 chuỗi. List là **mutable** nên thêm bệnh nhân (`append`) hay sửa chẩn đoán (`patient[3] = ...`) được thực hiện **trực tiếp** mà không cần tạo list mới.
- Chuẩn hóa chuỗi **trước khi** đưa vào list, nên dữ liệu lưu luôn sạch; khi tìm kiếm thì chuyển cả từ khóa và chẩn đoán về `.lower()` để so sánh công bằng.

### Truyền `patient_list` vào hàm là truyền tham chiếu hay giá trị?

Python truyền **tham chiếu tới đối tượng** (pass by object reference): tham số `patient_list` trong hàm và biến `patients` trong `main()` cùng trỏ tới **một list duy nhất**. Vì list là mutable, khi `add_patient` gọi `patient_list.append(...)`, danh sách gốc trong `main()` thay đổi ngay. Vì vậy các hàm không cần `return` list mới hay dùng biến toàn cục. Ngược lại, nếu trong hàm **gán lại** `patient_list = [...]`, thì chỉ biến cục bộ trỏ sang list khác, list gốc không đổi. Chuỗi là bất biến nên truyền chuỗi vào hàm không bao giờ làm đổi chuỗi gốc.

### Pseudocode

```
add_patient(list):
    mã ← strip().upper(); rỗng → lỗi; find_patient_index ≠ -1 → lỗi trùng
    tên ← gộp khoảng trắng, title(); rỗng → lỗi
    LẶP: giới tính ← nhập; validate_gender đúng → capitalize, thoát lặp; sai → "nhập lại"
    chẩn đoán ← gộp khoảng trắng, capitalize(); rỗng → lỗi
    list.append([mã, tên, giới tính, chẩn đoán])

search_by_disease(list):
    từ khóa ← strip(); rỗng → lỗi
    kết quả ← [bn VỚI MỖI bn NẾU từ_khóa.lower() in bn[3].lower()]
    in kết quả (hoặc "Không tìm thấy..."); in "Có tổng cộng len(kết quả) bệnh nhân..."
```

## (2) Triển khai code

File: [`quan_ly_benh_nhan_noi_tru.py`](quan_ly_benh_nhan_noi_tru.py)

```python
"""Hệ thống quản lý bệnh nhân nội trú Rikkei Hospital.

Mỗi bệnh nhân là một list con: [Mã BN, Tên BN, Giới tính, Chẩn đoán].
"""


# =====================================================================
# CÁC HÀM PHỤ TRỢ
# =====================================================================
def validate_gender(gender_input):
    """Kiểm tra giới tính.

    gender_input (str): chuỗi người dùng nhập
    Trả về: True nếu (sau khi bỏ khoảng trắng, chuyển chữ thường) là "nam" hoặc "nu"
    """
    return gender_input.strip().lower() in ["nam", "nu"]


def find_patient_index(patient_list, patient_id):
    """Tìm vị trí bệnh nhân theo mã (mã được xóa khoảng trắng 2 đầu, viết hoa trước khi so sánh).

    Trả về: index (int) của bệnh nhân trong list, hoặc -1 nếu không tìm thấy
    """
    patient_id = patient_id.strip().upper()
    for index, patient in enumerate(patient_list):
        if patient[0] == patient_id:
            return index
    return -1


# =====================================================================
# CÁC HÀM NGHIỆP VỤ
# =====================================================================
def display_menu():
    """In menu chính và trả về lựa chọn của người dùng (str)."""
    print("\n===== HỆ THỐNG QUẢN LÝ BỆNH NHÂN RIKKEI =====")
    print("1. Hiển thị danh sách bệnh nhân")
    print("2. Tiếp nhận bệnh nhân mới")
    print("3. Cập nhật chẩn đoán bệnh theo mã BN")
    print("4. Tìm kiếm và thống kê theo tên bệnh")
    print("5. Thoát chương trình")
    print("-" * 45)
    return input("Nhập lựa chọn của bạn: ").strip()


def print_patient(stt, patient, name_width):
    """In một dòng thông tin bệnh nhân (dùng chung cho chức năng 1 và 4)."""
    print(f"{stt}. Mã: {patient[0]} | Tên: {patient[1]:<{name_width}} | "
          f"Giới tính: {patient[2]:<3} | Bệnh: {patient[3]}")


def display_patients(patient_list):
    """Chức năng 1: in danh sách bệnh nhân đang điều trị. Trả về None."""
    if len(patient_list) == 0:
        print("Hiện không có bệnh nhân nào đang điều trị.")
        return
    name_width = max(len(patient[1]) for patient in patient_list)
    print("----- DANH SÁCH BỆNH NHÂN ĐANG ĐIỀU TRỊ -----")
    for stt, patient in enumerate(patient_list, start=1):
        print_patient(stt, patient, name_width)


def add_patient(patient_list):
    """Chức năng 2: tiếp nhận bệnh nhân mới, chuẩn hóa chuỗi rồi append list con."""
    print("----- TIẾP NHẬN BỆNH NHÂN MỚI -----")
    patient_id = input("Nhập mã bệnh nhân: ").strip().upper()
    if patient_id == "":                                                     # Bẫy 3
        print("Mã bệnh nhân không được để trống!")
        return
    if find_patient_index(patient_list, patient_id) != -1:                    # Bẫy 1
        print("Mã bệnh nhân đã tồn tại trong hệ thống, vui lòng kiểm tra lại!")
        return

    name = " ".join(input("Nhập tên bệnh nhân: ").split()).title()
    if name == "":                                                           # Bẫy 3
        print("Tên bệnh nhân không được để trống!")
        return

    while True:                                                              # Bẫy 2
        gender_input = input("Nhập giới tính Nam/Nu: ")
        if validate_gender(gender_input):
            gender = gender_input.strip().capitalize()                       # "nam" -> "Nam"
            break
        print("\nGiới tính không hợp lệ, vui lòng nhập lại!")

    diagnosis = " ".join(input("Nhập chẩn đoán bệnh: ").split()).capitalize()
    if diagnosis == "":
        print("Chẩn đoán bệnh không được để trống!")
        return

    patient_list.append([patient_id, name, gender, diagnosis])
    print("\nTiếp nhận bệnh nhân thành công!")


def update_diagnosis(patient_list):
    """Chức năng 3: cập nhật chẩn đoán (phần tử index 3) theo mã bệnh nhân."""
    print("----- CẬP NHẬT CHẨN ĐOÁN BỆNH -----")
    patient_id = input("Nhập mã bệnh nhân cần cập nhật: ").strip().upper()
    if patient_id == "":
        print("Mã bệnh nhân không được để trống!")
        return
    index = find_patient_index(patient_list, patient_id)
    if index == -1:
        print(f"Không tìm thấy hồ sơ mang mã {patient_id}!")
        return

    patient = patient_list[index]
    print(f"Tìm thấy bệnh nhân: {patient[1]}")
    print(f"Chẩn đoán hiện tại: {patient[3]}")
    new_diagnosis = " ".join(input("Nhập chẩn đoán mới: ").split()).capitalize()
    if new_diagnosis == "":
        print("Chẩn đoán bệnh không được để trống!")
        return
    patient[3] = new_diagnosis           # list con là mutable -> sửa trực tiếp
    print("Cập nhật chẩn đoán bệnh thành công!")


def search_by_disease(patient_list):
    """Chức năng 4: tìm bệnh nhân theo từ khóa tên bệnh (không phân biệt hoa/thường)."""
    print("----- TÌM KIẾM BỆNH NHÂN THEO TÊN BỆNH -----")
    keyword = input("Nhập từ khóa tên bệnh: ").strip()
    if keyword == "":
        print("\nTừ khóa tìm kiếm không được để trống!")
        return

    results = []
    for patient in patient_list:
        if keyword.lower() in patient[3].lower():
            results.append(patient)

    if len(results) == 0:
        print("Không tìm thấy bệnh nhân nào phù hợp.")
    else:
        print("Kết quả tìm kiếm:")
        name_width = max(len(patient[1]) for patient in results)
        for stt, patient in enumerate(results, start=1):
            print_patient(stt, patient, name_width)
    print(f"\nCó tổng cộng {len(results)} bệnh nhân mắc bệnh liên quan đến '{keyword}'.")


# =====================================================================
# CHƯƠNG TRÌNH CHÍNH
# =====================================================================
def main():
    """Vòng lặp menu: chỉ điều hướng tới các hàm chức năng."""
    patients = [
        ["BN001", "Nguyen Van A", "Nam", "Viem Phoi"],
        ["BN002", "Tran Thi B", "Nu", "Sot Xuat Huyet"],
    ]
    while True:
        choice = display_menu()
        if choice == "1":
            display_patients(patients)
        elif choice == "2":
            add_patient(patients)
        elif choice == "3":
            update_diagnosis(patients)
        elif choice == "4":
            search_by_disease(patients)
        elif choice == "5":
            print("Cảm ơn bác sĩ đã sử dụng hệ thống!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!")       # Bẫy 4


if __name__ == "__main__":
    main()
```

## Kết quả

Chạy thử toàn bộ chức năng và bẫy dữ liệu *(ẩn menu lặp lại)*:

```
Nhập lựa chọn của bạn: 1
----- DANH SÁCH BỆNH NHÂN ĐANG ĐIỀU TRỊ -----
1. Mã: BN001 | Tên: Nguyen Van A | Giới tính: Nam | Bệnh: Viem Phoi
2. Mã: BN002 | Tên: Tran Thi B   | Giới tính: Nu  | Bệnh: Sot Xuat Huyet

Nhập lựa chọn của bạn: 2
----- TIẾP NHẬN BỆNH NHÂN MỚI -----
Nhập mã bệnh nhân:   bn003 
Nhập tên bệnh nhân:   le   van  cuong 
Nhập giới tính Nam/Nu: nam
Nhập chẩn đoán bệnh:   dau da day 

Tiếp nhận bệnh nhân thành công!

Nhập lựa chọn của bạn: 2
----- TIẾP NHẬN BỆNH NHÂN MỚI -----
Nhập mã bệnh nhân: bn001
Mã bệnh nhân đã tồn tại trong hệ thống, vui lòng kiểm tra lại!

Nhập lựa chọn của bạn: 2
----- TIẾP NHẬN BỆNH NHÂN MỚI -----
Nhập mã bệnh nhân:    
Mã bệnh nhân không được để trống!

Nhập lựa chọn của bạn: 2
----- TIẾP NHẬN BỆNH NHÂN MỚI -----
Nhập mã bệnh nhân: BN004
Nhập tên bệnh nhân:   
Tên bệnh nhân không được để trống!

Nhập lựa chọn của bạn: 2
----- TIẾP NHẬN BỆNH NHÂN MỚI -----
Nhập mã bệnh nhân: BN004
Nhập tên bệnh nhân: Pham Thi Hoa
Nhập giới tính Nam/Nu: Không rõ

Giới tính không hợp lệ, vui lòng nhập lại!
Nhập giới tính Nam/Nu: Bê đê

Giới tính không hợp lệ, vui lòng nhập lại!
Nhập giới tính Nam/Nu: Nu
Nhập chẩn đoán bệnh: viem hong

Tiếp nhận bệnh nhân thành công!

Nhập lựa chọn của bạn: 1
----- DANH SÁCH BỆNH NHÂN ĐANG ĐIỀU TRỊ -----
1. Mã: BN001 | Tên: Nguyen Van A | Giới tính: Nam | Bệnh: Viem Phoi
2. Mã: BN002 | Tên: Tran Thi B   | Giới tính: Nu  | Bệnh: Sot Xuat Huyet
3. Mã: BN003 | Tên: Le Van Cuong | Giới tính: Nam | Bệnh: Dau da day
4. Mã: BN004 | Tên: Pham Thi Hoa | Giới tính: Nu  | Bệnh: Viem hong

Nhập lựa chọn của bạn: 3
----- CẬP NHẬT CHẨN ĐOÁN BỆNH -----
Nhập mã bệnh nhân cần cập nhật: bn001
Tìm thấy bệnh nhân: Nguyen Van A
Chẩn đoán hiện tại: Viem Phoi
Nhập chẩn đoán mới: viem phoi nang
Cập nhật chẩn đoán bệnh thành công!

Nhập lựa chọn của bạn: 3
----- CẬP NHẬT CHẨN ĐOÁN BỆNH -----
Nhập mã bệnh nhân cần cập nhật: BN999
Không tìm thấy hồ sơ mang mã BN999!

Nhập lựa chọn của bạn: 3
----- CẬP NHẬT CHẨN ĐOÁN BỆNH -----
Nhập mã bệnh nhân cần cập nhật:   
Mã bệnh nhân không được để trống!

Nhập lựa chọn của bạn: 3
----- CẬP NHẬT CHẨN ĐOÁN BỆNH -----
Nhập mã bệnh nhân cần cập nhật: BN001
Tìm thấy bệnh nhân: Nguyen Van A
Chẩn đoán hiện tại: Viem phoi nang
Nhập chẩn đoán mới:   
Chẩn đoán bệnh không được để trống!

Nhập lựa chọn của bạn: 4
----- TÌM KIẾM BỆNH NHÂN THEO TÊN BỆNH -----
Nhập từ khóa tên bệnh: viem
Kết quả tìm kiếm:
1. Mã: BN001 | Tên: Nguyen Van A | Giới tính: Nam | Bệnh: Viem phoi nang
2. Mã: BN004 | Tên: Pham Thi Hoa | Giới tính: Nu  | Bệnh: Viem hong

Có tổng cộng 2 bệnh nhân mắc bệnh liên quan đến 'viem'.

Nhập lựa chọn của bạn: 4
----- TÌM KIẾM BỆNH NHÂN THEO TÊN BỆNH -----
Nhập từ khóa tên bệnh: SOT
Kết quả tìm kiếm:
1. Mã: BN002 | Tên: Tran Thi B | Giới tính: Nu  | Bệnh: Sot Xuat Huyet

Có tổng cộng 1 bệnh nhân mắc bệnh liên quan đến 'SOT'.

Nhập lựa chọn của bạn: 4
----- TÌM KIẾM BỆNH NHÂN THEO TÊN BỆNH -----
Nhập từ khóa tên bệnh: tim
Không tìm thấy bệnh nhân nào phù hợp.

Có tổng cộng 0 bệnh nhân mắc bệnh liên quan đến 'tim'.

Nhập lựa chọn của bạn: 4
----- TÌM KIẾM BỆNH NHÂN THEO TÊN BỆNH -----
Nhập từ khóa tên bệnh:   

Từ khóa tìm kiếm không được để trống!

Nhập lựa chọn của bạn: abc
Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Nhập lựa chọn của bạn: 9
Lựa chọn không hợp lệ, vui lòng nhập số từ 1-5!

Nhập lựa chọn của bạn: 5
Cảm ơn bác sĩ đã sử dụng hệ thống!
```

Danh sách rỗng (gọi trực tiếp `display_patients([])`):

```
Hiện không có bệnh nhân nào đang điều trị.
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Hiển thị mẫu | Chọn 1 | 2 bệnh nhân, cột thẳng hàng (khớp đề) |
| Tiếp nhận hợp lệ | `  bn003 `, `  le   van  cuong `, `nam`, `  dau da day ` | Lưu `['BN003', 'Le Van Cuong', 'Nam', 'Dau da day']` (khớp đề) |
| Bẫy 1 - trùng mã | `bn001` | Mã bệnh nhân đã tồn tại... (khớp đề) |
| Bẫy 3 - mã / tên rỗng | khoảng trắng | ... không được để trống! (khớp đề) |
| Bẫy 2 - giới tính sai | `Không rõ`, `Bê đê` → `Nu` | Nhập lại đến khi hợp lệ (khớp đề) |
| Cập nhật chẩn đoán | `bn001` → `viem phoi nang` | Thành công (khớp đề) |
| Cập nhật mã không có / rỗng / chẩn đoán rỗng | `BN999`, khoảng trắng | Báo lỗi tương ứng (khớp đề) |
| Tìm kiếm có kết quả | `viem` | 2 bệnh nhân (khớp đề) |
| Không phân biệt hoa thường | `SOT` | 1 bệnh nhân: Sot Xuat Huyet (khớp đề) |
| Không có kết quả / từ khóa rỗng | `tim`, khoảng trắng | Có tổng cộng 0 ... / Từ khóa không được để trống (khớp đề) |
| Bẫy 4 - menu sai | `abc`, `9` | Lựa chọn không hợp lệ... |

## Ghi chú

- Ảnh menu trong đề không hiện số thứ tự; chương trình đánh số 1-5 cho đúng với lựa chọn "Nhập lựa chọn của bạn".
- Đề không yêu cầu kiểm tra chẩn đoán rỗng ở chức năng 2, nhưng chương trình vẫn chặn để dữ liệu không bị trống, giống chức năng 3.
