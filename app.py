import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
import os

# โหลดโมเดล YOLOv8 (ใช้เวอร์ชันเล็กเพื่อลดเวลา)
model = YOLO('yolov8n.pt')  # สามารถเปลี่ยนเป็น 'yolov8s.pt' หรืออื่น ๆ ได้

st.title("🔍 ตรวจจับวัตถุในภาพด้วย YOLOv8")

uploaded_file = st.file_uploader("📷 อัปโหลดภาพที่ต้องการตรวจจับวัตถุ", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # แสดงภาพต้นฉบับ
    image = Image.open(uploaded_file)
    st.image(image, caption='ภาพที่อัปโหลด', use_column_width=True)

    # บันทึกไฟล์ชั่วคราว
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        image.save(tmp.name)
        temp_path = tmp.name

    # ตรวจจับวัตถุด้วย YOLO
    results = model(temp_path)

    # แสดงผลลัพธ์เป็นภาพ
    st.subheader("🎯 ผลลัพธ์การตรวจจับวัตถุ:")
    result_image = results[0].plot()  # วาดกล่องรอบวัตถุ
    st.image(result_image, use_column_width=True)

    # แสดงชื่อวัตถุที่ตรวจจับได้
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
