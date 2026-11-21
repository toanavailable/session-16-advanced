# Bài 5 - Hệ thống phân loại và theo dõi sinh hiệu cấp cứu (ER Triage System)

## Đề bài

Tại Khoa Cấp cứu (ER), y tá liên tục ghi nhận sinh hiệu của bệnh nhân mới nhập viện: **Nhịp tim (HR)** và **Nhiệt độ (TEMP)**, để hệ thống tự động phân loại mức độ nguy hiểm. Dữ liệu là **list các chuỗi**, các trường nối với nhau bằng ký tự ống `|`; dữ liệu sinh hiệu dính liền chữ và số:

**Mã Bệnh Nhân | Tên Bệnh Nhân | Nhịp tim (HR) | Nhiệt độ (TEMP)**

```python
er_patients = [
    "ER01|Nguyen Van Quan|HR:115|TEMP:39.5",
    "ER02|Tran Thi Binh|HR:80|TEMP:37.0",
    "ER03|Le Van Cuong|HR:130|TEMP:38.2"
]
```

### Menu

```
===== HỆ THỐNG QUẢN LÝ CẤP CỨU RIKKEI ER =====
1. Bảng theo dõi bệnh nhân
2. Tiếp nhận ca cấp cứu mới
3. Cập nhật lại sinh hiệu
4. BÁO ĐỘNG ĐỎ Lọc bệnh nhân nguy kịch
5. Xuất viện / Chuyển khoa
6. Thoát chương trình
==============================================
Chọn chức năng (1-6):
```

### Yêu cầu chức năng

| Chức năng | Hàm | Mô tả |
|---|---|---|
| 1. Bảng theo dõi | `display_dashboard(patients)` | Tách chuỗi bằng `split("|")`, in bảng; rỗng: "Khoa cấp cứu hiện đang trống." |
| 2. Tiếp nhận ca mới | `admit_patient(patients)` | Mã ER: viết hoa, xóa khoảng trắng; Tên: Title case; nhịp tim / nhiệt độ ghép đúng format `HR:90`, `TEMP:38.4`; nối bằng `"|".join()`, `append()` |
| 3. Cập nhật sinh hiệu | `update_vitals(patients)` | Tách chuỗi → sửa index 2 (HR) hoặc 3 (TEMP) → `join()` → gán đè |
| 4. Báo động đỏ | `trigger_red_alert(patients)` | Lọc bệnh nhân có HR > 100 **hoặc** TEMP ≥ 39.0; bóc tách số bằng `split(":")` rồi ép `float` |
| 5. Xuất viện / Chuyển khoa | `discharge_patient(patients)` | Tìm vị trí, xóa bằng `pop()`; "Đã chuyển khoa thành công cho bệnh nhân [Tên BN]!" |
| 6. Thoát | `main()` | Kết thúc vòng lặp |

### Edge cases

| Bẫy | Tình huống | Xử lý |
|---|---|---|
| Bẫy 1 | Trùng mã ER (`er01`) | Kiểm tra bằng `startswith("ER01|")`: "Mã ca cấp cứu đã tồn tại!" |
| Bẫy 2 | Sinh hiệu nhập chữ (`chin muoi`, `mot tram`), ≤ 0, nhiệt độ < 36.5 | `.replace(".", "", 1).isdigit()` để bắt lỗi, yêu cầu nhập lại, không crash |
| Bẫy 3 | Xóa mã ER không tồn tại / rỗng | "Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!" / "Mã ER không được để trống!" |

## (1) Phân tích và thiết kế giải pháp

### Helper 1: `find_patient_index(patients, er_id)`

- **Input:** `patients`: list các chuỗi; `er_id`: mã ER đã chuẩn hóa.
- **Output:** `int`: vị trí trong list, hoặc `-1`.
- **Thuật toán:** duyệt `enumerate(patients)`, trả về index đầu tiên có `record.startswith(er_id + "|")`. Ghép thêm `"|"` để mã `ER0` không khớp nhầm với `ER01`.
- **Dùng ở:** chức năng 2 (kiểm tra trùng), 3 (tìm để cập nhật), 5 (tìm để xóa). Viết một lần, dùng ba nơi.

