import React from 'react';
import './ResultsDisplay.css';
import { PredictionResult } from '../types';

interface Props {
  result: PredictionResult;
  onReset: () => void;
}

const ResultsDisplay: React.FC<Props> = ({ result, onReset }) => {
  const getRiskColor = (band: string) => {
    switch (band) {
      case 'Low':
        return '#48bb78';
      case 'Medium':
        return '#ed8936';
      case 'High':
        return '#f56565';
      default:
        return '#718096';
    }
  };

  const getRiskIcon = (band: string) => {
    switch (band) {
      case 'Low':
        return '✅';
      case 'Medium':
        return '⚠️';
      case 'High':
        return '🚨';
      default:
        return '❓';
    }
  };

  const getRiskMessage = (band: string) => {
    switch (band) {
      case 'Low':
        return 'Student is performing well with minimal dropout risk.';
      case 'Medium':
        return 'Student shows some warning signs. Early intervention recommended.';
      case 'High':
        return 'Student is at high risk. Immediate intervention required.';
      default:
        return '';
    }
  };

  const getRecommendations = (band: string, drivers?: Record<string, number>) => {
    const recommendations: string[] = [];
    
    if (band === 'High' || band === 'Medium') {
      if (drivers) {
        const driverKeys = Object.keys(drivers);
        
        if (driverKeys.some(k => k.includes('gpa') || k.includes('failed'))) {
          recommendations.push('Schedule academic tutoring sessions');
          recommendations.push('Connect with academic advisor for course planning');
        }
        
        if (driverKeys.some(k => k.includes('attendance'))) {
          recommendations.push('Monitor attendance closely');
          recommendations.push('Reach out to understand barriers to attendance');
        }
        
        if (driverKeys.some(k => k.includes('work_hours'))) {
          recommendations.push('Discuss work-study balance');
          recommendations.push('Explore financial aid options');
        }
        
        if (driverKeys.some(k => k.includes('library') || k.includes('tutoring'))) {
          recommendations.push('Encourage use of campus resources');
          recommendations.push('Promote study skills workshops');
        }
      }
      
      if (recommendations.length === 0) {
        recommendations.push('Schedule meeting with academic advisor');
        recommendations.push('Connect with student support services');
        recommendations.push('Monitor progress weekly');
      }
    } else {
      recommendations.push('Continue current support level');
      recommendations.push('Periodic check-ins recommended');
      recommendations.push('Encourage continued engagement');
    }
    
    return recommendations;
  };

  const sortedDrivers = result.top_risk_drivers
    ? Object.entries(result.top_risk_drivers).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
    : [];

  const formatFeatureName = (name: string) => {
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const getDriverImpact = (value: number) => {
    if (value > 0) return 'increasing';
    if (value < 0) return 'decreasing';
    return 'neutral';
  };

  return (
    <div className="results-display">
      <div className="results-header">
        <button onClick={onReset} className="back-btn">
          ← Back to Form
        </button>
        <h2>Prediction Results</h2>
      </div>

      <div className="results-grid">
        {/* Main Prediction Card */}
        <div className="result-card main-result" style={{ borderColor: getRiskColor(result.risk_band) }}>
          <div className="card-icon" style={{ background: getRiskColor(result.risk_band) }}>
            {getRiskIcon(result.risk_band)}
          </div>
          <h3>Risk Assessment</h3>
          <div className="risk-band" style={{ color: getRiskColor(result.risk_band) }}>
            {result.risk_band} Risk
          </div>
          <div className="probability">
            <span className="probability-label">Dropout Probability</span>
            <div className="probability-bar-container">
              <div 
                className="probability-bar" 
                style={{ 
                  width: `${result.dropout_probability * 100}%`,
                  background: getRiskColor(result.risk_band)
                }}
              />
            </div>
            <span className="probability-value">{(result.dropout_probability * 100).toFixed(1)}%</span>
          </div>
          <div className="prediction-outcome">
            <strong>Prediction:</strong> {result.prediction}
          </div>
          <p className="risk-message">{getRiskMessage(result.risk_band)}</p>
        </div>

        {/* Risk Drivers Card */}
        {sortedDrivers.length > 0 && (
          <div className="result-card drivers-card">
            <h3>🎯 Top Risk Drivers (SHAP Values)</h3>
            <p className="drivers-explanation">
              These factors have the strongest influence on the prediction:
            </p>
            <div className="drivers-list">
              {sortedDrivers.map(([feature, value], index) => {
                const impact = getDriverImpact(value);
                const absValue = Math.abs(value);
                const maxAbs = Math.max(...sortedDrivers.map(([, v]) => Math.abs(v)));
                const barWidth = (absValue / maxAbs) * 100;
                
                return (
                  <div key={feature} className="driver-item">
                    <div className="driver-header">
                      <span className="driver-rank">#{index + 1}</span>
                      <span className="driver-name">{formatFeatureName(feature)}</span>
                      <span className={`driver-impact ${impact}`}>
                        {value > 0 ? '↑' : '↓'} {impact}
                      </span>
                    </div>
                    <div className="driver-bar-container">
                      <div 
                        className={`driver-bar ${impact}`}
                        style={{ width: `${barWidth}%` }}
                      />
                    </div>
                    <span className="driver-value">{value.toFixed(4)}</span>
                  </div>
                );
              })}
            </div>
            <div className="shap-legend">
              <div className="legend-item">
                <span className="legend-color increasing"></span>
                <span>Increases dropout risk</span>
              </div>
              <div className="legend-item">
                <span className="legend-color decreasing"></span>
                <span>Decreases dropout risk</span>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations Card */}
        <div className="result-card recommendations-card">
          <h3>💡 Recommended Actions</h3>
          <div className="recommendations-list">
            {getRecommendations(result.risk_band, result.top_risk_drivers).map((rec, index) => (
              <div key={index} className="recommendation-item">
                <span className="rec-number">{index + 1}</span>
                <span className="rec-text">{rec}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Additional Info Card */}
        <div className="result-card info-card">
          <h3>ℹ️ Understanding the Results</h3>
          <div className="info-content">
            <div className="info-section">
              <h4>Risk Bands</h4>
              <ul>
                <li><strong>Low (0-30%):</strong> Minimal intervention needed</li>
                <li><strong>Medium (30-60%):</strong> Monitor and support recommended</li>
                <li><strong>High (60-100%):</strong> Immediate intervention required</li>
              </ul>
            </div>
            <div className="info-section">
              <h4>SHAP Values</h4>
              <p>
                SHAP (SHapley Additive exPlanations) values show how much each feature 
                contributes to the prediction. Positive values increase dropout risk, 
                while negative values decrease it.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
