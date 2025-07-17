import streamlit as st
import pandas as pd
import numpy as np
from model import train_model

# GitHub CSV URL (raw file link)
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

st.set_page_config(page_title="AI-Powered Health Monitor", layout="centered")

st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# User input
st.header("📊 Enter Health Metrics")
heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)
spO2 = st.number_input("Blood Oxygen Level (%)", min_value=70, max_value=100, value=97)
temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

# Train model on deployment
model = train_model()

# Predict
data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
prediction = model.predict(data)[0]

if prediction == -1:
    st.error("⚠️ Anomaly Detected! Please consult a doctor.")
else:
    st.success("✅ All vitals appear normal.")

# Doctor contact form
st.header("📞 Reach Out to a Doctor")

with st.form("doctor_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Describe your issue or concern")

    submitted = st.form_submit_button("Send Request")
    if submitted:
        new_entry = pd.DataFrame([{
            "name": name,
            "email": email,
            "message": message
        }])

        try:
            existing = pd.read_csv(CSV_URL)
            updated = pd.concat([existing, new_entry], ignore_index=True)
        except Exception as e:
            st.warning(f"⚠️ Couldn't fetch remote CSV. Creating new file locally.\n{e}")
            updated = new_entry

        # Save locally
        updated.to_csv("doctor_requests.csv", index=False)
        st.success("✅ Your request has been saved!")

st.markdown("### 🧑‍⚕️ Available Doctors")
st.markdown("- **Tony Wabuko** — [tonywabuko@gmail.com](mailto:tonywabuko@gmail.com)")
st.markdown("- **Brian Sangura** — [sangura.bren@gmail.com](mailto:sangura.bren@gmail.com)")

