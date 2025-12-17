"""
Train Student Risk Prediction Model
Generates synthetic data, trains model, and saves bundle with SHAP explainer
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import shap
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_student_data(n_samples=1000):
    """Generate synthetic student data for training"""
    print(f"Generating {n_samples} synthetic student records...")
    
    data = {
        # Academic Performance
        'gpa': np.random.normal(2.8, 0.6, n_samples).clip(0, 4.0),
        'attendance_rate': np.random.normal(0.82, 0.15, n_samples).clip(0, 1),
        'failed_courses': np.random.poisson(1.2, n_samples).clip(0, 10),
        'credit_hours': np.random.normal(14, 3, n_samples).clip(3, 21),
        
        # Engagement
        'library_visits': np.random.poisson(8, n_samples),
        'tutoring_sessions': np.random.poisson(3, n_samples),
        'office_hours_visits': np.random.poisson(2, n_samples),
        'club_participation': np.random.binomial(3, 0.4, n_samples),
        
        # Demographics & Background
        'age': np.random.normal(20, 2, n_samples).clip(17, 30),
        'first_generation': np.random.binomial(1, 0.35, n_samples),
        'financial_aid': np.random.binomial(1, 0.55, n_samples),
        'work_hours_per_week': np.random.normal(15, 10, n_samples).clip(0, 40),
        
        # Health & Wellness
        'counseling_visits': np.random.poisson(1, n_samples),
        'health_center_visits': np.random.poisson(2, n_samples),
        
        # Academic Support
        'advisor_meetings': np.random.poisson(2, n_samples),
        'study_group_participation': np.random.binomial(1, 0.45, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable based on features (with some randomness)
    risk_score = (
        -df['gpa'] * 0.3 +
        -df['attendance_rate'] * 0.25 +
        df['failed_courses'] * 0.2 +
        -df['library_visits'] * 0.02 +
        -df['tutoring_sessions'] * 0.03 +
        df['work_hours_per_week'] * 0.01 +
        df['first_generation'] * 0.1 +
        -df['advisor_meetings'] * 0.05 +
        np.random.normal(0, 0.3, n_samples)  # Add noise
    )
    
    # Convert to binary (0: Retained, 1: Dropout)
    threshold = np.percentile(risk_score, 70)  # 30% dropout rate
    df['dropout'] = (risk_score > threshold).astype(int)
    
    print(f"Dataset created: {len(df)} samples")
    print(f"Dropout rate: {df['dropout'].mean():.2%}")
    print(f"\nFeature statistics:")
    print(df.describe())
    
    return df


def train_model(df):
    """Train Random Forest model with SHAP explainer"""
    print("\n" + "="*50)
    print("Training Student Risk Prediction Model")
    print("="*50)
    
    # Separate features and target
    X = df.drop('dropout', axis=1)
    y = df['dropout']
    
    features = X.columns.tolist()
    print(f"\nFeatures ({len(features)}): {features}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    print("✓ Model trained successfully")
    
    # Evaluate model
    print("\n" + "="*50)
    print("Model Evaluation")
    print("="*50)
    
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Retained', 'Dropout']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"TN: {cm[0,0]}, FP: {cm[0,1]}")
    print(f"FN: {cm[1,0]}, TP: {cm[1,1]}")
    
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"\nROC AUC Score: {auc:.4f}")
    
    # Feature importance
    print("\nTop 10 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.head(10).to_string(index=False))
    
    # Create SHAP explainer
    print("\nCreating SHAP explainer...")
    try:
        # Use a subset for SHAP to speed up computation
        background = shap.sample(X_train_scaled, 100)
        explainer = shap.KernelExplainer(model.predict_proba, background)
        print("✓ SHAP explainer created successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not create SHAP explainer: {e}")
        explainer = None
    
    # Save model bundle
    print("\nSaving model bundle...")
    bundle = {
        "model": model,
        "scaler": scaler,
        "explainer": explainer,
        "features": features,
        "model_version": "1.0",
        "metrics": {
            "auc": float(auc),
            "test_samples": len(X_test)
        }
    }
    
    return bundle, feature_importance


def main():
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate data
    df = generate_student_data(n_samples=1000)
    
    # Save dataset
    data_path = os.path.join(data_dir, "student_data.csv")
    df.to_csv(data_path, index=False)
    print(f"\n✓ Dataset saved to: {data_path}")
    
    # Train model
    bundle, feature_importance = train_model(df)
    
    # Save model
    model_path = os.path.join(models_dir, "model.pkl")
    joblib.dump(bundle, model_path)
    print(f"✓ Model bundle saved to: {model_path}")
    
    # Save feature importance
    importance_path = os.path.join(models_dir, "feature_importance.csv")
    feature_importance.to_csv(importance_path, index=False)
    print(f"✓ Feature importance saved to: {importance_path}")
    
    print("\n" + "="*50)
    print("✓ Model training completed successfully!")
    print("="*50)
    print(f"\nModel is ready to use. Start the API with:")
    print("  cd backend && uvicorn main:app --reload")


if __name__ == "__main__":
    main()
