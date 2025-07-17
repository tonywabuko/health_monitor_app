import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from model import train_model
from api_integration import WearableAPI  # New import

# GitHub CSV URL (raw file link)
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

st.set_page_config(page_title="AI-Powered Health Monitor", layout="centered")

# Sidebar for wearable integration
st.sidebar.header("Wearable Device Integration")
wearable_token = st.sidebar.text_input("Enter Wearable API Token", type="password")

# Initialize session state for historical data
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = pd.DataFrame()

# Fetch wearable data if token provided
if wearable_token:
    try:
        wearable = WearableAPI(wearable_token)
        hr_data = wearable.get_heart_rate()
        
        if 'activities-heart' in hr_data:
            st.sidebar.success("✅ Connected to wearable device")
            # Store historical data in session state
            st.session_state.historical_data = pd.DataFrame(
                hr_data['activities-heart'][0]['heart-rate-zones']
            )
    except Exception as e:
        st.sidebar.error(f"⚠️ Connection failed: {str(e)}")

# Main app content
st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# User input section with two columns
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Enter Health Metrics")
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
    spO2 = st.number_input("Blood Oxygen Level (%)", min_value=70, max_value=100, value=97)
    temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

with col2:
    if not st.session_state.historical_data.empty:
        st.header("📈 Your Heart Rate Zones")
        fig = px.bar(
            st.session_state.historical_data,
            x='name',
            y='minutes',
            color='name',
            title='Weekly Heart Rate Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)

# Train model and predict
model = train_model()
data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
prediction = model.predict(data)[0]

# Enhanced results display
if prediction == -1:
    st.error(f"""
    ⚠️ Anomaly Detected! Please consult a doctor.
    
    ### Your Readings vs Normal Ranges:
    | Metric          | Your Value   | Normal Range  | Status       |
    |----------------|-------------|--------------|-------------|
    | Heart Rate     | {heart_rate} bpm | 60-100 bpm   | ❌ Abnormal |
    | SpO2           | {spO2}%       | 95-100%      | {'❌ Abnormal' if spO2 < 95 else '✅ Normal'} |
    | Temperature    | {temperature}°C | 36.2-37.2°C  | {'❌ Abnormal' if temperature < 36.2 or temperature > 37.2 else '✅ Normal'} |
    """)
else:
    st.success(f"""
    ✅ All vitals appear normal.
    
    ### Your Readings:
    | Metric          | Your Value   | Normal Range  |
    |----------------|-------------|--------------|
    | Heart Rate     | {heart_rate} bpm | 60-100 bpm   |
    | SpO2           | {spO2}%       | 95-100%      |
    | Temperature    | {temperature}°C | 36.2-37.2°C  |
    """)

# Doctor contact form (unchanged)
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

        updated.to_csv("doctor_requests.csv", index=False)
        st.success("✅ Your request has been saved!")

# Enhanced doctors display
st.markdown("### 🧑‍⚕️ Available Doctors")
doctor_cols = st.columns(2)
with doctor_cols[0]:
    st.markdown("""
    **Dr. Tony Wabuko**  
    📧 [tonywabuko@gmail.com](mailto:tonywabuko@gmail.com)  
    📞 +254 700 000000  
    🏥 Cardiology Specialist
    """)
with doctor_cols[1]:
    st.markdown("""
    **Dr. Brian Sangura**  
    📧 [sangura.bren@gmail.com](mailto:sangura.bren@gmail.com)  
    📞 +254 700 000001  
    🏥 General Practitioner
    """)

# Add emergency contact button
if st.button("🚨 Emergency Contact"):
    st.warning("""
    For immediate medical assistance:
    - Call emergency services: 911 (or your local emergency number)
    - Nearest hospital: Nairobi Hospital (+254 20 2846000)
    """)
