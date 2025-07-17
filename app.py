import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import os
import random
from pathlib import Path
import base64

# --- Path Helpers ---
def file_path(relative_path):
    return os.path.join(Path(__file__).parent, relative_path)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

# --- Theme Injection ---
def inject_theme():
    # Load CSS
    css = """
    :root {
        --primary: #2b7a78;
        --secondary: #3aafa9;
        --danger: #e74c3c;
        --light: #feffff;
        --dark: #17252a;
    }
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #f5f7fa;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 15px;
    }
    .normal { background-color: var(--secondary); }
    .danger { background-color: var(--danger); }
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Load images
    try:
        logo = img_to_bytes(file_path("assets/images/logo.png"))
        banner = img_to_bytes(file_path("assets/images/banner.jpg"))
    except:
        logo = ""
        banner = ""

    # Inject HTML structure
    html = f"""
    <div class="sidebar">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo}" width="80">
            <h2>AI Health Monitor</h2>
        </div>
    </div>
    <img src="data:image/jpg;base64,{banner}" class="banner">
    """
    st.markdown(html, unsafe_allow_html=True)

# --- App Config ---
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide"
)

inject_theme()

# --- Constants ---
HR_MIN, HR_MAX = 60, 100
SPO2_MIN, SPO2_MAX = 95, 100
TEMP_MIN, TEMP_MAX = 36.2, 37.2

# --- Pages ---
def introduction_page():
    st.markdown("""
    <div class="card">
        <h1>🩺 Patient Profile</h1>
    """, unsafe_allow_html=True)

    with st.form("profile_form"):
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Full Name")
            age = st.number_input("Age", 1, 120)
        with cols[1]:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", 30, 200)
        
        medical_history = st.text_area("Medical History")
        
        if st.form_submit_button("Save Profile"):
            st.session_state.profile = {
                "name": name,
                "age": age,
                "gender": gender,
                "weight": weight,
                "history": medical_history
            }
            st.success("Profile saved!")

    if "profile" in st.session_state:
        st.json(st.session_state.profile)

    st.markdown("</div>", unsafe_allow_html=True)

def health_monitor_page():
    st.markdown("""
    <div class="card">
        <h1>📊 Health Monitoring</h1>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        heart_rate = st.number_input("Heart Rate (bpm)", 40, 200, 75)
    with cols[1]:
        spO2 = st.number_input("SpO2 (%)", 70, 100, 97)
    with cols[2]:
        temp = st.number_input("Temperature (°C)", 30.0, 42.0, 36.8)

    # Anomaly detection
    model = train_model()
    pred = model.predict([[heart_rate, spO2, temp]])[0]
    
    hr_abnormal = heart_rate < HR_MIN or heart_rate > HR_MAX
    spo2_abnormal = spO2 < SPO2_MIN
    temp_abnormal = temp < TEMP_MIN or temp > TEMP_MAX
    is_anomaly = pred == -1 or hr_abnormal or spo2_abnormal or temp_abnormal

    if is_anomaly:
        st.markdown("""
        <div class="metric-card danger">
            <h3>⚠️ Anomaly Detected!</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card normal">
            <h3>✅ Vitals Normal</h3>
        </div>
        """, unsafe_allow_html=True)

    # Doctor form
    with st.form("doctor_form"):
        st.text_input("Your Name")
        st.text_input("Your Email")
        st.text_area("Message")
        st.form_submit_button("Send Request")

    st.markdown("</div>", unsafe_allow_html=True)

# --- Navigation ---
PAGES = {
    "Profile": introduction_page,
    "Monitor": health_monitor_page
}

page = st.sidebar.radio("Navigation", list(PAGES.keys()))
PAGES[page]()
