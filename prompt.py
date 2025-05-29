import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ตั้งชื่อหน้า
st.title("แสดงรูปภาพจาก URL")

# URL ของรูปภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# โหลดรูปภาพจาก URL
try:
    response = requests.get(image_url)
    response.raise_for_status()  # ตรวจสอบว่าโหลดสำเร็จ
    image = Image.open(BytesIO(response.content))

    # แสดงรูปภาพ
    st.image(image, caption="Bulldog Inglese", use_column_width=True)

except requests.exceptions.RequestException as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดรูปภาพ: {e}")
