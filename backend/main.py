"""
API-only service for Student Risk Prediction
Extended for Advising Dashboard & Alert Engine
Assumes a pre-trained model bundle exists at models/model.pkl
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import joblib
import numpy as np
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")

# Load model bundle at startup
try:
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    scaler = bundle["scaler"]
    explainer = bundle.get("explainer")
    features = bundle["features"]
    print(f"✓ Model loaded successfully with {len(features)} features")
except Exception as e:
    print(f"⚠ Warning: Failed to load model bundle: {e}")
    print("The API will start but predictions will not work until a model is trained.")
    model = None
    scaler = None
    explainer = None
    features = []

app = FastAPI(title="Student Risk Prediction API", version="2.0")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Schemas
# -------------------------------

class StudentFeatures(BaseModel):
    data: Dict[str, float] = Field(..., description="Feature-name to value mapping")

class ThresholdConfig(BaseModel):
    low: float = 0.3
    medium: float = 0.6


# -------------------------------
# Utility functions
# -------------------------------

def check_model_loaded():
    """Check if model is loaded, raise error if not"""
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please train the model first using train_model.py"
        )

def score_student(feature_dict: Dict[str, float]):
    check_model_loaded()
    try:
        X = np.array([feature_dict[f] for f in features]).reshape(1, -1)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing feature: {e}")

    X_scaled = scaler.transform(X)
    probability = model.predict_proba(X_scaled)[0][1]
    return X_scaled, probability


def risk_band(probability: float, thresholds: ThresholdConfig):
    if probability >= thresholds.medium:
        return "High"
    elif probability >= thresholds.low:
        return "Medium"
    return "Low"


# -------------------------------
# Core Endpoints
# -------------------------------

@app.get("/")
def root():
    return {
        "message": "Student Risk Prediction API",
        "version": "2.0",
        "model_loaded": model is not None,
        "endpoints": [
            "/health",
            "/predict",
            "/model/info",
            "/risk/band",
            "/explanations/top-drivers",
            "/batch/predict",
            "/metrics",
            "/version"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "features_count": len(features) if features else 0
    }


@app.post("/predict")
def predict_risk(payload: StudentFeatures):
    X_scaled, probability = score_student(payload.data)

    prediction = "Dropout" if probability >= 0.5 else "Retained"

    response = {
        "prediction": prediction,
        "dropout_probability": round(float(probability), 4),
        "risk_band": risk_band(probability, ThresholdConfig())
    }

    if explainer:
        try:
            shap_values = explainer.shap_values(X_scaled)
            # Handle both binary and multiclass SHAP output
            if isinstance(shap_values, list):
                shap_values = shap_values[1][0]  # Get positive class
            else:
                shap_values = shap_values[0]
            
            response["top_risk_drivers"] = dict(
                sorted(
                    zip(features, shap_values.tolist()),
                    key=lambda x: abs(x[1]),
                    reverse=True
                )[:5]
            )
            
            # Add all SHAP values for detailed visualization
            response["all_shap_values"] = dict(zip(features, shap_values.tolist()))
        except Exception as e:
            print(f"SHAP calculation error: {e}")
            response["shap_error"] = str(e)

    return response


@app.get("/model/info")
def model_info():
    check_model_loaded()
    return {
        "model_type": type(model).__name__,
        "features": features,
        "feature_count": len(features),
        "threshold": 0.5,
        "output": ["Low", "Medium", "High"],
        "has_explainer": explainer is not None
    }


# -------------------------------
# Advising Dashboard Extensions
# -------------------------------

@app.post("/risk/band")
def get_risk_band(payload: StudentFeatures, thresholds: ThresholdConfig = ThresholdConfig()):
    _, probability = score_student(payload.data)
    band = risk_band(probability, thresholds)

    return {
        "risk_band": band,
        "dropout_probability": round(float(probability), 4)
    }


@app.post("/explanations/top-drivers")
def top_risk_drivers(payload: StudentFeatures):
    X_scaled, _ = score_student(payload.data)

    if not explainer:
        raise HTTPException(status_code=400, detail="SHAP explainer not available")

    try:
        shap_values = explainer.shap_values(X_scaled)
        # Handle both binary and multiclass SHAP output
        if isinstance(shap_values, list):
            shap_values = shap_values[1][0]  # Get positive class
        else:
            shap_values = shap_values[0]
        
        return {
            "top_drivers": dict(
                sorted(
                    zip(features, shap_values.tolist()),
                    key=lambda x: abs(x[1]),
                    reverse=True
                )[:5]
            ),
            "all_drivers": dict(zip(features, shap_values.tolist()))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SHAP calculation error: {str(e)}")


# -------------------------------
# Alert Engine / Batch Scoring
# -------------------------------

@app.post("/batch/predict")
def batch_predict(file: UploadFile = File(...)):
    check_model_loaded()
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    missing = set(features) - set(df.columns)
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing columns: {missing}")

    X = df[features].values
    X_scaled = scaler.transform(X)
    probs = model.predict_proba(X_scaled)[:, 1]

    results = []
    for idx, p in enumerate(probs):
        results.append({
            "row": idx,
            "dropout_probability": round(float(p), 4),
            "risk_band": risk_band(p, ThresholdConfig())
        })

    return {
        "count": len(results),
        "results": results
    }


# -------------------------------
# Governance & Metrics
# -------------------------------

@app.get("/metrics")
def metrics():
    return {
        "metrics_available": [
            "AUC",
            "Precision",
            "Recall",
            "F1"
        ],
        "note": "Computed offline during training"
    }


@app.get("/version")
def version():
    return {
        "api_version": "2.0",
        "model_version": bundle.get("model_version", "1.0") if model else "not loaded"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
