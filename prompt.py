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

# แสดงภาพที่เลือกในขนาดใหญ่ พร้อมแกน X Y และการ Resize
if selected:
    st.subheader(f"ภาพขนาดใหญ่: {selected}")
    big_image = load_image(image_urls[selected])
    if big_image:
        orig_width, orig_height = big_image.size
        st.write(f"📏 ขนาดต้นฉบับ: {orig_width} x {orig_height} พิกเซล")

        # ปรับขนาดใหม่
        st.markdown("### 🔧 ปรับขนาดภาพ")
        new_width = st.slider("ความกว้าง (px)", min_value=50, max_value=orig_width * 2, value=orig_width)
        new_height = st.slider("ความสูง (px)", min_value=50, max_value=orig_height * 2, value=orig_height)

        resized_image = big_image.resize((new_width, new_height))
        st.write(f"🖼️ ขนาดใหม่: {new_width} x {new_height} พิกเซล")
        st.image(resized_image, use_container_width=False)
