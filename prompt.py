import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="เลือกดูรูปภาพสัตว์เลี้ยง", layout="centered")
st.title("🐾 เลือกรูปสัตว์เลี้ยง & ปรับขนาดภาพพร้อมแกน X/Y")

# URLs ของภาพ
image_urls = {
    "สุนัข": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg",
    "แมวสูงวัย": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

# โหลดภาพจาก URL
@st.cache_data
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
        return None

# วาดแกน X/Y ตรงขอบภาพ
def draw_axes(image, step=50):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.load_default()

    # วาดแกน X (บน)
    for x in range(0, width, step):
        draw.line([(x, 0), (x, 10)], fill="red", width=1)
        draw.text((x + 2, 2), str(x), fill="red", font=font)

    # วาดแกน Y (ซ้าย)
    for y in range(0, height, step):
        draw.line([(0, y), (10, y)], fill="blue", width=1)
        draw.text((2, y + 2), str(y), fill="blue", font=font)

    return image

# แสดง thumbnails + ปุ่มเลือก
st.markdown("### 🔽 เลือกภาพ")
cols = st.columns(len(image_urls))
selected = None

for i, (label, url) in enumerate(image_urls.items()):
    with cols[i]:
        image = load_image(url)
        if image:
            st.image(image.resize((150, 100)), caption=label)
            if st.button(f"เลือก {label}", key=label):
                selected = label

# แสดงภาพใหญ่ พร้อม resize + แกน
if selected:
    st.markdown(f"### 📸 ภาพที่เลือก: **{selected}**")
    image = load_image(image_urls[selected])
    if image:
        orig_w, orig_h = image.size
        st.write(f"ขนาดต้นฉบับ: {orig_w} x {orig_h} px")

        # sliders สำหรับปรับขนาด
        new_w = st.slider("ความกว้าง (px)", 50, orig_w * 2, orig_w)
        new_h = st.slider("ความสูง (px)", 50, orig_h * 2, orig_h)

        # resize และวาดแกน
        resized = image.resize((new_w, new_h))
        image_with_axes = draw_axes(resized.copy(), step=50)

        st.image(image_with_axes, caption=f"{new_w} x {new_h} px พร้อมแกน X/Y", use_container_width=False)
