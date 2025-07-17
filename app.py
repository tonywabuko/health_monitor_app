import streamlit as st
import pandas as pd
import numpy as np
from model import load_model
import base64
from pathlib import Path
import os
import time

# --- 1. Performance Optimization ---
@st.cache_resource()
def load_cached_model():
    start_time = time.time()
    model = load_model()
    st.session_state.model_load_time = time.time() - start_time
    return model

# --- 2. Path Configuration ---
def get_file_path(filename):
    return os.path.join(Path(__file__).parent, "assets", "images", filename)

# --- 3. Image Handling ---
@st.cache_data()
def image_to_base64(img_path):
    try:
        return base64.b64encode(Path(img_path).read_bytes()).decode()
    except:
        return ""

# --- 4. Asset Injection ---
def inject_assets():
    css_path = os.path.join(Path(__file__).parent, "assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    js_path = os.path.join(Path(__file__).parent, "assets", "js", "script.js")
    if os.path.exists(js_path):
        with open(js_path) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    
    st.session_state.images = {
        "logo": image_to_base64(get_file_path("logo.png")),
        "banner": image_to_base64(get_file_path("banner.jpg")),
        "doctor_icon": image_to_base64(get_file_path("doctor-icon.png"))
    }

# --- 5. Page Config ---
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize app
if "images" not in st.session_state:
    inject_assets()

# --- 6. Doctor Data ---
DOCTORS = [
    {
        "name": "Dr. Tony Wabuko",
        "email": "tonywabuko@gmail.com",
        "specialty": "Cardiologist",
        "phone": "+254 700 123456",
        "availability": "Mon-Fri: 9AM-5PM"
    },
    {
        "name": "Dr. Brian Sangura",
        "email": "sangura.bren@gmail.com",
        "specialty": "General Physician",
        "phone": "+254 700 654321",
        "availability": "Mon-Sat: 8AM-6PM"
    }
]

# --- 7. Page Content ---
def introduction_page():
    st.markdown("""
    <div class="card">
        <h2><i class="fas fa-user"></i> Patient Profile</h2>
    """, unsafe_allow_html=True)
    
    with st.form("patient_profile"):
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
        with cols[1]:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        
        medical_history = st.text_area("Medical History")
        
        if st.form_submit_button("Save Profile"):
            st.session_state.patient = {
                "name": name, "age": age,
                "gender": gender, "weight": weight,
                "history": medical_history
            }
            st.success("Profile saved successfully!")
    
    st.markdown("</div>", unsafe_allow_html=True)

def health_monitor_page():
    st.markdown("""
    <div class="card">
        <h2><i class="fas fa-heartbeat"></i> Health Monitoring</h2>
    """, unsafe_allow_html=True)
    
    # Load model
    with st.spinner("Loading health analyzer..."):
        model = load_cached_model()
    
    # Vital Signs Input
    with st.form("vitals_form"):
        cols = st.columns(3)
        with cols[0]:
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
        with cols[1]:
            spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97)
        with cols[2]:
            temp = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=36.6)
        
        submitted = st.form_submit_button("Analyze Vitals")
        
        if submitted:
            # Analysis code here
            st.success("Analysis complete!")
    
    # Doctor Contact Section
    st.markdown("""
    <div class="card" style="margin-top: 20px;">
        <h2><i class="fas fa-user-md"></i> Reach Out to Doctors</h2>
    """, unsafe_allow_html=True)
    
    for doctor in DOCTORS:
        st.markdown(f"""
        <div class="doctor-card">
            <h3>{doctor['name']}</h3>
            <p><i class="fas fa-stethoscope"></i> <strong>Specialty:</strong> {doctor['specialty']}</p>
            <p><i class="fas fa-envelope"></i> <strong>Email:</strong> {doctor['email']}</p>
            <p><i class="fas fa-phone"></i> <strong>Phone:</strong> {doctor['phone']}</p>
            <p><i class="fas fa-calendar-alt"></i> <strong>Availability:</strong> {doctor['availability']}</p>
            <button class="contact-btn" onclick="window.location.href='mailto:{doctor['email']}'">
                <i class="fas fa-paper-plane"></i> Contact
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. Navigation ---
PAGES = {
    "Patient Profile": introduction_page,
    "Health Monitor": health_monitor_page
}

current_page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    format_func=lambda x: f"📌 {x}" if x == "Patient Profile" else f"🩺 {x}"
)

PAGES[current_page]()
