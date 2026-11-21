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
