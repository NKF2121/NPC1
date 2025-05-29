import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ฟังก์ชันโหลดภาพจาก URL
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"โหลดภาพไม่ได้: {e}")
        return None

# URLs ของภาพ
image_urls = {
    "Bulldog Inglese": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Old Cat": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

st.title("เลือกภาพเพื่อดูแบบขนาดใหญ่")

# สร้างคอลัมน์เล็กแสดง thumbnails
cols = st.columns(len(image_urls))

# เก็บภาพและชื่อภาพที่ผู้ใช้เลือก
selected_image = None

for i, (name, url) in enumerate(image_urls.items()):
    with cols[i]:
        image = load_image(url)
        if image:
            if st.button(f"ดู {name}"):
                selected_image = (name, image)
            st.image(image, caption=name, use_container_width=True)

# แสดงภาพที่เลือก
if selected_image:
    st.subheader(f"แสดงภาพ: {selected_image[0]}")
    st.image(selected_image[1], use_container_width=True)