### Helper 2: `extract_vital_value(vital_string)`

- **Input:** `vital_string`: chuỗi dạng `"HR:115"` hoặc `"TEMP:39.5"`.
- **Output:** `float`: `115.0` hoặc `39.5`.
- **Thuật toán xử lý chuỗi:**
```
"HR:115".split(":")   →  ["HR", "115"]
lấy phần tử index 1   →  "115"
float("115")          →  115.0
```
  Dùng `split(":")` thay vì slicing cố định (`s[3:]`) vì độ dài tiền tố khác nhau (`HR:` có 3 ký tự, `TEMP:` có 5 ký tự). `split` hoạt động đúng với cả hai mà không cần đếm vị trí.
- **Dùng ở:** chức năng 4, để so sánh toán học `HR > 100`, `TEMP >= 39.0`.

### Luồng dữ liệu giữa String và List

```
Chuỗi lưu trữ  "ER02|Tran Thi Binh|HR:80|TEMP:37.0"
        │ split("|")
        ▼
List tạm       ["ER02", "Tran Thi Binh", "HR:80", "TEMP:37.0"]
        │ parts[2] = "HR:105"          (list sửa được, chuỗi thì không)
        ▼
List đã sửa    ["ER02", "Tran Thi Binh", "HR:105", "TEMP:37.0"]
        │ "|".join(parts)
        ▼
Chuỗi mới      "ER02|Tran Thi Binh|HR:105|TEMP:37.0"  → gán đè patients[index]
```

### Bảng hàm

| Hàm | Input | Output |
|---|---|---|
| `find_patient_index(patients, er_id)` | `list[str]`, `str` | `int` |
| `extract_vital_value(vital_string)` | `str` | `float` |
| `vital_text(vital_string)` | `str` | `str` phần số để hiển thị |
| `is_valid_number(text)` | `str` | `bool` |
| `read_er_id(prompt)` | `str` | `str` mã đã chuẩn hóa (`""` nếu trống) |
| `is_empty(patients)` | `list[str]` | `bool` |
| `display_dashboard` / `admit_patient` / `update_vitals` / `trigger_red_alert` / `discharge_patient` | `list[str]` | `None` |

### Tách bạch logic xử lý dữ liệu và logic hiển thị

- Các hàm helper (`extract_vital_value`, `find_patient_index`, `is_valid_number`) **chỉ tính toán và trả về giá trị**, không `print`.
- Các hàm chức năng gọi helper để lấy dữ liệu, rồi mới định dạng và `print`. Ví dụ `trigger_red_alert` lọc danh sách nguy kịch vào list `critical` trước, sau đó mới in bảng.

## (2) Triển khai code

File: [`er_triage.py`](er_triage.py)

