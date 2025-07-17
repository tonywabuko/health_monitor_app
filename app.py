import streamlit as st
import pandas as pd
import numpy as np
from model import load_model
from datetime import datetime
import os

# Constants
LOCAL_CSV = "doctor_requests.csv"
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2)
}

# Page Config
st.set_page_config(
    page_title="AI-Powered Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .doctor-card {
        background-color: #1e293b !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: white !important;
        border-left: 4px solid #6366f1;
    }
    .doctor-card h4 {
        color: #ffffff !important;
        margin-bottom: 12px;
    }
    .doctor-card p {
        color: #e2e8f0 !important;
        margin-bottom: 8px;
    }
    .doctor-card i {
        color: #818cf8 !important;
        margin-right: 8px;
        width: 20px;
        text-align: center;
    }
    .stForm {
        background-color: #1e293b !important;
        border-radius: 10px;
        padding: 1.5rem;
    }
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background-color: #334155 !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: #f8fafc !important;
    }
    .metric-card {
        background: #1e293b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights powered by AI.")

# Input: Health Metrics
st.header("📊 Health Metrics")
cols = st.columns(3)
with cols[0]:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75,
                                 help="Normal range: 60–100 bpm")
with cols[1]:
    spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97,
                           help="Normal range: 95–100%")
with cols[2]:
    temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8, step=0.1,
                                  help="Normal range: 36.2–37.2°C")

# AI-Based Anomaly Detection
model = load_model()
input_df = pd.DataFrame([{
    "heart_rate": heart_rate,
    "spO2": spO2,
    "temperature": temperature
}])
prediction = model.predict(input_df)[0]
is_anomaly = prediction == -1

# Output Feedback
if is_anomaly:
    st.error("⚠️ Anomaly Detected by AI Model")
    st.markdown("""
    One or more vital signs appear outside the expected pattern based on historical health data.
    Please consult a medical professional.
    """)
else:
    st.success("✅ Your vital signs appear normal based on the AI model.")

st.markdown(f"""
### 🔎 Your Input:
- Heart Rate: {heart_rate} bpm
- Blood Oxygen: {spO2}%
- Temperature: {temperature}°C
""")

# Doctors Section
st.header("👨‍⚕️ Available Doctors")
with st.expander("View Doctors", expanded=True):
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Wabuko</h4>
            <p><i class="fas fa-envelope"></i> tonywabuko@gmail.com</p>
            <p><i class="fas fa-phone"></i> +254 799104517</p>
            <p><i class="fas fa-user-md"></i> Cardiology Specialist</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Sangura</h4>
            <p><i class="fas fa-envelope"></i> sangura.bren@gmail.com</p>
            <p><i class="fas fa-phone"></i> +254 720638389</p>
            <p><i class="fas fa-procedures"></i> ICU Specialist</p>
        </div>
        """, unsafe_allow_html=True)

# Contact Form
st.header("📩 Contact a Doctor")
with st.form("doctor_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    submitted = st.form_submit_button("Send Request")

    if submitted:
        if not name or not email or not message:
            st.warning("⚠️ Please fill out all fields before submitting.")
        else:
            try:
                new_entry = pd.DataFrame([{
                    "name": name,
                    "email": email,
                    "message": message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])

                if os.path.exists(LOCAL_CSV):
                    existing = pd.read_csv(LOCAL_CSV)
                    updated = pd.concat([existing, new_entry], ignore_index=True)
                else:
                    updated = new_entry

                updated.to_csv(LOCAL_CSV, index=False)
                st.success("✅ Request submitted successfully!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Privacy & Footer
st.markdown("---")
st.markdown("AI Health Monitor © 2025 | Version 1.0")
st.markdown("<small>🔒 This tool is for educational use only. It does not replace professional medical advice.</small>", unsafe_allow_html=True)
