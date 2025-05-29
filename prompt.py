import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="เลือกดูรูปภาพ", layout="centered")
st.title("เลือกดูรูปภาพสัตว์เลี้ยง")

# รายการ URL ของรูปภาพ
image_urls = {
    "สุนัข": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg",
    "แมวสูงวัย": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

# ฟังก์ชันโหลดรูปภาพจาก URL
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพจาก URL: {e}")
        return None

# สร้าง thumbnail
cols = st.columns(len(image_urls))
selected = None

for i, (label, url) in enumerate(image_urls.items()):
    with cols[i]:
        image = load_image(url)
        if image:
            if st.button(label, key=label):
                selected = label
            st.image(image.resize((150, 100)), caption=label)

# แสดงภาพที่เลือกในขนาดใหญ่
if selected:
    st.subheader(f"ภาพขนาดใหญ่: {selected}")
    big_image = load_image(image_urls[selected])
    if big_image:
        st.image(big_image, use_column_width=True)
