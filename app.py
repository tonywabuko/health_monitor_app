# app.py
import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
from datetime import datetime

# Train the model at runtime
model = train_model()

st.set_page_config(page_title="AI Health Monitor", layout="centered")

st.title("🩺 AI-Powered Health Monitoring System")

st.markdown("Enter your health vitals to check for anomalies and get personalized feedback.")

# User input
heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)
spO2 = st.number_input("SpO₂ (%)", min_value=70, max_value=100, value=98)
temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0, value=36.8)

if st.button("Check Health"):
    input_data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(input_data)

    if prediction[0] == -1:
        st.error("⚠️ Anomaly detected! Your vitals may be abnormal.")
        st.markdown("Please consider reaching out to a healthcare professional.")
    else:
        st.success("✅ Your vitals are within a normal range.")

st.markdown("---")
st.subheader("📞 Request a Doctor Consultation")

with st.form("doctor_request_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    symptoms = st.text_area("Describe your symptoms")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        request = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "email": email,
            "symptoms": symptoms
        }

        try:
            df = pd.read_csv("doctor_requests.csv")
        except FileNotFoundError:
            df = pd.DataFrame(columns=["timestamp", "name", "email", "symptoms"])

        df = df.append(request, ignore_index=True)
        df.to_csv("doctor_requests.csv", index=False)

        st.success("✅ Your request has been sent. A doctor will contact you soon.")

st.markdown("---")
st.caption("Built by Tony Wabuko, Brian Sangura and John Kuria • 2025")
