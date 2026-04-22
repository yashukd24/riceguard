import React, { useState } from "react";

export default function GradCAMPanel({ preview, overlay, affectedArea }) {
  const [view, setView] = useState("overlay");

  return (
    <div className="card gradcam-card">
      <div className="card-header">
        <span className="card-icon">🔥</span>
        <h3>Grad-CAM Visualization</h3>
      </div>
      <p className="gradcam-desc">
        Highlighted regions show where the AI detected disease activity.
      </p>

      <div className="gradcam-toggle">
        <button
          className={`toggle-btn ${view === "original" ? "active" : ""}`}
          onClick={() => setView("original")}
        >
          Original
        </button>
        <button
          className={`toggle-btn ${view === "overlay" ? "active" : ""}`}
          onClick={() => setView("overlay")}
        >
          Grad-CAM Overlay
        </button>
      </div>

      <div className="gradcam-image-wrap">
        {view === "original" ? (
          <img src={preview} alt="Original leaf" className="gradcam-img" />
        ) : (
          <img
            src={`data:image/png;base64,${overlay}`}
            alt="Grad-CAM overlay"
            className="gradcam-img"
          />
        )}
        <div className="gradcam-badge">
          🔥 {affectedArea}% affected area
        </div>
      </div>

      <div className="gradcam-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ background: "#ff0000" }} />
          <span>High activation (most affected)</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: "#ffff00" }} />
          <span>Medium activation</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: "#0000ff" }} />
          <span>Low activation (healthy area)</span>
        </div>
      </div>
    </div>
  );
}
