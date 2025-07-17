import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
from datetime import datetime

# Constants
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"
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

# Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Dark Cards for Doctors */
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
    
    /* Dark Form */
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
    
    /* General Improvements */
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
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# Health Metrics
st.header("📊 Health Metrics")
cols = st.columns(3)
with cols[0]:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=80)
with cols[1]:
    spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97)
with cols[2]:
    temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

# Analysis
try:
    model = train_model()
    data = pd.DataFrame([[heart_rate, spO2, temperature]], 
                       columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(data)[0]
    
    is_anomaly = prediction == -1
    if is_anomaly:
        st.error("⚠️ Anomaly Detected! Please consult a doctor.")
    else:
        st.success("✅ All vitals appear normal.")
except:
    st.warning("⚠️ Model analysis unavailable - showing basic range checks")
    is_anomaly = not (NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1] and
                     spO2 >= NORMAL_RANGES["spO2"][0] and
                     NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1])

# Doctors Section
st.header("👨‍⚕️ Available Doctors")
with st.expander("View Doctors", expanded=True):
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Tony Wabuko</h4>
            <p><i class="fas fa-envelope"></i> tonywabuko@gmail.com</p>
            <p><i class="fas fa-phone"></i> +254 799104517</p>
            <p><i class="fas fa-stethoscope"></i> Cardiology Specialist</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Brian Sangura</h4>
            <p><i class="fas fa-envelope"></i> sangura.bren@gmail.com</p>
            <p><i class="fas fa-phone"></i> +254 720638389</p>
            <p><i class="fas fa-user-md"></i> General Practitioner</p>
        </div>
        """, unsafe_allow_html=True)

# Contact Form
with st.form("doctor_form"):
    st.subheader("📩 Contact a Doctor")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    
    submitted = st.form_submit_button("Send Request")
    if submitted:
        try:
            new_entry = pd.DataFrame([{
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            
            try:
                existing = pd.read_csv(CSV_URL)
                updated = pd.concat([existing, new_entry], ignore_index=True)
            except:
                updated = new_entry
            
            updated.to_csv("doctor_requests.csv", index=False)
            st.success("✅ Request submitted successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("AI Health Monitor © 2025 | Version 1.0")