```python
"""ER Triage System - Hệ thống phân loại & theo dõi sinh hiệu cấp cứu Rikkei ER.

Mỗi ca là MỘT chuỗi: "Mã ER|Tên bệnh nhân|HR:<nhịp tim>|TEMP:<nhiệt độ>".
Không dùng Dictionary: mọi thao tác đi qua lại giữa String và List (split / join).
"""

SEPARATOR = "|"
MIN_TEMP = 36.5          # Nhiệt độ hợp lệ phải >= 36.5
ALERT_HR = 100           # Nguy kịch khi nhịp tim > 100
ALERT_TEMP = 39.0        # hoặc nhiệt độ >= 39.0


# =====================================================================
# CÁC HÀM PHỤ TRỢ
# =====================================================================
def find_patient_index(patients, er_id):
    """Tìm vị trí ca cấp cứu có mã er_id (so bằng startswith "Mã|").

    patients (list[str]), er_id (str đã chuẩn hóa)
    Trả về: index (int), hoặc -1 nếu không tìm thấy
    """
    for index, record in enumerate(patients):
        if record.startswith(er_id + SEPARATOR):
            return index
    return -1


def extract_vital_value(vital_string):
    """Bóc tách giá trị số từ chuỗi sinh hiệu.

    vital_string (str): ví dụ "HR:115" hoặc "TEMP:39.5"
    Trả về: float, ví dụ 115.0 hoặc 39.5
    Thuật toán: split(":") -> ["HR", "115"] -> lấy phần tử index 1 -> ép float
    """
    return float(vital_string.split(":")[1])


def vital_text(vital_string):
    """Trả về phần chữ số sau dấu ":" để hiển thị (giữ nguyên định dạng, ví dụ "115")."""
    return vital_string.split(":")[1]


def is_valid_number(text):
    """True nếu chuỗi là số không âm (cho phép một dấu thập phân). Dùng replace + isdigit."""
    return text.replace(".", "", 1).isdigit()


def read_er_id(prompt):
    """Nhập mã ER, chuẩn hóa (xóa khoảng trắng, viết hoa). Trả về "" nếu bỏ trống (đã báo lỗi)."""
    er_id = "".join(input(prompt).split()).upper()
    if er_id == "":
        print("Mã ER không được để trống!")
    return er_id


def is_empty(patients):
    """In thông báo và trả về True nếu khoa cấp cứu đang trống."""
    if len(patients) == 0:
        print("Khoa cấp cứu hiện đang trống.")
        return True
    return False


# =====================================================================
# CÁC HÀM NGHIỆP VỤ
# =====================================================================
def display_menu():
    """In menu và trả về lựa chọn (str)."""
    print("\n===== HỆ THỐNG QUẢN LÝ CẤP CỨU RIKKEI ER =====")
    print("1. Bảng theo dõi bệnh nhân")
    print("2. Tiếp nhận ca cấp cứu mới")
    print("3. Cập nhật lại sinh hiệu")
    print("4. BÁO ĐỘNG ĐỎ Lọc bệnh nhân nguy kịch")
    print("5. Xuất viện / Chuyển khoa")
    print("6. Thoát chương trình")
    print("=" * 46)
    return input("Chọn chức năng (1-6): ").strip()


def display_dashboard(patients):
    """Chức năng 1: tách từng chuỗi bằng split("|") và in bảng theo dõi. Trả về None."""
    if is_empty(patients):
        return
    name_width = max(len(record.split(SEPARATOR)[1]) for record in patients)
    print("--- BẢNG THEO DÕI CA CẤP CỨU " + "-" * 36)
    for stt, record in enumerate(patients, start=1):
        er_id, name, hr, temp = record.split(SEPARATOR)
        print(f"{stt}. [{er_id}] {name:<{name_width}} | Nhịp tim: {vital_text(hr):<3} bpm | "
              f"Nhiệt độ: {vital_text(temp)} °C")
    print("-" * 65)


def admit_patient(patients):
    """Chức năng 2: nhập, chuẩn hóa, ghép 4 thông tin bằng "|".join() rồi append."""
    print("--- TIẾP NHẬN CA CẤP CỨU MỚI ---")
    er_id = read_er_id("Nhập mã ER: ")
    if er_id == "":
        return
    if find_patient_index(patients, er_id) != -1:                            # Bẫy 1
        print("\nMã ca cấp cứu đã tồn tại!")
        return

    name = " ".join(input("Nhập tên bệnh nhân: ").replace(SEPARATOR, " ").split()).title()
    if name == "":
        print("\nTên bệnh nhân không được để trống!")
        return

    while True:                                                              # Bẫy 2 (HR)
        hr_text = input("Nhập nhịp tim HR: ").strip()
        if hr_text.isdigit() and int(hr_text) > 0:
            break
        print("\nSinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")

    while True:                                                              # Bẫy 2 (TEMP)
        temp_text = input("Nhập nhiệt độ TEMP: ").strip()
        if is_valid_number(temp_text) and float(temp_text) >= MIN_TEMP:
            break
        print(f"Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng {MIN_TEMP}!")

    new_record = SEPARATOR.join([er_id, name, "HR:" + str(int(hr_text)),
                                 "TEMP:" + str(float(temp_text))])
    patients.append(new_record)
    print("\nTiếp nhận ca cấp cứu mới thành công!")
    print("Sau khi chuẩn hóa, dữ liệu được lưu là:")
    print(new_record)


def update_vitals(patients):
    """Chức năng 3: tách chuỗi -> sửa index 2 (HR) hoặc 3 (TEMP) -> join() -> gán đè."""
    print("--- CẬP NHẬT LẠI SINH HIỆU ---")
    er_id = read_er_id("Nhập mã ER cần cập nhật: ")
    if er_id == "":
        return
    index = find_patient_index(patients, er_id)
    if index == -1:
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return

    parts = patients[index].split(SEPARATOR)
    print(f"Tìm thấy bệnh nhân: {parts[1]}")
    print(f"Sinh hiệu hiện tại: {parts[2]} | {parts[3]}")
    print("Bạn muốn cập nhật:")
    print("1. Nhịp tim HR")
    print("2. Nhiệt độ TEMP")
    vital_choice = input("Chọn loại sinh hiệu: ").strip()

    if vital_choice == "1":
        value_text = input("Nhập nhịp tim mới: ").strip()
        if not (value_text.isdigit() and int(value_text) > 0):
            print("\nSinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!")
            return
        parts[2] = "HR:" + str(int(value_text))
        message = "Cập nhật nhịp tim thành công!"
    elif vital_choice == "2":
        value_text = input("Nhập nhiệt độ mới: ").strip()
        if not (is_valid_number(value_text) and float(value_text) >= MIN_TEMP):
            print(f"\nSinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng {MIN_TEMP}!")
            return
        parts[3] = "TEMP:" + str(float(value_text))
        message = "Cập nhật nhiệt độ thành công!"
    else:
        print("\nLựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2!")
        return

    patients[index] = SEPARATOR.join(parts)       # ghép lại và gán đè vào vị trí cũ
    print(f"\n{message}")


def trigger_red_alert(patients):
    """Chức năng 4: lọc bệnh nhân có HR > 100 hoặc TEMP >= 39.0 và in cảnh báo."""
    if is_empty(patients):
        return
    critical = []
    for record in patients:
        parts = record.split(SEPARATOR)
        if extract_vital_value(parts[2]) > ALERT_HR or extract_vital_value(parts[3]) >= ALERT_TEMP:
            critical.append(parts)

    if len(critical) == 0:
        print("--- KIỂM TRA BÁO ĐỘNG ĐỎ ---")
        print("Không có bệnh nhân nguy kịch tại thời điểm hiện tại.")
        return
    name_width = max(len(parts[1]) for parts in critical)
    print("\n!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!")
    for stt, (er_id, name, hr, temp) in enumerate(critical, start=1):
        print(f"{stt}. [{er_id}] {name:<{name_width}} | HR: {vital_text(hr):<3} bpm | "
              f"TEMP: {vital_text(temp)} °C | CẦN XỬ LÝ KHẨN CẤP")
    print("-" * 52)
    print(f"Tổng số ca nguy kịch: {len(critical)}")


def discharge_patient(patients):
    """Chức năng 5: xóa hồ sơ bệnh nhân xuất viện / chuyển khoa bằng pop()."""
    print("\n--- XUẤT VIỆN / CHUYỂN KHOA ---")
    er_id = read_er_id("Nhập mã ER cần xóa khỏi hệ thống: ")
    if er_id == "":
        return
    index = find_patient_index(patients, er_id)
    if index == -1:                                                          # Bẫy 3
        print("Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!")
        return
    removed = patients.pop(index)
    print(f"Đã chuyển khoa thành công cho bệnh nhân {removed.split(SEPARATOR)[1]}!")


# =====================================================================
# CHƯƠNG TRÌNH CHÍNH
# =====================================================================
def main():
    """Vòng lặp menu, điều hướng tới các hàm nghiệp vụ."""
    er_patients = [
        "ER01|Nguyen Van Quan|HR:115|TEMP:39.5",
        "ER02|Tran Thi Binh|HR:80|TEMP:37.0",
        "ER03|Le Van Cuong|HR:130|TEMP:38.2",
    ]
    while True:
        choice = display_menu()
        if choice == "1":
            display_dashboard(er_patients)
        elif choice == "2":
            admit_patient(er_patients)
        elif choice == "3":
            update_vitals(er_patients)
        elif choice == "4":
            trigger_red_alert(er_patients)
        elif choice == "5":
            discharge_patient(er_patients)
        elif choice == "6":
            print("Đã thoát hệ thống cấp cứu Rikkei ER. Cảm ơn bác sĩ!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập số từ 1-6!")


if __name__ == "__main__":
    main()
```

