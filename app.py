import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import IsolationForest
from datetime import datetime

# === Train model if not already saved ===


def train_model():
    data = {
        "heart_rate": [72, 75, 71, 69, 180, 65, 85, 77, 66, 160],
        "spO2": [98, 97, 99, 96, 90, 99, 97, 95, 98, 88],
        "temperature": [36.7, 36.8, 37.0, 36.5, 39.2, 36.9, 37.1, 36.6, 36.8, 38.5]
    }

    df = pd.DataFrame(data)
    X = df[["heart_rate", "spO2", "temperature"]]

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)

    joblib.dump(model, "anomaly_model.pkl")
    print("✅ Model trained and saved as anomaly_model.pkl")

# === Check if model exists; if not, train ===


if not os.path.exists("anomaly_model.pkl"):
    train_model()

# === Load the trained model ===

model = joblib.load("anomaly_model.pkl")

# === Streamlit UI ===

st.title("🧠 AI-Powered Health Monitoring System")
st.write("Enter patient health data to detect potential anomalies.")

heart_rate = st.number_input(
    "Heart Rate (bpm)", min_value=30, max_value=200, value=75)
spO2 = st.number_input("Oxygen Saturation (%)",
                       min_value=70, max_value=100, value=98)
temperature = st.number_input(
    "Temperature (°C)", min_value=30.0, max_value=45.0, value=36.8)

if st.button("Check for Anomaly"):
    input_data = np.array([[heart_rate, spO2, temperature]])
    result = model.predict(input_data)

    if result[0] == -1:
        st.error("🚨 Anomaly detected! Vitals appear abnormal.")

        st.subheader("📞 Request a Doctor Consultation")
        name = st.text_input("Your Name")
        contact = st.text_input("Phone or Email")

        if st.button("Submit Request"):
            if name and contact:
                request_data = {
                    "name": name,
                    "contact": contact,
                    "heart_rate": heart_rate,
                    "spO2": spO2,
                    "temperature": temperature,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Save to CSV
                file_path = "doctor_requests.csv"
                df = pd.DataFrame([request_data])

                if os.path.exists(file_path):
                    df.to_csv(file_path, mode='a', header=False, index=False)
                else:
                    df.to_csv(file_path, index=False)

                st.success("✅ Your request has been submitted to a doctor.")
            else:
                st.warning("Please fill in your name and contact information.")
    else:
        st.success("✅ Vitals are within the normal range. No anomaly detected.")
