# app.py

import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import altair as alt
from datetime import datetime

# Train the model on app startup
model = train_model()

st.title("🧠 AI-Powered Health Monitoring System")

st.write("Enter your real-time health metrics to check for anomalies:")

# Form input
heart_rate = st.number_input(
    "Heart Rate (bpm)", min_value=30, max_value=220, value=72)
spO2 = st.number_input("SpO2 (%)", min_value=50, max_value=100, value=98)
temperature = st.number_input(
    "Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.7)

# Detect anomaly
if st.button("🔍 Check Health Status"):
    input_data = pd.DataFrame([[heart_rate, spO2, temperature]],
                              columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(input_data)

    if prediction[0] == -1:
        st.error(
            "⚠️ Anomaly detected in your health metrics. Please consult a doctor.")
    else:
        st.success("✅ Your health metrics appear normal.")

# Doctor contact form
st.markdown("---")
st.header("📞 Reach Out to a Doctor")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    symptoms = st.text_area("Describe your symptoms")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        if name and email and symptoms:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame([{
                "timestamp": timestamp,
                "name": name,
                "email": email,
                "symptoms": symptoms
            }])

            try:
                existing = pd.read_csv("doctor_requests.csv")
                updated = pd.concat([existing, new_row], ignore_index=True)
            except FileNotFoundError:
                updated = new_row

            updated.to_csv("doctor_requests.csv", index=False)
            st.success(
                "✅ Your request has been submitted. A doctor will reach out soon.")
        else:
            st.error("❗ Please fill in all fields before submitting.")
