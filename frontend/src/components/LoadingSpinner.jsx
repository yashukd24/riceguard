import React from "react";

export default function LoadingSpinner() {
  const steps = [
    { icon: "📸", label: "Reading image..." },
    { icon: "🧠", label: "Running EfficientNetB0..." },
    { icon: "🔥", label: "Generating Grad-CAM..." },
    { icon: "💊", label: "Preparing advisory..." },
  ];

  return (
    <div className="loading-wrapper">
      <div className="spinner" />
      <h2 className="loading-title">Analyzing your rice leaf...</h2>
      <div className="loading-steps">
        {steps.map((s, i) => (
          <div key={i} className="loading-step">
            <span>{s.icon}</span>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