## Kết quả

Chạy thử toàn bộ chức năng và bẫy dữ liệu *(ẩn menu lặp lại)*:

```
Chọn chức năng (1-6): 1
--- BẢNG THEO DÕI CA CẤP CỨU ------------------------------------
1. [ER01] Nguyen Van Quan | Nhịp tim: 115 bpm | Nhiệt độ: 39.5 °C
2. [ER02] Tran Thi Binh   | Nhịp tim: 80  bpm | Nhiệt độ: 37.0 °C
3. [ER03] Le Van Cuong    | Nhịp tim: 130 bpm | Nhiệt độ: 38.2 °C
-----------------------------------------------------------------

Chọn chức năng (1-6): 4

!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!
1. [ER01] Nguyen Van Quan | HR: 115 bpm | TEMP: 39.5 °C | CẦN XỬ LÝ KHẨN CẤP
2. [ER03] Le Van Cuong    | HR: 130 bpm | TEMP: 38.2 °C | CẦN XỬ LÝ KHẨN CẤP
----------------------------------------------------
Tổng số ca nguy kịch: 2

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER:   er04
Nhập tên bệnh nhân:    pham thi dung
Nhập nhịp tim HR: 95
Nhập nhiệt độ TEMP: 39.2

Tiếp nhận ca cấp cứu mới thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
ER04|Pham Thi Dung|HR:95|TEMP:39.2

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER: er01

Mã ca cấp cứu đã tồn tại!

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER:  
Mã ER không được để trống!

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER: ER05
Nhập tên bệnh nhân:  

Tên bệnh nhân không được để trống!

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER: ER05
Nhập tên bệnh nhân: Nguyen Van Nam
Nhập nhịp tim HR: chin muoi

Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!
Nhập nhịp tim HR: 90
Nhập nhiệt độ TEMP: 37.8

Tiếp nhận ca cấp cứu mới thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
ER05|Nguyen Van Nam|HR:90|TEMP:37.8

Chọn chức năng (1-6): 2
--- TIẾP NHẬN CA CẤP CỨU MỚI ---
Nhập mã ER: ER06
Nhập tên bệnh nhân: Le Thi Hoa
Nhập nhịp tim HR: 88
Nhập nhiệt độ TEMP: 0
Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 36.5!
Nhập nhiệt độ TEMP: 38.0

Tiếp nhận ca cấp cứu mới thành công!
Sau khi chuẩn hóa, dữ liệu được lưu là:
ER06|Le Thi Hoa|HR:88|TEMP:38.0

Chọn chức năng (1-6): 3
--- CẬP NHẬT LẠI SINH HIỆU ---
Nhập mã ER cần cập nhật: er02
Tìm thấy bệnh nhân: Tran Thi Binh
Sinh hiệu hiện tại: HR:80 | TEMP:37.0
Bạn muốn cập nhật:
1. Nhịp tim HR
2. Nhiệt độ TEMP
Chọn loại sinh hiệu: 1
Nhập nhịp tim mới: 105

Cập nhật nhịp tim thành công!

Chọn chức năng (1-6): 3
--- CẬP NHẬT LẠI SINH HIỆU ---
Nhập mã ER cần cập nhật: ER01
Tìm thấy bệnh nhân: Nguyen Van Quan
Sinh hiệu hiện tại: HR:115 | TEMP:39.5
Bạn muốn cập nhật:
1. Nhịp tim HR
2. Nhiệt độ TEMP
Chọn loại sinh hiệu: 2
Nhập nhiệt độ mới: 38.6

Cập nhật nhiệt độ thành công!

Chọn chức năng (1-6): 3
--- CẬP NHẬT LẠI SINH HIỆU ---
Nhập mã ER cần cập nhật: ER99
Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!

Chọn chức năng (1-6): 3
--- CẬP NHẬT LẠI SINH HIỆU ---
Nhập mã ER cần cập nhật: ER02
Tìm thấy bệnh nhân: Tran Thi Binh
Sinh hiệu hiện tại: HR:105 | TEMP:37.0
Bạn muốn cập nhật:
1. Nhịp tim HR
2. Nhiệt độ TEMP
Chọn loại sinh hiệu: 5

Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2!

Chọn chức năng (1-6): 3
--- CẬP NHẬT LẠI SINH HIỆU ---
Nhập mã ER cần cập nhật: ER03
Tìm thấy bệnh nhân: Le Van Cuong
Sinh hiệu hiện tại: HR:130 | TEMP:38.2
Bạn muốn cập nhật:
1. Nhịp tim HR
2. Nhiệt độ TEMP
Chọn loại sinh hiệu: 1
Nhập nhịp tim mới: mot tram

Sinh hiệu không hợp lệ, vui lòng nhập số lớn hơn 0!

Chọn chức năng (1-6): 4

!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!
1. [ER01] Nguyen Van Quan | HR: 115 bpm | TEMP: 38.6 °C | CẦN XỬ LÝ KHẨN CẤP
2. [ER02] Tran Thi Binh   | HR: 105 bpm | TEMP: 37.0 °C | CẦN XỬ LÝ KHẨN CẤP
3. [ER03] Le Van Cuong    | HR: 130 bpm | TEMP: 38.2 °C | CẦN XỬ LÝ KHẨN CẤP
4. [ER04] Pham Thi Dung   | HR: 95  bpm | TEMP: 39.2 °C | CẦN XỬ LÝ KHẨN CẤP
----------------------------------------------------
Tổng số ca nguy kịch: 4

Chọn chức năng (1-6): 5

--- XUẤT VIỆN / CHUYỂN KHOA ---
Nhập mã ER cần xóa khỏi hệ thống: er02
Đã chuyển khoa thành công cho bệnh nhân Tran Thi Binh!

Chọn chức năng (1-6): 5

--- XUẤT VIỆN / CHUYỂN KHOA ---
Nhập mã ER cần xóa khỏi hệ thống: ER99
Không tìm thấy bệnh nhân. Vui lòng kiểm tra lại mã ER!

Chọn chức năng (1-6): 5

--- XUẤT VIỆN / CHUYỂN KHOA ---
Nhập mã ER cần xóa khỏi hệ thống:  
Mã ER không được để trống!

Chọn chức năng (1-6): 1
--- BẢNG THEO DÕI CA CẤP CỨU ------------------------------------
1. [ER01] Nguyen Van Quan | Nhịp tim: 115 bpm | Nhiệt độ: 38.6 °C
2. [ER03] Le Van Cuong    | Nhịp tim: 130 bpm | Nhiệt độ: 38.2 °C
3. [ER04] Pham Thi Dung   | Nhịp tim: 95  bpm | Nhiệt độ: 39.2 °C
4. [ER05] Nguyen Van Nam  | Nhịp tim: 90  bpm | Nhiệt độ: 37.8 °C
5. [ER06] Le Thi Hoa      | Nhịp tim: 88  bpm | Nhiệt độ: 38.0 °C
-----------------------------------------------------------------

Chọn chức năng (1-6): 7
Lựa chọn không hợp lệ, vui lòng nhập số từ 1-6!

Chọn chức năng (1-6): 6
Đã thoát hệ thống cấp cứu Rikkei ER. Cảm ơn bác sĩ!
```

