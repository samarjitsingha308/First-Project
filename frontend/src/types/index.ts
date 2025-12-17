export interface StudentFeatures {
  gpa: number;
  attendance_rate: number;
  failed_courses: number;
  credit_hours: number;
  library_visits: number;
  tutoring_sessions: number;
  office_hours_visits: number;
  club_participation: number;
  age: number;
  first_generation: number;
  financial_aid: number;
  work_hours_per_week: number;
  counseling_visits: number;
  health_center_visits: number;
  advisor_meetings: number;
  study_group_participation: number;
}

export interface PredictionResult {
  prediction: 'Dropout' | 'Retained';
  dropout_probability: number;
  risk_band: 'Low' | 'Medium' | 'High';
  top_risk_drivers?: Record<string, number>;
  all_shap_values?: Record<string, number>;
}

export interface ModelInfo {
  model_type: string;
  features: string[];
  feature_count: number;
  threshold: number;
  output: string[];
  has_explainer: boolean;
}

export interface HealthStatus {
  status: string;
  model_loaded: boolean;
  features_count: number;
}
