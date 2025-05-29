import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.set_page_config(page_title="เลือกดูรูปภาพ", layout="centered")
st.title("เลือกดูรูปภาพสัตว์เลี้ยง")

# URL ของรูปภาพ
image_urls = {
    "สุนัข": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "แมว": "https://cdn.britannica.com/39/226539-050-D21D7721/Portrait-of-a-cat-with-whiskers-visible.jpg",
    "แมวสูงวัย": "https://vetmarlborough.co.nz/wp-content/uploads/old-cats.jpg"
}

# โหลดรูปภาพ
def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        st.error(f"ไม่สามารถโหลดรูปภาพ: {e}")
        return None

# แสดงภาพต้นฉบับ
    st.subheader("ภาพต้นฉบับ (Original Image with Axes)")
    fig_orig, ax_orig = plt.subplots()
    ax_orig.imshow(image)
    ax_orig.set_title("Original Image")
    ax_orig.set_xlabel("X (Column)")
    ax_orig.set_ylabel("Y (Row)")
    st.pyplot(fig_orig)

    # ----------------------------
    # Resize
    # ----------------------------
    st.subheader("ปรับขนาด (Resize Image)")
    resize_scale = st.slider("ปรับขนาด (0.1 = เล็กลง, 2.0 = ใหญ่ขึ้น)", 0.1, 2.0, st.session_state.resize_scale, step=0.1)
    st.session_state.resize_scale = resize_scale
    resized_image = transform.rescale(image, resize_scale, channel_axis=2, anti_aliasing=True)
# ส่วนแสดงรูปขนาดเล็ก
cols = st.columns(len(image_urls))
selected = None

for i, (label, url) in enumerate(image_urls.items()):
    with cols[i]:
        img = load_image(url)
        if img:
            if st.button(label):
                selected = label
            st.image(img.resize((150, 100)), caption=label)

# แสดงภาพที่เลือกพร้อมปรับขนาดและแกน
if selected:
    st.subheader(f"ภาพที่เลือก: {selected}")
    img = load_image(image_urls[selected])
    if img:
        orig_w, orig_h = img.size
        st.write(f"📏 ขนาดต้นฉบับ: {orig_w} x {orig_h} px")

        # ปรับขนาด
        new_w = st.slider("ความกว้าง (px)", 50, orig_w * 2, orig_w)
        new_h = st.slider("ความสูง (px)", 50, orig_h * 2, orig_h)

        resized = img.resize((new_w, new_h))

        # วาดแกน
        image_with_axes = draw_axes(resized.copy(), step=50)

        st.write(f"📐 ขนาดใหม่: {new_w} x {new_h} px พร้อมแกน X/Y ทุก 50px")
        st.image(image_with_axes, use_container_width=False)
