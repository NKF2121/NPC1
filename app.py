import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv8
model = YOLO('yolov8n.pt')

st.title("🔎 ตรวจจับวัตถุจาก URL ของภาพด้วย YOLOv8")

# รับ URL จากผู้ใช้
image_url = st.text_input("📌 วาง URL ของภาพที่ต้องการตรวจจับวัตถุ")

if image_url:
    try:
        # ดาวน์โหลดภาพจาก URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")

        # แสดงภาพต้นฉบับ
        st.image(image, caption="ภาพจาก URL", use_column_width=True)

        # ตรวจจับวัตถุ
        results = model(image)

        # แสดงผลภาพที่มีการตรวจจับ
        st.subheader("🎯 ผลลัพธ์การตรวจจับวัตถุ:")
        result_image = results[0].plot()
        st.image(result_image, use_column_width=True)

        # แสดงวัตถุที่ตรวจพบ
        st.subheader("📌 วัตถุที่พบในภาพ:")
        detected_objects = set()
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detected_objects.add(label)

        if detected_objects:
            for obj in detected_objects:
                st.write(f"✅ {obj}")
        else:
            st.write("❌ ไม่พบวัตถุในภาพ")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดภาพ: {e}")
