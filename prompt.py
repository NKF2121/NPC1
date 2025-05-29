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
# -------------------------------
# ส่วน UI
# -------------------------------
st.title("Interactive Image Processing with scikit-image")

st.subheader("เลือกภาพตัวอย่าง")
cols = st.columns(2)

for i, (label, url) in enumerate(image_options.items()):
    with cols[i]:
        st.image(url, caption=label, width=200)
        if st.button(f"เลือก {label}"):
            st.session_state.original_image = load_image_from_url(url)
            st.session_state.reset = True  # trigger reset
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

# -------------------------------
# ถ้ามีภาพที่โหลดแล้ว
# -------------------------------
if 'original_image' in st.session_state:
    if 'reset' not in st.session_state or st.session_state.reset:
        st.session_state.resize_scale = 1.0
        st.session_state.angle = 0
        st.session_state.flip_option = "None"
        st.session_state.reset = False

    image = st.session_state.original_image

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

    # ----------------------------
    # Rotate
    # ----------------------------
    st.subheader("หมุนภาพ (Rotate Image)")
    angle = st.slider("เลือกองศาในการหมุน", -180, 180, st.session_state.angle)
    st.session_state.angle = angle
    rotated_image = transform.rotate(resized_image, angle)
