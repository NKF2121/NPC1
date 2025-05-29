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

import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="Blend รูปแมว", layout="centered")
st.title("😺 ผสมภาพแมว + ปรับขนาด + แสดงแกน X/Y")

# URLs ของภาพแมว 2 ใบ
image1_url = "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg"
image2_url = "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"

# โหลดรูปภาพ
@st.cache_data
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        st.error(f"โหลดภาพไม่สำเร็จ: {e}")
        return None

# วาดแกน X/Y
def draw_axes(image, step=50):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    font = ImageFont.load_default()
    # แกน X
    for x in range(0, width, step):
        draw.line([(x, 0), (x, 10)], fill="red", width=1)
        draw.text((x + 2, 2), str(x), fill="red", font=font)
    # แกน Y
    for y in range(0, height, step):
        draw.line([(0, y), (10, y)], fill="blue", width=1)
        draw.text((2, y + 2), str(y), fill="blue", font=font)
    return image

# โหลดทั้งสองภาพ
img1 = load_image(image1_url)
img2 = load_image(image2_url)

if img1 and img2:
    st.markdown("### 🔄 ปรับระดับการผสมภาพ (Blending)")
    alpha = st.slider("ระดับการผสม (0.0 = เฉพาะภาพที่ 2, 1.0 = เฉพาะภาพที่ 1)", 0.0, 1.0, 0.5, 0.01)

    # Resize ให้ขนาดเท่ากันก่อน Blend
    min_width = min(img1.width, img2.width)
    min_height = min(img1.height, img2.height)
    img1_resized = img1.resize((min_width, min_height))
    img2_resized = img2.resize((min_width, min_height))

    blended = Image.blend(img1_resized, img2_resized, alpha)

    st.markdown("### 📐 ปรับขนาดภาพหลังการผสม")
    new_w = st.slider("ความกว้าง (px)", 50, min_width * 2, min_width)
    new_h = st.slider("ความสูง (px)", 50, min_height * 2, min_height)

    resized_blended = blended.resize((new_w, new_h))
    final_image = draw_axes(resized_blended.copy(), step=50)

    st.image(final_image, caption=f"ภาพแมว Blended ขนาด {new_w}x{new_h} px", use_container_width=False)
