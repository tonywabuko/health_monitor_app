import streamlit as st
import pandas as pd
import numpy as np
from model import load_model  # Changed from train_model to load_model
import base64
from pathlib import Path
import os
import time

# --- 1. Performance Optimization ---
@st.cache_resource()  # Cache the model loading
def load_cached_model():
    start_time = time.time()
    model = load_model()
    st.session_state.model_load_time = time.time() - start_time
    return model

# --- 2. Path Configuration ---
def get_file_path(filename):
    return os.path.join(Path(__file__).parent, "assets", "images", filename)

# --- 3. Image Handling ---
@st.cache_data()  # Cache image loading
def image_to_base64(img_path):
    try:
        return base64.b64encode(Path(img_path).read_bytes()).decode()
    except:
        return ""

# --- 4. Asset Injection ---
def inject_assets():
    # Load CSS (cached)
    css_path = os.path.join(Path(__file__).parent, "assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Load JS (cached)
    js_path = os.path.join(Path(__file__).parent, "assets", "js", "script.js")
    if os.path.exists(js_path):
        with open(js_path) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    
    # Load images (cached)
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
        "phone": "+254 700 123456"
    },
    {
        "name": "Dr. Brian Sangura",
        "email": "sangura.bren@gmail.com",
        "specialty": "General Physician",
        "phone": "+254 700 654321"
    }
]

# --- 7. Page Content ---
def introduction_page():
    st.markdown(render_html_template("header"), unsafe_allow_html=True)
    # ... (rest of your introduction page code)

def health_monitor_page():
    st.markdown(render_html_template("header"), unsafe_allow_html=True)
    
    # Load model with progress indicator
    with st.spinner("Loading health analyzer..."):
        model = load_cached_model()
    
    if "model_load_time" in st.session_state:
        st.sidebar.text(f"Model loaded in {st.session_state.model_load_time:.2f}s")
    
    # ... (rest of your health monitoring page code)

# --- 8. Sidebar with Both Doctors ---
def show_sidebar():
    st.sidebar.markdown(f"""
    <div class="sidebar-header">
        <img src="data:image/png;base64,{st.session_state.images['logo']}" width="60">
        <h3>Navigation</h3>
    </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio("", list(PAGES.keys()), label_visibility="collapsed")

    # Doctor contacts
    st.sidebar.markdown("""
    <div class="sidebar-card">
        <h4><i class="fas fa-user-md"></i> Available Doctors</h4>
    """, unsafe_allow_html=True)
    
    for doctor in DOCTORS:
        st.sidebar.markdown(f"""
        <div class="doctor-profile">
            <h5>{doctor['name']}</h5>
            <p><i class="fas fa-envelope"></i> {doctor['email']}</p>
            <p><i class="fas fa-mobile-alt"></i> {doctor['phone']}</p>
            <p><i class="fas fa-stethoscope"></i> {doctor['specialty']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <button class="emergency-btn" onclick="alert('Emergency contact initiated!')">
            <i class="fas fa-ambulance"></i> Emergency Call
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    return page

# --- 9. Main App Flow ---
PAGES = {
    "Patient Profile": introduction_page,
    "Health Monitor": health_monitor_page
}

current_page = show_sidebar()
PAGES[current_page]()
