import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "anomaly_detector.pkl"

def generate_training_data(n=1000):
    np.random.seed(42)
    heart_rate = np.random.normal(loc=75, scale=5, size=n)
    spO2 = np.random.normal(loc=98, scale=1, size=n)
    temperature = np.random.normal(loc=36.8, scale=0.3, size=n)
    df = pd.DataFrame({
        "heart_rate": heart_rate,
        "spO2": spO2,
        "temperature": temperature
    })
    return df

def train_and_save_model():
    df = generate_training_data()
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(df)
    joblib.dump(model, MODEL_PATH)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)

if __name__ == "__main__":
    train_and_save_model()
