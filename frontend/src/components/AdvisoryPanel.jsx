import React, { useState } from "react";

export default function AdvisoryPanel({ advisory, severityColor }) {
  const [tab, setTab] = useState("action");

  const tabs = [
    { key: "action",    label: "⚠️ Action",    icon: "⚠️" },
    { key: "chemicals", label: "💊 Chemicals", icon: "💊" },
    { key: "cultural",  label: "🌱 Cultural",  icon: "🌱" },
  ];

  return (
    <div className="card advisory-card">
      <div className="card-header">
        <span className="card-icon">📋</span>
        <h3>Treatment Advisory</h3>
        <span className="advisory-severity" style={{ color: severityColor }}>
          {advisory.severity} — {advisory.disease}
        </span>
      </div>

      <div className="advisory-desc">{advisory.description}</div>

      <div className="advisory-tabs">
        {tabs.map((t) => (
          <button
            key={t.key}
            className={`advisory-tab ${tab === t.key ? "active" : ""}`}
            style={tab === t.key ? { borderColor: severityColor, color: severityColor } : {}}
            onClick={() => setTab(t.key)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="advisory-content">
        {tab === "action" && (
          <div className="advisory-action">
            <p>{advisory.action}</p>
          </div>
        )}

        {tab === "chemicals" && (
          <ul className="advisory-list">
            {advisory.chemicals.map((c, i) => (
              <li key={i} className="advisory-list-item">
                <span className="list-dot" style={{ background: severityColor }} />
                {c}
              </li>
            ))}
          </ul>
        )}

        {tab === "cultural" && (
          <ul className="advisory-list">
            {advisory.cultural.map((c, i) => (
              <li key={i} className="advisory-list-item">
                <span className="list-dot" style={{ background: "#27ae60" }} />
                {c}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="advisory-disclaimer">
        ⚕️ Always consult a local agricultural extension officer before applying treatments.
      </div>
    </div>
  );
}
