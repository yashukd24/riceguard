import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from utils.config import CLASS_NAMES, IMG_SIZE


class GradCAM:
    def __init__(self, model, layer_name="top_activation"):
        self.model = model
        self.base_model = model.get_layer("efficientnetb0")
        self.grad_base_model = tf.keras.models.Model(
            inputs=self.base_model.inputs,
            outputs=[self.base_model.get_layer(layer_name).output, self.base_model.output],
        )

    def compute_heatmap(self, img_array, class_idx=None):
        img_tensor = tf.cast(img_array, tf.float32)

        with tf.GradientTape() as tape:
            conv_outputs, base_outputs = self.grad_base_model(img_tensor, training=False)
            tape.watch(conv_outputs)

            predictions = base_outputs
            for layer in self.model.layers:
                if layer.name in ["input_layer", "efficientnetb0"]:
                    continue
                predictions = layer(predictions, training=False)

            if class_idx is None:
                class_idx = int(tf.argmax(predictions[0]))
            loss = predictions[:, class_idx]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)

        confidence = float(predictions[0][class_idx])
        return heatmap.numpy(), class_idx, confidence

    def overlay_heatmap(self, heatmap, original_img, alpha=0.45):
        heatmap_resized = cv2.resize(heatmap, IMG_SIZE)
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)

        img_bgr = cv2.cvtColor(original_img.astype(np.uint8), cv2.COLOR_RGB2BGR)
        superimposed = cv2.addWeighted(img_bgr, 1 - alpha, heatmap_colored, alpha, 0)
        return cv2.cvtColor(superimposed, cv2.COLOR_BGR2RGB)

    def compute_affected_area(self, heatmap, threshold=0.5):
        resized = cv2.resize(heatmap, IMG_SIZE)
        return float(np.sum(resized >= threshold) / resized.size)


def generate_gradcam(model, img_array, save_path=None):
    gcam = GradCAM(model)
    heatmap, pred_idx, confidence = gcam.compute_heatmap(img_array[np.newaxis])
    overlay = gcam.overlay_heatmap(heatmap, img_array)
    affected_area = gcam.compute_affected_area(heatmap)
    pred_class = CLASS_NAMES[pred_idx]

    if save_path:
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        fig.suptitle(
            f"Grad-CAM | {pred_class.replace('_', ' ')} ({confidence * 100:.1f}%)",
            fontsize=13,
            fontweight="bold",
        )
        axes[0].imshow(img_array.astype(np.uint8))
        axes[0].set_title("Original")
        axes[0].axis("off")
        axes[1].imshow(cv2.resize(heatmap, IMG_SIZE), cmap="jet")
        axes[1].set_title("Heatmap")
        axes[1].axis("off")
        axes[2].imshow(overlay)
        axes[2].set_title(f"Overlay ({affected_area * 100:.1f}% affected)")
        axes[2].axis("off")
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()

    return pred_class, confidence, affected_area, overlay
