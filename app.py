import streamlit as st
import numpy as np
import joblib
import pandas as pd
import os

# Load the trained model
model = joblib.load("anomaly_model.pkl")

# Streamlit app config
st.set_page_config(
    page_title="AI-Powered Health Monitoring", layout="centered")
st.title("🩺 AI-Powered Health Monitoring System")

st.subheader("Enter Your Vital Signs")
heart_rate = st.number_input(
    "Heart Rate (bpm)", min_value=30, max_value=200, value=75)
spO2 = st.number_input("Oxygen Saturation (%)",
                       min_value=50, max_value=100, value=98)
temperature = st.number_input(
    "Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.7, step=0.1)

# Prediction
if st.button("Check Health Status"):
    input_data = np.array([[heart_rate, spO2, temperature]])
    prediction = model.predict(input_data)

    if prediction[0] == -1:
        st.error("⚠️ Anomaly Detected! Your health readings may be abnormal.")
    else:
        st.success("✅ Your vital signs appear to be within normal range.")

# Divider
st.markdown("---")

# Consultation Form
st.subheader("📞 Request a Doctor Consultation")
with st.form("consult_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    symptoms = st.text_area("Briefly Describe Your Symptoms")
    submit = st.form_submit_button("Submit Request")

    if submit:
        if name and email and symptoms:
            new_entry = {
                "Name": name,
                "Email": email,
                "Symptoms": symptoms,
                "Heart Rate": heart_rate,
                "SpO2": spO2,
                "Temperature": temperature
            }

            # Save to consultations.csv
            if os.path.exists("consultations.csv"):
                df = pd.read_csv("consultations.csv")
                df = pd.concat([df, pd.DataFrame([new_entry])],
                               ignore_index=True)
            else:
                df = pd.DataFrame([new_entry])

            df.to_csv("consultations.csv", index=False)
            st.success(
                "✅ Your request has been submitted. A doctor will reach out to you soon.")
        else:
            st.warning("⚠️ Please fill in all the fields before submitting.")
