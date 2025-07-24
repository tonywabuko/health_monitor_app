import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "anomaly_detector.pkl"

def generate_training_data(n=1000):
    """Generate synthetic normal health data for training"""
    np.random.seed(42)
    data = {
        "heart_rate": np.random.normal(loc=75, scale=5, size=n),
        "spO2": np.random.normal(loc=98, scale=1, size=n),
        "temperature": np.random.normal(loc=36.8, scale=0.3, size=n)
    }
    return pd.DataFrame(data)

def train_and_save_model():
    """Train and persist the anomaly detection model"""
    df = generate_training_data()
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(df)
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    """Load the trained model or train if not exists"""
    if not os.path.exists(MODEL_PATH):
        return train_and_save_model()
    return joblib.load(MODEL_PATH)

def predict_anomalies(heart_rate, spO2, temperature):
    """Predict if health metrics are anomalous"""
    model = load_model()
    data = np.array([[heart_rate, spO2, temperature]])
    prediction = model.predict(data)
    anomaly_score = model.decision_function(data)
    return {
        "is_anomaly": prediction[0] == -1,
        "score": float(anomaly_score[0]),
        "message": "⚠️ Abnormal reading detected!" if prediction[0] == -1 else "✅ Normal reading"
    }

if __name__ == "__main__":
    print("Training anomaly detection model...")
    train_and_save_model()
    print("Model trained and saved successfully!")
