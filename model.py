# model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Sample training data (replace with real sensor data or load from CSV)
data = {
    "heart_rate": [72, 75, 71, 69, 180, 65, 85, 77, 66, 160],
    "spO2": [98, 97, 99, 96, 90, 99, 97, 95, 98, 88],
    "temperature": [36.7, 36.8, 37.0, 36.5, 39.2, 36.9, 37.1, 36.6, 36.8, 38.5]
}

# Create DataFrame
df = pd.DataFrame(data)

# Select features for model training
X = df[["heart_rate", "spO2", "temperature"]]

# Train Isolation Forest model
model = IsolationForest(contamination=0.2, random_state=42)
model.fit(X)

# Save the trained model to a file
joblib.dump(model, "anomaly_model.pkl")

print("✅ Model trained and saved as anomaly_model.pkl using 3 features")
