import React from "react";

const DISEASE_ICONS = {
  "Bacterial Blight": "🦠",
  "Blast": "💨",
  "Brown Spot": "🟤",
  "Tungro": "🟡",
};

const SEVERITY_EMOJI = {
  Mild: "🟢",
  Moderate: "🟡",
  Severe: "🔴",
};

export default function DiagnosisCard({ result, severityColor }) {
  const icon = DISEASE_ICONS[result.disease_display] || "🌿";

  return (
    <div className="card diagnosis-card">
      <div className="card-header">
        <span className="card-icon">🔬</span>
        <h3>Disease Diagnosis</h3>
      </div>

      <div className="disease-result">
        <span className="disease-emoji">{icon}</span>
        <div>
          <div className="disease-name">{result.disease_display}</div>
          <div className="confidence-text">
            {result.confidence}% confidence
          </div>
        </div>
      </div>

      <div className="confidence-bar-wrap">
        <div
          className="confidence-bar-fill"
          style={{ width: `${result.confidence}%` }}
        />
      </div>

      <div className="severity-row" style={{ borderColor: severityColor }}>
        <div>
          <div className="severity-label">Severity Level</div>
          <div className="severity-value" style={{ color: severityColor }}>
            {SEVERITY_EMOJI[result.severity]} {result.severity}
          </div>
        </div>
        <div>
          <div className="severity-label">Affected Area</div>
          <div className="severity-value" style={{ color: severityColor }}>
            {result.affected_area}%
          </div>
        </div>
      </div>
    </div>
  );
}
