# 🌾 RiceGuard AI
## CNN-Based Rice Leaf Disease Diagnosis and Advisory System

> **Department of AIML | Dayananda Sagar University, Bangalore**
> Team: Yashu · Rubin Raj S · Abilash A | Mentor: Dr. Vegi Fernando A

---

## 📁 Full Project Structure

```
riceguard/
│
├── ml/                              ← Machine Learning Module
│   ├── dataset/                     ← Place Kaggle dataset here
│   │   ├── Bacterial_Blight/
│   │   ├── Blast/
│   │   ├── Brown_Spot/
│   │   └── Tungro/
│   ├── models/                      ← Saved model (auto-created after training)
│   ├── results/                     ← Training plots & Grad-CAM outputs
│   ├── config.py                    ← Hyperparameters & paths
│   ├── data_loader.py               ← Dataset loading & augmentation
│   ├── model.py                     ← EfficientNetB0 architecture
│   ├── gradcam.py                   ← Grad-CAM explainability
│   ├── advisory.py                  ← Severity + rule-based advisory engine
│   ├── train.py                     ← Training pipeline
│   └── requirements.txt
│
├── backend/                         ← FastAPI Backend
│   ├── main.py                      ← FastAPI app entry point
│   ├── routes/
│   │   └── predict.py               ← /api/predict endpoint
│   ├── utils/
│   │   └── image_utils.py           ← Image preprocessing helpers
│   └── requirements.txt
│
├── frontend/                        ← React Frontend
│   ├── public/index.html
│   ├── src/
│   │   ├── App.jsx                  ← Main app
│   │   ├── index.js                 ← Entry point
│   │   ├── index.css                ← Global styles
│   │   └── components/
│   │       ├── Header.jsx
│   │       ├── UploadSection.jsx    ← Drag & drop upload
│   │       ├── ResultSection.jsx    ← Results container
│   │       ├── DiagnosisCard.jsx    ← Disease + confidence
│   │       ├── ProbabilityChart.jsx ← All class probabilities
│   │       ├── GradCAMPanel.jsx     ← Heatmap visualization
│   │       ├── AdvisoryPanel.jsx    ← Treatment advisory
│   │       └── LoadingSpinner.jsx
│   └── package.json
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml               ← Full stack deployment
├── nginx.conf
└── README.md
```

---

## 🧠 Model: EfficientNetB0

| Property | Value |
|----------|-------|
| Backbone | EfficientNetB0 (ImageNet) |
| Parameters | ~5.3M (vs VGG16's 138M) |
| Input Size | 224 × 224 × 3 |
| Classes | 4 rice diseases |
| Explainability | Grad-CAM (top_activation layer) |
| Training | 2-phase transfer learning |

### Architecture
```
Input (224×224×3)
  └── EfficientNetB0 (frozen Phase 1 → fine-tuned Phase 2)
      └── GlobalAveragePooling2D
      └── Dense(256) + BatchNorm + Dropout(0.4)
      └── Dense(128) + BatchNorm + Dropout(0.3)
      └── Dense(4, softmax)
```

---

## 🚀 Step-by-Step Setup

### STEP 1 — Train the Model

```bash
cd ml
pip install -r requirements.txt

# Place your dataset in ml/dataset/ with 4 subfolders:
# Bacterial_Blight/ Blast/ Brown_Spot/ Tungro/

python train.py
# → Saves model to ml/models/riceguard_efficientnetb0.h5
# → Saves plots to ml/results/
```

---

### STEP 2 — Run Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt

# Make sure ml/ is in your PYTHONPATH
export PYTHONPATH=../ml   # Linux/Mac
set PYTHONPATH=..\ml      # Windows

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API will be live at: http://localhost:8000
Swagger docs at:     http://localhost:8000/docs

---

### STEP 3 — Run Frontend (React)

```bash
cd frontend
npm install
npm start
# Opens at http://localhost:3000
```

---

### STEP 4 — Deploy with Docker (Production)

```bash
# From root riceguard/ directory
docker-compose up --build

# Frontend → http://localhost:3000
# Backend  → http://localhost:8000
# API Docs → http://localhost:8000/docs
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Model status |
| POST | `/api/predict` | Upload image → get diagnosis |
| GET | `/api/classes` | List all disease classes |

### POST /api/predict — Sample Response
```json
{
  "disease": "Blast",
  "disease_display": "Blast",
  "confidence": 94.7,
  "severity": "Moderate",
  "affected_area": 38.2,
  "all_probabilities": {
    "Bacterial Blight": 2.1,
    "Blast": 94.7,
    "Brown Spot": 1.8,
    "Tungro": 1.4
  },
  "advisory": {
    "disease": "Blast",
    "severity": "Moderate",
    "description": "...",
    "action": "...",
    "chemicals": ["..."],
    "cultural": ["..."]
  },
  "gradcam_overlay": "<base64 PNG string>"
}
```

---

## 🩺 Disease Coverage

| Disease | Pathogen | Severity Levels |
|---------|----------|----------------|
| Bacterial Blight | *Xanthomonas oryzae* | Mild / Moderate / Severe |
| Blast | *Magnaporthe oryzae* | Mild / Moderate / Severe |
| Brown Spot | *Bipolaris oryzae* | Mild / Moderate / Severe |
| Tungro | RTBV + RTSV (viral) | Mild / Moderate / Severe |

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `../ml/models/riceguard_efficientnetb0.h5` | Path to trained model |
| `REACT_APP_API_URL` | `http://localhost:8000` | Backend API URL |

---

*Built with ❤️ for RiceGuard AI — empowering farmers with AI-powered crop protection*
