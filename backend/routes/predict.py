import random

import numpy as np
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from pydantic import BaseModel

from utils.advisory import estimate_severity, get_advisory
from utils.gradcam import GradCAM
from utils.image_utils import array_to_base64, preprocess_image

router = APIRouter()

CLASS_NAMES = ["Bacterial_Blight", "Blast", "Brown_Spot", "Tungro"]


class PredictionResponse(BaseModel):
    disease: str
    disease_display: str
    confidence: float
    severity: str
    affected_area: float
    all_probabilities: dict
    advisory: dict
    gradcam_overlay: str


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size must be under 10MB.")

    img_array = preprocess_image(file_bytes)
    demo_mode = getattr(request.app.state, "demo_mode", False)

    if demo_mode:
        pred_idx = random.randint(0, len(CLASS_NAMES) - 1)
        pred_class = CLASS_NAMES[pred_idx]
        confidence = round(random.uniform(0.75, 0.98), 4)

        remaining = 1.0 - confidence
        probs = []
        for index in range(len(CLASS_NAMES)):
            if index == pred_idx:
                probs.append(confidence)
            else:
                probs.append(round(remaining / (len(CLASS_NAMES) - 1), 4))

        predictions = np.array(probs)
        affected_area = round(random.uniform(0.1, 0.7), 4)
        overlay_b64 = array_to_base64(img_array)
    else:
        model = request.app.state.model
        batch = img_array[np.newaxis]

        predictions = model.predict(batch, verbose=0)[0]
        pred_idx = int(np.argmax(predictions))
        pred_class = CLASS_NAMES[pred_idx]
        confidence = float(predictions[pred_idx])

        sorted_probs = np.sort(predictions)[::-1]
        top1 = sorted_probs[0]
        top2 = sorted_probs[1]

        if confidence < 0.7 or (top1 - top2) < 0.2:
            raise HTTPException(
                status_code=400,
                detail="Invalid or unclear image. Please upload a proper rice leaf image.",
            )

        gcam = GradCAM(model)
        heatmap, _, _ = gcam.compute_heatmap(batch, class_idx=pred_idx)
        overlay = gcam.overlay_heatmap(heatmap, img_array)
        affected_area = gcam.compute_affected_area(heatmap)
        overlay_b64 = array_to_base64(overlay)

    severity = estimate_severity(affected_area)
    advisory = get_advisory(pred_class, severity)

    return PredictionResponse(
        disease=pred_class,
        disease_display=pred_class.replace("_", " "),
        confidence=round(confidence * 100, 2),
        severity=severity,
        affected_area=round(affected_area * 100, 2),
        all_probabilities={
            CLASS_NAMES[index].replace("_", " "): round(float(probability) * 100, 2)
            for index, probability in enumerate(predictions)
        },
        advisory=advisory,
        gradcam_overlay=overlay_b64,
    )


@router.get("/classes")
async def get_classes():
    return {
        "classes": [class_name.replace("_", " ") for class_name in CLASS_NAMES],
        "count": len(CLASS_NAMES),
    }
