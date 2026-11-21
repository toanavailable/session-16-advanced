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
