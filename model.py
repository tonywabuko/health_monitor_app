import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "anomaly_model.pkl"


def train_model(df):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(df[['heart_rate', 'blood_oxygen']])
    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained and saved.")


def detect_anomalies(df, model):
    df = df.copy()
    df['anomaly'] = model.predict(df[['heart_rate', 'blood_oxygen']])
    df['anomaly'] = df['anomaly'].apply(
        lambda x: 'Anomaly' if x == -1 else 'Normal')
    return df


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError("Model not found. Train the model first.")
