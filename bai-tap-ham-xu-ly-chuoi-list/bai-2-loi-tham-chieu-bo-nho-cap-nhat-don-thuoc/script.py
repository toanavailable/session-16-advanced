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
