import React from "react";
import DiagnosisCard from "./DiagnosisCard";
import GradCAMPanel from "./GradCAMPanel";
import ProbabilityChart from "./ProbabilityChart";
import AdvisoryPanel from "./AdvisoryPanel";

export default function ResultSection({ result, preview, onReset }) {
  const severityColor = {
    Mild: "#27ae60",
    Moderate: "#e67e22",
    Severe: "#e74c3c",
  }[result.severity] || "#888";

  return (
    <div className="result-wrapper">

      {/* Top bar */}
      <div className="result-topbar">
        <div>
          <h2 className="result-title">🔬 Diagnosis Complete</h2>
          <p className="result-subtitle">EfficientNetB0 · Grad-CAM Analysis</p>
        </div>
        <button className="btn-reset" onClick={onReset}>
          ↩ Analyze Another
        </button>
      </div>

      {/* Main grid */}
      <div className="result-grid">

        {/* Left column */}
        <div className="result-left">
          <DiagnosisCard result={result} severityColor={severityColor} />
          <ProbabilityChart probs={result.all_probabilities} />
        </div>

        {/* Right column */}
        <div className="result-right">
          <GradCAMPanel
            preview={preview}
            overlay={result.gradcam_overlay}
            affectedArea={result.affected_area}
          />
        </div>
      </div>

      {/* Advisory — full width */}
      <AdvisoryPanel advisory={result.advisory} severityColor={severityColor} />

    </div>
  );
}
