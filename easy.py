from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# โหลดโมเดล YOLO ที่ผ่านการเทรนมาแล้ว (YOLOv8 หรือ v5 ก็ใช้ได้)
model = YOLO('yolov8n.pt')  # 'yolov8n.pt' คือเวอร์ชันเล็กสุด ใช้งานเร็ว

# โหลดภาพที่ต้องการตรวจจับวัตถุ
image_path = 'your_image.jpg'
results = model(image_path)

# แสดงผลวัตถุที่ตรวจเจอ
for result in results:
    for box in result.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        print(f"ตรวจพบวัตถุ: {label}")

# แสดงภาพพร้อมกล่องขอบเขต
results[0].show()
