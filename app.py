import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path
import os
import time

# --- 1. Model Loading with Error Handling ---
try:
    from model import load_model
except ImportError as e:
    st.error(f"Failed to import model: {str(e)}")
    # Fallback to direct path (for some deployment environments)
    try:
        from .model import load_model
    except:
        st.error("Could not load model.py in any way")
        raise

# --- 2. Performance Optimization ---
@st.cache_resource()
def load_cached_model():
    try:
        start_time = time.time()
        model = load_model()
        st.session_state.model_load_time = time.time() - start_time
        return model
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        raise

# --- 3. Path Configuration ---
def get_file_path(filename):
    try:
        return os.path.join(Path(__file__).parent, "assets", "images", filename)
    except Exception as e:
        st.error(f"Path error: {str(e)}")
        return filename  # fallback

# --- 4. Image Handling ---
@st.cache_data()
def image_to_base64(img_path):
    try:
        return base64.b64encode(Path(img_path).read_bytes()).decode()
    except Exception as e:
        st.warning(f"Image load warning: {str(e)}")
        return ""

# --- 5. Asset Injection ---
def inject_assets():
    try:
        # CSS
        css_path = os.path.join(Path(__file__).parent, "assets", "css", "style.css")
        if os.path.exists(css_path):
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
        # JS
        js_path = os.path.join(Path(__file__).parent, "assets", "js", "script.js")
        if os.path.exists(js_path):
            with open(js_path) as f:
                st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
        
        # Images
        st.session_state.images = {
            "logo": image_to_base64(get_file_path("logo.png")),
            "banner": image_to_base64(get_file_path("banner.jpg")),
            "doctor_icon": image_to_base64(get_file_path("doctor-icon.png"))
        }
    except Exception as e:
        st.error(f"Asset loading error: {str(e)}")

# --- 6. Page Config ---
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize app
if "images" not in st.session_state:
    inject_assets()

# --- 7. Doctor Data ---
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

# --- 8. Page Content ---
def introduction_page():
    try:
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
    except Exception as e:
        st.error(f"Profile page error: {str(e)}")

def health_monitor_page():
    try:
        st.markdown("""
        <div class="card">
            <h2><i class="fas fa-heartbeat"></i> Health Monitoring</h2>
        """, unsafe_allow_html=True)
        
        # Load model with error handling
        try:
            with st.spinner("Loading health analyzer..."):
                model = load_cached_model()
            
            if "model_load_time" in st.session_state:
                st.sidebar.text(f"Model loaded in {st.session_state.model_load_time:.2f}s")
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            return
        
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
                try:
                    data = pd.DataFrame([[heart_rate, spO2, temp]], 
                                     columns=["heart_rate", "spO2", "temperature"])
                    prediction = model.predict(data)[0]
                    
                    if prediction == -1:
                        st.error("⚠️ Anomaly detected in your vital signs!")
                    else:
                        st.success("✅ All vitals appear normal")
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
        
        # Doctor Contact Section
        st.markdown("""
        <div class="card" style="margin-top: 20px;">
            <h2><i class="fas fa-user-md"></i> Reach Out to Doctors</h2>
        """, unsafe_allow_html=True)
        
        for doctor in DOCTORS:
            st.markdown(f"""
            <div class="doctor-card">
                <h3>{doctor['name']}</h3>
                <p><i class="fas fa-stethoscope"></i> {doctor['specialty']}</p>
                <p><i class="fas fa-envelope"></i> {doctor['email']}</p>
                <p><i class="fas fa-phone"></i> {doctor['phone']}</p>
                <p><i class="fas fa-calendar-alt"></i> {doctor['availability']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Health page error: {str(e)}")

# --- 9. Navigation ---
PAGES = {
    "Patient Profile": introduction_page,
    "Health Monitor": health_monitor_page
}

try:
    current_page = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
        format_func=lambda x: f"📌 {x}" if x == "Patient Profile" else f"🩺 {x}"
    )
    PAGES[current_page]()
except Exception as e:
    st.error(f"Navigation error: {str(e)}")
