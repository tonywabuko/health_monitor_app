import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = "anomaly.pkl"

def generate_training_data(n=1000):
    np.random.seed(42)
    data = pd.DataFrame({
        "heart_rate": np.random.normal(75, 5, n),
        "spo2": np.random.normal(98, 1, n),
        "respiration_rate": np.random.normal(16, 2, n),
        "temperature": np.random.normal(36.8, 0.3, n)
    })
    return data

def train_and_save_model():
    data = generate_training_data()
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(data)
    joblib.dump(model, MODEL_PATH)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)

if __name__ == "__main__":
    train_and_save_model()

