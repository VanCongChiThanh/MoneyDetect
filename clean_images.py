import os
import cv2
import numpy as np
from PIL import Image
import imagehash

# ===============================
# 1. XÓA ẢNH KHÔNG HỢP LỆ
# ===============================
def remove_invalid_images(folder_path, min_size_kb=5, min_resolution=(100, 100)):
    removed = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            file_path = os.path.join(root, file)
            try:
                img = Image.open(file_path)
                img_gray = img.convert('L')
                arr = np.array(img_gray)

                # Kiểm tra ảnh trắng/đen gần như tuyệt đối
                if arr.std() < 3:
                    os.remove(file_path)
                    print(f"[X] Ảnh trắng/đen: {file_path}")
                    removed += 1
                    continue

                # Kiểm tra kích thước nhỏ
                if img.size[0] < min_resolution[0] or img.size[1] < min_resolution[1]:
                    os.remove(file_path)
                    print(f"[X] Ảnh kích thước nhỏ: {file_path}")
                    removed += 1
                    continue

                # Kiểm tra dung lượng file
                if os.path.getsize(file_path) < min_size_kb * 1024:
                    os.remove(file_path)
                    print(f"[X] Ảnh dung lượng nhỏ: {file_path}")
                    removed += 1
                    continue

            except Exception as e:
                os.remove(file_path)
                print(f"[X] Không thể mở ảnh: {file_path}")
                removed += 1
    print(f"Tổng số ảnh không hợp lệ đã xóa: {removed}")


# ===============================
# 2. XÓA ẢNH TRÙNG LẶP
# ===============================
def remove_duplicate_images(folder_path):
    seen_hashes = {}
    removed = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img_hash = imagehash.phash(img)

                if img_hash in seen_hashes:
                    os.remove(file_path)
                    print(f"[X] Ảnh trùng: {file_path}")
                    removed += 1
                else:
                    seen_hashes[img_hash] = file_path
            except:
                continue
    print(f"Tổng số ảnh trùng lặp đã xóa: {removed}")


# ===============================
# 3. LIỆT KÊ ẢNH NGHI NGỜ SAI CHỦ ĐỀ
# ===============================
def list_suspect_images(folder_path):
    print("\n== Danh sách ảnh nghi ngờ sai chủ đề ==")
    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            file_path = os.path.join(root, file)
            try:
                img = cv2.imread(file_path)
                h, w = img.shape[:2]

                # Ảnh rất dọc hoặc rất ngang, nghi ngờ infographic
                if h / w > 2.5 or w / h > 2.5:
                    print(f"Ảnh tỷ lệ lạ: {file_path}")

                # Ảnh có ít màu (có thể là vẽ hoặc biểu đồ)
                if len(np.unique(img.reshape(-1, img.shape[2]), axis=0)) < 30:
                    print(f"Ảnh màu ít (nghi ngờ vẽ): {file_path}")

            except:
                continue
    print("== Hết danh sách ảnh nghi ngờ ==\n")


# ===============================
# CHẠY TOÀN BỘ
# ===============================
if __name__ == "__main__":
    data_dir = "D:\Ki2_Nam3\MoneyDetectVN\data\10 euro banknote front"  # đổi thành thư mục ảnh của bạn nếu khác

    print("👉 Bắt đầu xoá ảnh không hợp lệ...")
    remove_invalid_images(data_dir)

    print("\n👉 Bắt đầu xoá ảnh trùng lặp...")
    remove_duplicate_images(data_dir)

    print("\n👉 Liệt kê ảnh nghi sai chủ đề để kiểm tra bằng tay...")
    list_suspect_images(data_dir)
