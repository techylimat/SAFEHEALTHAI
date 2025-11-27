# app/utils.py
from PIL import Image
import numpy as np
import io

def load_image_from_bytes(uploaded_file):
    img_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    return np.array(image)
