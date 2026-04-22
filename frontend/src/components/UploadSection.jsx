import React, { useCallback, useState } from "react";

export default function UploadSection({ onUpload, error }) {
  const [dragging, setDragging] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) onUpload(file);
  }, [onUpload]);

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) onUpload(file);
  };

  return (
    <div className="upload-wrapper">
      <div className="hero-text">
        <h2>Diagnose Rice Leaf Diseases Instantly</h2>
        <p>Upload a rice leaf photo — our AI detects disease, estimates severity, and provides treatment advice.</p>
        <div className="disease-chips">
          {["Bacterial Blight", "Blast", "Brown Spot", "Tungro"].map((d) => (
            <span key={d} className="disease-chip">{d}</span>
          ))}
        </div>
      </div>

      <div
        className={`dropzone ${dragging ? "dragging" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById("fileInput").click()}
      >
        <div className="dropzone-icon">📸</div>
        <p className="dropzone-title">Drop your rice leaf image here</p>
        <p className="dropzone-subtitle">or click to browse</p>
        <p className="dropzone-hint">Supports JPG, PNG — Max 10MB</p>
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={handleFileInput}
        />
      </div>

      {error && (
        <div className="error-box">
          ⚠️ {error}
        </div>
      )}

      <div className="how-it-works">
        <h3>How it works</h3>
        <div className="steps">
          {[
            { icon: "📸", step: "1. Upload", desc: "Take or upload a clear rice leaf photo" },
            { icon: "🧠", step: "2. Analyze", desc: "EfficientNetB0 AI classifies the disease" },
            { icon: "🔥", step: "3. Grad-CAM", desc: "See exactly which leaf areas are affected" },
            { icon: "💊", step: "4. Advisory", desc: "Get treatment recommendations instantly" },
          ].map((s) => (
            <div key={s.step} className="step-card">
              <div className="step-icon">{s.icon}</div>
              <div className="step-title">{s.step}</div>
              <div className="step-desc">{s.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
