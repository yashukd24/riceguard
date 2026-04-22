import React, { useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ResultSection from "./components/ResultSection";
import LoadingSpinner from "./components/LoadingSpinner";
import "./index.css";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [preview, setPreview]   = useState(null);

  const handleImageUpload = async (file) => {
    setError(null);
    setResult(null);
    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Prediction failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
    setPreview(null);
  };

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        {!result && !loading && (
          <UploadSection onUpload={handleImageUpload} error={error} />
        )}
        {loading && <LoadingSpinner />}
        {result && (
          <ResultSection
            result={result}
            preview={preview}
            onReset={handleReset}
          />
        )}
      </main>
      <footer className="footer">
        <p>🌾 RiceGuard AI — Dayananda Sagar University | AIML Dept | 2024</p>
      </footer>
    </div>
  );
}

export default App;
