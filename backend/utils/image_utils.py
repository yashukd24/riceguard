import base64
import io

import numpy as np
from PIL import Image

from utils.gradcam import GradCAM

IMG_SIZE = (224, 224)


def preprocess_image(file_bytes: bytes) -> np.ndarray:
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE, Image.LANCZOS)
    return np.array(img, dtype=np.float32)


def array_to_base64(img_array: np.ndarray) -> str:
    image = Image.fromarray(img_array.astype(np.uint8))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def compute_gradcam_overlay(model, img_array: np.ndarray):
    gcam = GradCAM(model)
    heatmap, pred_idx, confidence = gcam.compute_heatmap(img_array[np.newaxis])
    overlay = gcam.overlay_heatmap(heatmap, img_array)
    affected_area = gcam.compute_affected_area(heatmap)
    overlay_b64 = array_to_base64(overlay)

    return pred_idx, confidence, affected_area, overlay_b64
