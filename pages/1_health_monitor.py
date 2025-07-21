import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

MODEL_PATH = "anomaly.pkl"

# Normal ranges for basic health vitals
NORMAL_RANGES = {
    "heart_rate": (60, 100),           # bpm
    "spo2": (95, 100),                 # %
    "respiration_rate": (12, 20),      # breaths/min
    "temperature": (36.1, 37.2)        # °C
}

def check_abnormalities(data):
    abnormalities = []
    for vital, value in data.items():
        min_val, max_val = NORMAL_RANGES[vital]
        if value < min_val or value > max_val:
            abnormalities.append(f"**{vital.replace('_', ' ').title()}** is out of range: {value} (Normal: {min_val}-{max_val})")
    return abnormalities

def run():
    st.title("💓 Real-Time Health Monitor")
    st.write("Monitor your vital signs and detect any health anomalies instantly.")

    # User input
    st.subheader("📋 Enter your health vitals:")

    heart_rate = st.slider("Heart Rate (bpm)", 30, 180, 72)
    spo2 = st.slider("SpO2 (%)", 70, 100, 98)
    respiration_rate = st.slider("Respiration Rate (breaths/min)", 5, 40, 18)
    temperature = st.slider("Body Temperature (°C)", 34.0, 42.0, 36.7)

    input_data = pd.DataFrame([{
        "heart_rate": heart_rate,
        "spo2": spo2,
        "respiration_rate": respiration_rate,
        "temperature": temperature
    }])

    st.subheader("📊 Your Input:")
    st.dataframe(input_data)

    # Load anomaly detection model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        prediction = model.predict(input_data)[0]

        # Check for abnormal values even if model says it's OK
        abnormalities = check_abnormalities(input_data.iloc[0])

        st.subheader("🩺 AI Health Analysis:")

        if prediction == -1 or abnormalities:
            st.error("🚨 Anomaly detected!")
            if abnormalities:
                st.write("⚠️ **Vitals outside normal range:**")
                for issue in abnormalities:
                    st.markdown(f"- {issue}")
            else:
                st.write("⚠️ The AI model detected an abnormal pattern, even though all vitals are within normal ranges.")
            st.info("Please consult a medical professional.")
        else:
            st.success("✅ All vitals appear normal. Keep it up!")

    else:
        st.warning("⚠️ Anomaly detection model not found. Please retrain the model.")
