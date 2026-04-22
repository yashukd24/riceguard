import React from "react";

const COLORS = {
  "Bacterial Blight": "#e74c3c",
  "Blast": "#e67e22",
  "Brown Spot": "#8B4513",
  "Tungro": "#f1c40f",
};

export default function ProbabilityChart({ probs }) {
  const entries = Object.entries(probs).sort((a, b) => b[1] - a[1]);

  return (
    <div className="card prob-card">
      <div className="card-header">
        <span className="card-icon">📊</span>
        <h3>Class Probabilities</h3>
      </div>
      <div className="prob-list">
        {entries.map(([disease, prob]) => (
          <div key={disease} className="prob-row">
            <div className="prob-label">{disease}</div>
            <div className="prob-bar-wrap">
              <div
                className="prob-bar-fill"
                style={{
                  width: `${prob}%`,
                  backgroundColor: COLORS[disease] || "#3498db",
                }}
              />
            </div>
            <div className="prob-value">{prob}%</div>
          </div>
        ))}
      </div>
    </div>
  );
}
