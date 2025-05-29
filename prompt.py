import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from ultralytics import YOLO

st.set_page_config(page_title="Object Detection", layout="centered")
st.title("🔍 ตรวจจับวัตถุในภาพ (Object Detection)")

# โหลดโมเดล YOLOv5
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # ใช้โมเดลขนาดเล็ก

model = load_model()

# เลือกว่าจะใช้ URL หรือ Upload
option = st.radio("เลือกรูปภาพ:", ["📷 อัปโหลดไฟล์", "🌐 ใส่ URL"])

image = None

if option == "📷 อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

elif option == "🌐 ใส่ URL":
    url = st.text_input("URL ของภาพ", "https://media.istockphoto.com/id/467652436/photo/cats-and-dogs.jpg")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            st.error(f"โหลดภาพไม่สำเร็จ: {e}")

if image:
    st.image(image, caption="ภาพต้นฉบับ", use_column_width=True)

    # ตรวจจับวัตถุ
    st.markdown("### 🔍 กำลังตรวจจับวัตถุ...")
    results = model(image)

    # แสดงผลภาพที่มี bounding box
    result_image = results[0].plot()
    st.image(result_image, caption="📦 วัตถุที่พบ", use_column_width=True)

    # แสดงวัตถุที่พบ
    boxes = results[0].boxes
    classes = boxes.cls.tolist()
    names = results[0].names

    detected_objects = [names[int(cls)] for cls in classes]
    if detected_objects:
        st.success(f"🔎 วัตถุที่ตรวจพบ: {', '.join(set(detected_objects))}")
    else:
        st.warning("ไม่พบวัตถุที่รู้จักในภาพนี้")
