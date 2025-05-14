import numpy as np
import cv2
import os

# Label: 00000 là không cầm tiền, còn lại là các mệnh giá
label = "500000"

cap = cv2.VideoCapture(0)
frame_count = 0  # Đếm số frame từ khi bắt đầu
captured_images = 0  # Đếm số ảnh đã lưu
max_images = 1000  # Giới hạn số ảnh cần chụp

# Tạo thư mục nếu chưa có
save_path = f'data/{label}'
os.makedirs(save_path, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_count += 1  # Tăng bộ đếm frame
    frame = cv2.resize(frame, dsize=None, fx=0.3, fy=0.3)

    # Hiển thị frame
    cv2.imshow('frame', frame)

    # Bắt đầu lưu ảnh từ frame 60 trở đi
    if frame_count >= 60 and captured_images < max_images:
        filename = f"{save_path}/{captured_images + 1}.png"
        cv2.imwrite(filename, frame)
        captured_images += 1
        print(f"Đã chụp {captured_images}/{max_images} ảnh")

    # Dừng nếu đã chụp đủ 1000 ảnh hoặc frame_count đạt 1060
    if captured_images >= max_images or frame_count >= 460:
        print("Đã chụp đủ số lượng ảnh, kết thúc chương trình!")
        break

    # Thoát nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng camera và đóng cửa sổ
cap.release()
cv2.destroyAllWindows()
