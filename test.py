import cv2
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
from Resnet18 import BasicBlock, CustomResNet
# Lớp tên (thay bằng danh sách đúng của bạn nếu không dùng train_dataset.classes)
class_names = [
    '000000',        # 0
    'euro_10',       # 1
    'euro_20',       # 2
    'euro_5',        # 3
    'euro_50',       # 4
    'usd_1',         # 5
    'usd_10',        # 6
    'usd_100',       # 7
    'usd_5',         # 8
    'usd_50',        # 9
    'vnd_1000',      # 10
    'vnd_10000',     # 11
    'vnd_100000',    # 12
    'vnd_200',       # 13
    'vnd_2000',      # 14
    'vnd_20000',     # 15
    'vnd_200000',    # 16
    'vnd_500',       # 17
    'vnd_5000',      # 18
    'vnd_50000',     # 19
    'vnd_500000',    # 20
    'won_1000',      # 21
    'won_10000',     # 22
    'won_5000'       # 23
]

# Thiết bị sử dụng
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = r'D:\Ki2_Nam3\MoneyDetect\resnet18_best_money.pth'
model = torch.load(model_path, map_location=DEVICE)

model = CustomResNet(BasicBlock, [2, 2, 2, 2], num_classes=len(class_names))
model.load_state_dict(torch.load(model_path, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

# Transform ảnh từ webcam
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# Mở webcam
cap = cv2.VideoCapture(0)  # 0 là camera mặc định

if not cap.isOpened():
    print("❌ Không thể mở webcam")
    exit()

print("📷 Webcam đang chạy... Nhấn 'q' để thoát.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Không nhận được khung hình từ webcam")
        break

    # Chuyển frame (OpenCV dùng BGR) sang PIL RGB để xử lý
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)

    # Tiền xử lý
    input_tensor = transform(pil_img).unsqueeze(0).to(DEVICE)

    # Dự đoán
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        max_prob, predicted = torch.max(probabilities, 1)
        predicted_class = class_names[predicted.item()]
        confidence = max_prob.item()

    # Ghi kết quả lên ảnh nếu độ chính xác > 80%
    if confidence >= 0.8:
        label = f'Prediction: {predicted_class} ({confidence*100:.1f}%)'
    else:
        label = 'Prediction: ???'

    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2, cv2.LINE_AA)

    # Hiển thị ảnh có kết quả
    cv2.imshow("Real-time Detection", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
