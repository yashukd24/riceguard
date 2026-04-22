
#uvicorn main:app --reload --host 0.0.0.0 --port 8000
from contextlib import asynccontextmanager
import os
from pathlib import Path

import tensorflow as tf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.predict import router as predict_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    default_model_path = Path(__file__).resolve().parent.parent / "models" / "riceguard_efficientnetb0.h5"
    model_path = Path(os.getenv("MODEL_PATH", str(default_model_path))).resolve()

    if not model_path.exists():
        print(f"Model not found at {model_path}. Running in demo mode.")
        print("Add the trained model file to models/riceguard_efficientnetb0.h5.")
        app.state.model = None
        app.state.demo_mode = True
    else:
        print(f"Loading model from {model_path}")
        app.state.model = tf.keras.models.load_model(model_path)
        app.state.demo_mode = False
        print("Model loaded and ready.")

    yield

    if getattr(app.state, "model", None) is not None:
        del app.state.model


app = FastAPI(
    title="RiceGuard AI API",
    description="CNN-Based Rice Leaf Disease Diagnosis and Advisory System using EfficientNetB0",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router, prefix="/api", tags=["Prediction"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "RiceGuard AI is running",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "model": "EfficientNetB0"}
