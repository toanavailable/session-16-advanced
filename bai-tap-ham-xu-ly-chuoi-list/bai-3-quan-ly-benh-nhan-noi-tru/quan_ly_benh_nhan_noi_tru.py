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
