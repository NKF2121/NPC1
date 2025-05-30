import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

# โหลดโมเดล YOLOv8 (ขนาดเล็ก โหลดเร็ว)
model = YOLO('yolov8n.pt')

st.title("🧠 ตรวจจับวัตถุจากภาพ (ฝัง URL โดยตรง)")

# URL ของภาพ (ไม่ต้องรับจากผู้ใช้)
image_url = "https://www.thehrdigest.com/wp-content/uploads/2021/12/5-Types-of-People-e1640865120273.jpg"

# ดาวน์โหลดและแสดงภาพ
try:
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    
    st.image(image, caption="📷 ภาพจาก URL", use_container_width=True)

    # ตรวจจับวัตถุ
    results = model(image)

    # แสดงผลภาพที่ตรวจจับแล้ว
    st.subheader("🎯 ผลลัพธ์การตรวจจับวัตถุ:")
    result_image = results[0].plot()
    st.image(result_image, use_container_width=True)

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
    st.error(f"เกิดข้อผิดพลาดในการโหลดหรือประมวลผลภาพ: {e}")
