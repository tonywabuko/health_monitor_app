import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Define the path where the model will be saved
MODEL_PATH = "anomaly_detector.pkl"

# Extended training data to match all vital signs used in app.py
def generate_training_data(n=10000):
    np.random.seed(42)
    
    # Generate normal health data with realistic distributions
    data = {
        "heart_rate": np.random.normal(loc=72, scale=8, size=n),
        "spO2": np.random.normal(loc=98, scale=1.5, size=n),
        "temperature": np.random.normal(loc=36.8, scale=0.4, size=n),
        "resp_rate": np.random.normal(loc=16, scale=3, size=n),
        "blood_pressure_sys": np.random.normal(loc=115, scale=10, size=n),
        "blood_pressure_dia": np.random.normal(loc=75, scale=8, size=n)
    }
    
    # Add some natural correlations between vitals
    data["heart_rate"] = np.where(data["temperature"] > 37.2, 
                                 data["heart_rate"] + np.random.normal(5, 2, n),
                                 data["heart_rate"])
    
    return pd.DataFrame(data)

# Train and save the model
def train_model():
    print("🔄 Generating training data...")
    df = generate_training_data()
    
    print("🔧 Training Isolation Forest model...")
    model = IsolationForest(
        n_estimators=200,
        contamination=0.01,  # 1% anomaly rate
        random_state=42,
        verbose=1
    )
    model.fit(df)
    
    print("💾 Saving model...")
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model successfully trained and saved to {MODEL_PATH}")
    
    return model

# Load model (trains new one if not found)
def load_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training new model...")
        return train_model()
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}. Retraining...")
        return train_model()

# Health data validation function
def validate_health_data(data):
    required_keys = {
        'heart_rate', 'spO2', 'temperature',
        'resp_rate', 'blood_pressure_sys', 'blood_pressure_dia'
    }
    return all(key in data for key in required_keys)

# Prediction function
def detect_anomalies(health_data):
    if not validate_health_data(health_data):
        raise ValueError("Incomplete health data provided")
    
    model = load_model()
    df = pd.DataFrame([health_data])
    
    # Get prediction (-1 for anomaly, 1 for normal)
    prediction = model.predict(df)[0]
    
    # Get anomaly score (the lower, the more anomalous)
    score = model.decision_function(df)[0]
    
    return {
        'is_anomaly': prediction == -1,
        'anomaly_score': float(score),
        'confidence': float(1 - (1 / (1 + np.exp(-abs(score)))))  # sigmoid transform
    }

if __name__ == "__main__":
    print("=== Starting model training ===")
    model = train_model()
    print("\n=== Sample prediction ===")
    
    test_data = {
        'heart_rate': 72,
        'spO2': 98,
        'temperature': 36.8,
        'resp_rate': 16,
        'blood_pressure_sys': 120,
        'blood_pressure_dia': 80
    }
    
    result = detect_anomalies(test_data)
    print(f"Test Result: {result}")
