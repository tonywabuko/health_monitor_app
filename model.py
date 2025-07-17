import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "health_model.pkl"

def train_model():
    """Train and save the anomaly detection model"""
    data = {
        "heart_rate": [72, 75, 71, 69, 180, 65, 85, 77, 66, 160, 62, 110, 58, 130],
        "spO2": [98, 97, 99, 96, 90, 99, 97, 95, 98, 88, 99, 92, 100, 85],
        "temperature": [36.7, 36.8, 37.0, 36.5, 39.2, 36.9, 37.1, 36.6, 36.8, 38.5, 36.4, 37.5, 36.3, 38.0]
    }

    model = Pipeline([
        ('scaler', StandardScaler()),
        ('iso_forest', IsolationForest(contamination=0.2, random_state=42))
    ])
    
    trained_model = model.fit(pd.DataFrame(data))
    joblib.dump(trained_model, MODEL_PATH)
    return trained_model

def load_model():
    """Load the trained model or train if not found"""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_model()
