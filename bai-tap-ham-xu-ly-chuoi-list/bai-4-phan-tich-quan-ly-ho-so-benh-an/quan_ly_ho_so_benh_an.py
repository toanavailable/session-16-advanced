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
