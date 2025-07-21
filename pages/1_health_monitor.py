import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest

MODEL_PATH = "anomaly_detector.pkl"

def generate_training_data(n=1000):
    np.random.seed(42)
    heart_rate = np.random.normal(loc=75, scale=5, size=n)
    spO2 = np.random.normal(loc=98, scale=1, size=n)
    temperature = np.random.normal(loc=36.8, scale=0.3, size=n)
    return pd.DataFrame({"heart_rate": heart_rate, "spO2": spO2, "temperature": temperature})

def train_model():
    df = generate_training_data()
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(df)
    joblib.dump(model, MODEL_PATH)

def load_model():
    if not os.path.exists(MODEL_PATH):
        train_model()
    return joblib.load(MODEL_PATH)

# Page content
st.title("📊 Health Monitor")

st.write("Enter your vitals:")
heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=180)
spO2 = st.number_input("SpO2 (%)", min_value=70, max_value=100)
temperature = st.number_input("Temperature (°C)", min_value=34.0, max_value=42.0)

if st.button("Analyze"):
    model = load_model()
    input_data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(input_data)

    if prediction[0] == -1:
        st.error("⚠️ Anomaly Detected! Please consult a doctor.")
    else:
        st.success("✅ Your vitals are within normal range.")