Các trường hợp còn lại của chức năng 4 (gọi trực tiếp hàm):

```
>>> Chỉ có bệnh nhân sốt cao (HR 95, TEMP 39.2):

!!! BÁO ĐỘNG ĐỎ - DANH SÁCH BỆNH NHÂN NGUY KỊCH !!!
1. [ER04] Pham Thi Dung | HR: 95  bpm | TEMP: 39.2 °C | CẦN XỬ LÝ KHẨN CẤP
----------------------------------------------------
Tổng số ca nguy kịch: 1

>>> Không có bệnh nhân nguy kịch:
--- KIỂM TRA BÁO ĐỘNG ĐỎ ---
Không có bệnh nhân nguy kịch tại thời điểm hiện tại.

>>> Khoa cấp cứu trống:
Khoa cấp cứu hiện đang trống.
Khoa cấp cứu hiện đang trống.

>>> extract_vital_value:
115.0 39.5
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Bảng theo dõi mẫu | Chọn 1 | 3 ca, cột thẳng hàng (khớp đề) |
| Báo động đỏ mẫu | Chọn 4 | ER01 (HR 115), ER03 (HR 130); tổng 2 (khớp đề) |
| Tiếp nhận hợp lệ | `  er04`, `   pham thi dung`, 95, 39.2 | `ER04\|Pham Thi Dung\|HR:95\|TEMP:39.2` |
| Bẫy 1 - trùng mã | `er01` | Mã ca cấp cứu đã tồn tại! (khớp đề) |
| Mã ER / tên rỗng | khoảng trắng | ... không được để trống! (khớp đề) |
| Bẫy 2 - HR là chữ | `chin muoi` → 90 | Báo lỗi, nhập lại (khớp đề) |
| Bẫy 2 - TEMP = 0 | `0` → 38.0 | Phải ≥ 36.5, nhập lại (khớp đề) |
| Cập nhật HR / TEMP | `er02` HR 105; `ER01` TEMP 38.6 | Thành công (khớp đề) |
| Cập nhật: mã sai / loại sai / HR là chữ | `ER99`; `5`; `mot tram` | Báo lỗi tương ứng (khớp đề) |
| Báo động sau cập nhật | Chọn 4 | 4 ca (ER02 HR 105, ER04 sốt 39.2) |
| Chỉ sốt cao / không nguy kịch / trống | gọi hàm trực tiếp | 1 ca / thông báo không có / khoa trống (khớp đề) |
| Xuất viện | `er02` | Đã chuyển khoa thành công cho bệnh nhân Tran Thi Binh! (khớp đề) |
| Bẫy 3 - mã sai / rỗng | `ER99`, khoảng trắng | Báo lỗi (khớp đề) |
| Menu sai / thoát | `7`, `6` | Báo lỗi / thoát |

## Ghi chú

- Không dùng Dictionary: toàn bộ dữ liệu là chuỗi, mọi lần đọc / sửa đều đi qua `split("|")` và `"|".join()` đúng yêu cầu đề.
- Nhịp tim lưu dạng số nguyên (`HR:95`); nhiệt độ lưu dạng số thực (`TEMP:38.0` khi nhập `38`).
- Lỗi khi **tiếp nhận** cho nhập lại ngay; lỗi khi **cập nhật** báo rồi quay về menu, giống output mẫu của đề.
- Đề không có output mẫu cho chức năng 6; chương trình in "Đã thoát hệ thống cấp cứu Rikkei ER. Cảm ơn bác sĩ!".
