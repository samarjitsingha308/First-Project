import React, { useState } from 'react';
import './PredictionForm.css';
import { StudentFeatures, ModelInfo } from '../types';

interface Props {
  onSubmit: (features: Record<string, number>) => void;
  loading: boolean;
  modelInfo: ModelInfo | null;
}

const FEATURE_GROUPS = {
  'Academic Performance': [
    { name: 'gpa', label: 'GPA', min: 0, max: 4, step: 0.1, default: 3.0, unit: '' },
    { name: 'attendance_rate', label: 'Attendance Rate', min: 0, max: 1, step: 0.01, default: 0.85, unit: '%' },
    { name: 'failed_courses', label: 'Failed Courses', min: 0, max: 10, step: 1, default: 0, unit: '' },
    { name: 'credit_hours', label: 'Credit Hours', min: 3, max: 21, step: 1, default: 15, unit: 'hrs' },
  ],
  'Engagement': [
    { name: 'library_visits', label: 'Library Visits', min: 0, max: 50, step: 1, default: 8, unit: '/month' },
    { name: 'tutoring_sessions', label: 'Tutoring Sessions', min: 0, max: 20, step: 1, default: 3, unit: '/semester' },
    { name: 'office_hours_visits', label: 'Office Hours Visits', min: 0, max: 20, step: 1, default: 2, unit: '/semester' },
    { name: 'club_participation', label: 'Club Participation', min: 0, max: 5, step: 1, default: 1, unit: 'clubs' },
  ],
  'Demographics & Background': [
    { name: 'age', label: 'Age', min: 17, max: 30, step: 1, default: 20, unit: 'years' },
    { name: 'first_generation', label: 'First Generation', min: 0, max: 1, step: 1, default: 0, unit: '' },
    { name: 'financial_aid', label: 'Financial Aid', min: 0, max: 1, step: 1, default: 0, unit: '' },
    { name: 'work_hours_per_week', label: 'Work Hours/Week', min: 0, max: 40, step: 1, default: 10, unit: 'hrs' },
  ],
  'Support Services': [
    { name: 'counseling_visits', label: 'Counseling Visits', min: 0, max: 20, step: 1, default: 1, unit: '/semester' },
    { name: 'health_center_visits', label: 'Health Center Visits', min: 0, max: 20, step: 1, default: 2, unit: '/semester' },
    { name: 'advisor_meetings', label: 'Advisor Meetings', min: 0, max: 20, step: 1, default: 2, unit: '/semester' },
    { name: 'study_group_participation', label: 'Study Group Participation', min: 0, max: 1, step: 1, default: 0, unit: '' },
  ],
};

const PredictionForm: React.FC<Props> = ({ onSubmit, loading, modelInfo }) => {
  const [features, setFeatures] = useState<Record<string, number>>(() => {
    const initial: Record<string, number> = {};
    Object.values(FEATURE_GROUPS).flat().forEach(field => {
      initial[field.name] = field.default;
    });
    return initial;
  });

  const handleChange = (name: string, value: number) => {
    setFeatures(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(features);
  };

  const handleReset = () => {
    const initial: Record<string, number> = {};
    Object.values(FEATURE_GROUPS).flat().forEach(field => {
      initial[field.name] = field.default;
    });
    setFeatures(initial);
  };

  const loadSampleData = (type: 'high-risk' | 'low-risk') => {
    if (type === 'high-risk') {
      setFeatures({
        gpa: 2.0,
        attendance_rate: 0.65,
        failed_courses: 3,
        credit_hours: 12,
        library_visits: 2,
        tutoring_sessions: 0,
        office_hours_visits: 0,
        club_participation: 0,
        age: 22,
        first_generation: 1,
        financial_aid: 1,
        work_hours_per_week: 30,
        counseling_visits: 0,
        health_center_visits: 1,
        advisor_meetings: 1,
        study_group_participation: 0,
      });
    } else {
      setFeatures({
        gpa: 3.7,
        attendance_rate: 0.95,
        failed_courses: 0,
        credit_hours: 16,
        library_visits: 15,
        tutoring_sessions: 5,
        office_hours_visits: 4,
        club_participation: 2,
        age: 19,
        first_generation: 0,
        financial_aid: 0,
        work_hours_per_week: 10,
        counseling_visits: 2,
        health_center_visits: 1,
        advisor_meetings: 3,
        study_group_participation: 1,
      });
    }
  };

  const formatValue = (name: string, value: number) => {
    const field = Object.values(FEATURE_GROUPS).flat().find(f => f.name === name);
    if (!field) return value;
    
    if (name === 'attendance_rate') {
      return `${(value * 100).toFixed(0)}%`;
    }
    if (name === 'gpa') {
      return value.toFixed(2);
    }
    if (name === 'first_generation' || name === 'financial_aid' || name === 'study_group_participation') {
      return value === 1 ? 'Yes' : 'No';
    }
    return value.toString();
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Student Information</h2>
        <p>Enter student details to predict dropout risk</p>
        <div className="sample-buttons">
          <button type="button" onClick={() => loadSampleData('high-risk')} className="sample-btn high">
            Load High-Risk Sample
          </button>
          <button type="button" onClick={() => loadSampleData('low-risk')} className="sample-btn low">
            Load Low-Risk Sample
          </button>
          <button type="button" onClick={handleReset} className="sample-btn reset">
            Reset to Default
          </button>
        </div>
      </div>

      {Object.entries(FEATURE_GROUPS).map(([groupName, fields]) => (
        <div key={groupName} className="feature-group">
          <h3 className="group-title">{groupName}</h3>
          <div className="feature-grid">
            {fields.map(field => (
              <div key={field.name} className="form-field">
                <label htmlFor={field.name}>
                  <span className="label-text">{field.label}</span>
                  <span className="label-value">{formatValue(field.name, features[field.name])}</span>
                </label>
                <input
                  type="range"
                  id={field.name}
                  name={field.name}
                  min={field.min}
                  max={field.max}
                  step={field.step}
                  value={features[field.name]}
                  onChange={(e) => handleChange(field.name, parseFloat(e.target.value))}
                  className="slider"
                />
                <div className="slider-labels">
                  <span>{field.min}{field.unit}</span>
                  <span>{field.max}{field.unit}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      <div className="form-actions">
        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing...
            </>
          ) : (
            <>
              🎯 Predict Risk
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;
