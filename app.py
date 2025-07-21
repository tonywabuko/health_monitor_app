import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

try:
    from model import load_model
except ImportError as e:
    st.error(f"Error importing model: {str(e)}")
    st.stop()

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
</style>
""", unsafe_allow_html=True)

# Header
st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# Health Metrics
st.header("📊 Health Metrics")
cols = st.columns(3)
with cols[0]:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75, 
                               help=f"Normal range: {NORMAL_RANGES['heart_rate'][0]}-{NORMAL_RANGES['heart_rate'][1]} bpm")
with cols[1]:
    spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97,
                          help=f"Normal range: {NORMAL_RANGES['spO2'][0]}-{NORMAL_RANGES['spO2'][1]}%")
with cols[2]:
    temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8, step=0.1,
                                help=f"Normal range: {NORMAL_RANGES['temperature'][0]}-{NORMAL_RANGES['temperature'][1]}°C",
                                format="%.1f")

# Load model and predict
try:
    model = load_model()
    data = pd.DataFrame([[heart_rate, spO2, temperature]], 
                       columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(data)[0]
    
    # Manual range checks
    hr_normal = NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1]
    spo2_normal = NORMAL_RANGES["spO2"][0] <= spO2 <= NORMAL_RANGES["spO2"][1]
    temp_normal = NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1]
    
    is_anomaly = prediction == -1 or not all([hr_normal, spo2_normal, temp_normal])

except Exception as e:
    st.error(f"Model error: {str(e)}")
    is_anomaly = not all([
        NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1],
        NORMAL_RANGES["spO2"][0] <= spO2 <= NORMAL_RANGES["spO2"][1],
        NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1]
    ])

# Display results
if is_anomaly:
    st.error("""
    ⚠️ Anomaly Detected! Please consult a doctor.
    
    ### Abnormal Values:
    """ + 
    (f"- ❌ Heart Rate: {heart_rate} bpm (Normal: 60-100)\n" if not hr_normal else "") +
    (f"- ❌ SpO2: {spO2}% (Normal: 95-100)\n" if not spo2_normal else "") +
    (f"- ❌ Temperature: {temperature:.1f}°C (Normal: 36.2-37.2)\n" if not temp_normal else ""))
else:
    st.success("""
    ✅ All vitals appear normal.
    
    ### Your Readings:
    - Heart rate: {heart_rate} bpm (Normal: 60-100)
    - SpO2: {spO2}% (Normal: 95-100)
    - Temperature: {temperature:.1f}°C (Normal: 36.2-37.2)
    """.format(heart_rate=heart_rate, spO2=spO2, temperature=temperature))

# Doctors Section
st.header("👨‍⚕️ Available Doctors")
with st.expander("View Doctors", expanded=True):
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Tony Wabuko</h4>
            <p>tonywabuko@gmail.com</p>
            <p>+254 700 000000</p>
            <p>General Practitioner</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div class="doctor-card">
            <h4>Dr. Brian Sangura</h4>
            <p>sangura.bren@gmail.com</p>
            <p>+254 700 000001</p>
            <p>ICU Specialist</p>
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
st.markdown("AI Health Monitor © 2023 | Version 1.0")
