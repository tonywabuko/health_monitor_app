import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from model import load_model

MODEL_PATH = "anomaly.pkl"

NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spo2": (95, 100),
    "respiration_rate": (12, 20),
    "temperature": (36.1, 37.2)
}

def check_abnormalities(data):
    issues = []
    for key, val in data.items():
        min_val, max_val = NORMAL_RANGES[key]
        if val < min_val or val > max_val:
            issues.append(f"**{key.replace('_', ' ').title()}** = {val} (Normal: {min_val}-{max_val})")
    return issues

def run():
    st.title("💓 Real-Time Health Monitor")
    st.write("Enter your vitals to check for anomalies.")

    # Input sliders
    heart_rate = st.slider("Heart Rate (bpm)", 30, 180, 72)
    spo2 = st.slider("SpO2 (%)", 70, 100, 98)
    respiration_rate = st.slider("Respiration Rate (breaths/min)", 5, 40, 18)
    temperature = st.slider("Body Temperature (°C)", 34.0, 42.0, 36.7)

    data = pd.DataFrame([{
        "heart_rate": heart_rate,
        "spo2": spo2,
        "respiration_rate": respiration_rate,
        "temperature": temperature
    }])

    st.subheader("📊 Your Input:")
    st.dataframe(data)

    if os.path.exists(MODEL_PATH):
        model = load_model()
        prediction = model.predict(data)[0]
        abnormalities = check_abnormalities(data.iloc[0])

        st.subheader("🩺 AI Health Analysis:")
        if prediction == -1 or abnormalities:
            st.error("🚨 Anomaly Detected!")
            if abnormalities:
                st.markdown("⚠️ **Abnormal Readings:**")
                for issue in abnormalities:
                    st.markdown(f"- {issue}")
            else:
                st.info("⚠️ AI model flagged this as anomalous, even though all vitals are normal.")
        else:
            st.success("✅ All vitals appear normal.")
    else:
        st.warning("⚠️ No model found. Please retrain the model.")
