import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import os

# ===== CSS Loading =====
def load_css():
    """Load CSS with multiple fallback methods"""
    # Try package-relative path first (for deployed apps)
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles.css')
    
    # Method 1: Try loading from file
    if os.path.exists(css_path):
        try:
            with open(css_path, encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            return
        except Exception as e:
            st.warning(f"CSS loading warning: {str(e)}")
    
    # Method 2: Embedded minimal CSS fallback
    st.markdown("""
    <style>
        /* Basic UI Enhancements */
        .stApp {
            background: #f0f2f6;
            font-family: Arial, sans-serif;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .vital-normal { color: #28a745; }
        .vital-warning { color: #ffc107; }
        .vital-danger { color: #dc3545; }
        .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize app
load_css()
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Rest of your existing app code...
# [Keep all your current functionality here]
# [Include the vital signs monitoring, prediction, and doctor contact form]

# GitHub CSV URL (raw file link)
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

st.set_page_config(page_title="AI-Powered Health Monitor", layout="centered")

st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# Constants for normal ranges
HR_MIN, HR_MAX = 60, 100
SPO2_MIN, SPO2_MAX = 95, 100
TEMP_MIN, TEMP_MAX = 36.2, 37.2

# User input
st.header("📊 Enter Health Metrics")
heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
spO2 = st.number_input("Blood Oxygen Level (%)", min_value=70, max_value=100, value=97)
temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

# Train model on deployment
model = train_model()

# Predict
data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
prediction = model.predict(data)[0]

# Enhanced detection with manual range checking
is_hr_abnormal = heart_rate < HR_MIN or heart_rate > HR_MAX
is_spo2_abnormal = spO2 < SPO2_MIN
is_temp_abnormal = temperature < TEMP_MIN or temperature > TEMP_MAX

# Combined detection (model prediction OR manual range check)
is_anomaly = prediction == -1 or is_hr_abnormal or is_spo2_abnormal or is_temp_abnormal

if is_anomaly:
    st.error(f"""
    ⚠️ Anomaly Detected! Please consult a doctor.
    
    ### Abnormal Values:
    {"- ❌ Heart Rate: " + str(heart_rate) + " bpm (Normal: 60-100)" if is_hr_abnormal else "- ✅ Heart Rate: Normal"}
    {"- ❌ SpO2: " + str(spO2) + "% (Normal: ≥95%)" if is_spo2_abnormal else "- ✅ SpO2: Normal"}
    {"- ❌ Temperature: " + str(temperature) + "°C (Normal: 36.2-37.2)" if is_temp_abnormal else "- ✅ Temperature: Normal"}
    """)
else:
    st.success(f"""
    ✅ All vitals appear normal.
    
    Your readings:
    - Heart rate: {heart_rate} bpm (normal: 60-100)
    - SpO2: {spO2}% (normal: 95-100)
    - Temperature: {temperature}°C (normal: 36.2-37.2)
    """)

# Simple historical data visualization using Streamlit native
st.header("📈 Health Trends")
try:
    trend_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Heart Rate': [72, 75, 71, 69, heart_rate],
        'SpO2': [98, 97, 99, 96, spO2],
        'Temperature': [36.7, 36.8, 37.0, 36.5, temperature]
    })
    
    st.line_chart(trend_data.set_index('Day'))
except Exception as e:
    st.warning(f"Couldn't display trends: {str(e)}")

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

        updated.to_csv("doctor_requests.csv", index=False)
        st.success("✅ Your request has been saved!")

st.markdown("### 🧑‍⚕️ Available Doctors")
st.markdown("- **Tony Wabuko** — [tonywabuko@gmail.com](mailto:tonywabuko@gmail.com)")
st.markdown("- **Brian Sangura** — [sangura.bren@gmail.com](mailto:sangura.bren@gmail.com)")

# Emergency instructions
with st.expander("🚨 Emergency Instructions"):
    st.warning("""
    If experiencing any of these symptoms:
    - Chest pain
    - Severe shortness of breath
    - Confusion or dizziness
    - Blue lips or face
    
    Call emergency services immediately!
    """)
