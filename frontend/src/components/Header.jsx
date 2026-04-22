import React from "react";

export default function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <span className="logo-icon">🌾</span>
          <div>
            <h1 className="logo-title">RiceGuard AI</h1>
            <p className="logo-subtitle">Rice Leaf Disease Diagnosis System</p>
          </div>
        </div>
        <div className="header-badges">
          <span className="badge badge-green">EfficientNetB0</span>
          <span className="badge badge-blue">Grad-CAM</span>
          <span className="badge badge-orange">4 Diseases</span>
        </div>
      </div>
    </header>
  );
}
