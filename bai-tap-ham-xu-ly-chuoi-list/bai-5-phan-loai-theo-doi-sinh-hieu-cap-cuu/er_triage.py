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
