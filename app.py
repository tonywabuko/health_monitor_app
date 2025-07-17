import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import base64
from datetime import datetime
import os

# --- Constants ---
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2)
}

# --- Page Config ---
st.set_page_config(
    page_title="AI-Powered Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
def load_css():
    st.markdown("""
    <style>
        /* Main container */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Cards */
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Animated alerts */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        .alert-pulse {
            animation: pulse 2s infinite;
        }
        
        /* Improved form inputs */
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stTextArea>div>div>textarea {
            border-radius: 8px !important;
            padding: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# --- Header Section ---
st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("""
<div style="margin-bottom: 2rem;">
    <p style="font-size: 1.1rem;">Monitor your vital signs in real-time and get personalized health insights.</p>
</div>
""", unsafe_allow_html=True)

# --- Health Metrics Section ---
with st.container():
    st.header("📊 Health Metrics Dashboard")
    
    cols = st.columns(3)
    with cols[0]:
        heart_rate = st.number_input(
            "❤️ Heart Rate (bpm)", 
            min_value=40, 
            max_value=200, 
            value=75,
            help="Normal range: 60-100 bpm"
        )
    with cols[1]:
        spO2 = st.number_input(
            "🫁 Blood Oxygen (%)", 
            min_value=70, 
            max_value=100, 
            value=97,
            help="Normal range: 95-100%"
        )
    with cols[2]:
        temperature = st.number_input(
            "🌡️ Temperature (°C)", 
            min_value=30.0, 
            max_value=42.0, 
            value=36.8,
            help="Normal range: 36.2-37.2°C",
            step=0.1
        )

# --- Analysis Section ---
try:
    model = train_model()
    data = pd.DataFrame([[heart_rate, spO2, temperature]], 
                       columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(data)[0]
    
    # Manual range checks as backup
    hr_normal = NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1]
    spo2_normal = spO2 >= NORMAL_RANGES["spO2"][0]
    temp_normal = NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1]
    
    is_anomaly = prediction == -1 or not all([hr_normal, spo2_normal, temp_normal])
    
    if is_anomaly:
        with st.container():
            st.markdown("""
            <div class="metric-card alert-pulse" style="border-left: 4px solid #ff4b4b;">
                <h3 style="color: #ff4b4b;">⚠️ Anomaly Detected</h3>
                <p>Please consult a healthcare professional.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.table(pd.DataFrame({
                "Metric": ["Heart Rate", "Blood Oxygen", "Temperature"],
                "Your Value": [f"{heart_rate} bpm", f"{spO2}%", f"{temperature}°C"],
                "Normal Range": ["60-100 bpm", "≥95%", "36.2-37.2°C"],
                "Status": [
                    "❌ Abnormal" if not hr_normal else "✅ Normal",
                    "❌ Abnormal" if not spo2_normal else "✅ Normal",
                    "❌ Abnormal" if not temp_normal else "✅ Normal"
                ]
            }))
    else:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="border-left: 4px solid #4CAF50;">
                <h3 style="color: #4CAF50;">✅ All Vitals Normal</h3>
                <p>Your readings are within healthy ranges.</p>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Error in analysis: {str(e)}")
    st.warning("Using basic range checks instead")
    
    # Fallback to simple range checks
    if not all([hr_normal, spo2_normal, temp_normal]):
        st.error("Some values are outside normal ranges")

# --- Doctor Contact Section ---
with st.container():
    st.header("📞 Contact a Doctor")
    
    with st.expander("🧑‍⚕️ Available Doctors", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Tony Wabuko</h4>
                <p><i class="fas fa-envelope"></i> tonywabuko@gmail.com</p>
                <p><i class="fas fa-phone"></i> +254 700 000000</p>
                <p><i class="fas fa-stethoscope"></i> Cardiology Specialist</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Brian Sangura</h4>
                <p><i class="fas fa-envelope"></i> sangura.bren@gmail.com</p>
                <p><i class="fas fa-phone"></i> +254 700 000001</p>
                <p><i class="fas fa-user-md"></i> General Practitioner</p>
            </div>
            """, unsafe_allow_html=True)
    
    with st.form("doctor_form"):
        st.subheader("Send Consultation Request")
        name = st.text_input("Your Full Name")
        email = st.text_input("Email Address")
        urgency = st.selectbox("Urgency Level", ["Routine", "Urgent", "Emergency"])
        message = st.text_area("Describe your symptoms or concerns")
        
        submitted = st.form_submit_button("📤 Send Request")
        if submitted:
            if not all([name, email, message]):
                st.warning("Please fill all required fields")
            else:
                try:
                    new_entry = pd.DataFrame([{
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "name": name,
                        "email": email,
                        "urgency": urgency,
                        "message": message
                    }])
                    
                    try:
                        existing = pd.read_csv(CSV_URL)
                        updated = pd.concat([existing, new_entry], ignore_index=True)
                    except:
                        updated = new_entry
                    
                    updated.to_csv("doctor_requests.csv", index=False)
                    st.success("✅ Your request has been submitted!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Error saving request: {str(e)}")

# --- Emergency Section ---
with st.container():
    st.markdown("""
    <div class="metric-card" style="background-color: #fff8f8; border-left: 4px solid #ff4b4b;">
        <h3><i class="fas fa-ambulance"></i> Emergency Assistance</h3>
        <p>For immediate medical attention:</p>
        <button style="background-color: #ff4b4b; color: white; border: none; padding: 10px 15px; border-radius: 5px; margin-top: 10px;">
            <i class="fas fa-phone"></i> Call Emergency Services
        </button>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;">
    <p>AI Health Monitor v1.0 • Last updated {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)
