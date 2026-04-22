import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

model = tf.keras.models.load_model("models/riceguard_efficientnetb0.h5")

classes = ["Bacterial Blight", "Blast", "Brown Spot", "Tungro"]

def predict(image):
    img = image.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img)[0]
    idx = np.argmax(preds)

    return f"Prediction: {classes[idx]} (Confidence: {preds[idx]*100:.2f}%)"

interface = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="RiceGuard AI 🌾",
    description="Upload a rice leaf image to detect disease"
)

interface.launch()