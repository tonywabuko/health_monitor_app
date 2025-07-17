# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Sample synthetic data
np.random.seed(42)
data = pd.DataFrame({
    "Heart Rate": np.random.normal(70, 10, 500),
    "SpO2": np.random.normal(98, 1, 500),
    "Temperature": np.random.normal(36.5, 0.5, 500),
})

# Train model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(data)

# Save model
joblib.dump(model, "anomaly_model.pkl")
print("✅ Model saved as anomaly_model.pkl")
