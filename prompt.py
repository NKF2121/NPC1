import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("เลือกรูปภาพจากเว็บไซต์แล้วแสดง")

# ตัวเลือก URL รูปภาพ
image_options = {
    "Bulldog Inglese": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Old Cat": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

# เลือกรูปภาพ
selected_label = st.selectbox("เลือกรูปภาพ", list(image_options.keys()))

# ดึง URL ของรูปภาพที่เลือก
selected_url = image_options[selected_label]

# โหลดรูปจาก URL
try:
    response = requests.get(selected_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))

    # แสดงรูป
    st.image(image, caption=selected_label, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดรูปภาพ: {e}")
