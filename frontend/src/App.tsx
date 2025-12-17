import React, { useState, useEffect } from 'react';
import './App.css';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import { apiService } from './services/api';
import { PredictionResult, ModelInfo } from './types';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const health = await apiService.checkHealth();
      if (health.status === 'ok') {
        setApiStatus('connected');
        if (health.model_loaded) {
          const info = await apiService.getModelInfo();
          setModelInfo(info);
        }
      } else {
        setApiStatus('disconnected');
      }
    } catch (err) {
      setApiStatus('disconnected');
      console.error('API connection error:', err);
    }
  };

  const handlePredict = async (features: Record<string, number>) => {
    setLoading(true);
    setError(null);
    
    try {
      const prediction = await apiService.predict(features);
      setResult(prediction);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🎓 Student Risk Prediction System</h1>
          <p>AI-powered early warning system for student retention</p>
          <div className={`api-status ${apiStatus}`}>
            <span className="status-dot"></span>
            {apiStatus === 'connected' ? 'API Connected' : 
             apiStatus === 'disconnected' ? 'API Disconnected' : 
             'Checking Connection...'}
          </div>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠️</span>
            <div>
              <strong>Error:</strong> {error}
            </div>
            <button onClick={() => setError(null)} className="close-btn">×</button>
          </div>
        )}

        {apiStatus === 'disconnected' && (
          <div className="warning-banner">
            <span className="warning-icon">⚠️</span>
            <div>
              <strong>API Connection Failed</strong>
              <p>Please ensure the backend API is running on http://localhost:8000</p>
              <button onClick={checkApiStatus} className="retry-btn">Retry Connection</button>
            </div>
          </div>
        )}

        {!result ? (
          <div className="form-container">
            <PredictionForm 
              onSubmit={handlePredict} 
              loading={loading}
              modelInfo={modelInfo}
            />
          </div>
        ) : (
          <div className="results-container">
            <ResultsDisplay result={result} onReset={handleReset} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 Student Risk Prediction System | Powered by Machine Learning & SHAP</p>
        {modelInfo && (
          <p className="model-info">
            Model: {modelInfo.model_type} | Features: {modelInfo.feature_count}
          </p>
        )}
      </footer>
    </div>
  );
}

export default App;
