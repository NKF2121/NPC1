!pip install git+https://github.com/JaidedAI/EasyOCR.git
from PIL import Image, ImageDraw, ImageFont
import easyocr
import numpy as np
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
# ==== Load OCR Reader (Thai + English) ====
def load_reader():
    return easyocr.Reader(['th', 'en'], gpu=False)

#Initialize EasyOCR reader
reader = load_reader()
# ---------------------------
# ฟังก์ชันโหลดภาพจาก URL
# ---------------------------
def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img
  def show_image(img):
    display(img)

#def show_image(image, title_image="Show Image"):
#  plt.title(title_image)
#  plt.imshow(image)
#  plt.show()
# ==== Sample Images ====
sample_images = {
    "sample_1": "https://metalbyexample.com/wp-content/uploads/figure-65.png",
    "sample_2": "https://i.ytimg.com/vi/Ch8YcYvSftw/maxresdefault.jpg",
    "sample_3": "https://m.media-amazon.com/images/I/41rLoTHkMbL.png"
}
image = load_image_from_url(sample_images["sample_1"])
show_image(image)
