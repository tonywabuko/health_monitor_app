import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import base64
from pathlib import Path
import os

# --- 1. Path Configuration ---
def get_file_path(filename):
    """Get absolute path to a file in assets folder"""
    return os.path.join(Path(__file__).parent, "assets", "images", filename)

# --- 2. Image Handling ---
def image_to_base64(img_path):
    """Convert image to base64 for HTML embedding"""
    try:
        img_bytes = Path(img_path).read_bytes()
        return base64.b64encode(img_bytes).decode()
    except:
        return ""

# --- 3. Asset Injection ---
def inject_assets():
    """Inject CSS, JS, and images into Streamlit app"""
    
    # Inject CSS
    css_path = os.path.join(Path(__file__).parent, "assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Inject JS
    js_path = os.path.join(Path(__file__).parent, "assets", "js", "script.js")
    if os.path.exists(js_path):
        with open(js_path) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
    
    # Load images
    st.session_state.images = {
        "logo": image_to_base64(get_file_path("logo.png")),
        "banner": image_to_base64(get_file_path("banner.jpg")),
        "doctor_icon": image_to_base64(get_file_path("doctor-icon.png"))
    }

# --- 4. HTML Templates ---
def render_html_template(template_name, **kwargs):
    """Render HTML templates with dynamic content"""
    templates = {
        "header": f"""
        <header class="app-header">
            <div class="logo-container">
                <img src="data:image/png;base64,{st.session_state.images['logo']}" alt="Logo">
                <h1>AI Health Monitor</h1>
            </div>
            <img src="data:image/jpg;base64,{st.session_state.images['banner']}" class="app-banner">
        </header>
        """,
        
        "profile_page": """
        <div class="card profile-card">
            <h2><i class="fas fa-user"></i> Patient Profile</h2>
            {content}
        </div>
        """,
        
        "monitor_page": """
        <div class="card monitor-card">
            <h2><i class="fas fa-heartbeat"></i> Health Monitoring</h2>
            {content}
        </div>
        """
    }
    return templates[template_name].format(**kwargs)

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

# --- 6. Page Content ---
def introduction_page():
    """Patient profile page"""
    st.markdown(render_html_template("header"), unsafe_allow_html=True)
    
    with st.container():
        # Profile Form
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
        
        # Display saved profile
        if "patient" in st.session_state:
            st.markdown(render_html_template(
                "profile_page",
                content=f"""
                <div class="profile-display">
                    <h3>Saved Profile</h3>
                    <p><strong>Name:</strong> {st.session_state.patient['name']}</p>
                    <p><strong>Age:</strong> {st.session_state.patient['age']}</p>
                    <p><strong>Gender:</strong> {st.session_state.patient['gender']}</p>
                    <p><strong>Weight:</strong> {st.session_state.patient['weight']} kg</p>
                </div>
                """
            ), unsafe_allow_html=True)

def health_monitor_page():
    """Health monitoring page"""
    st.markdown(render_html_template("header"), unsafe_allow_html=True)
    
    with st.container():
        # Vital Signs Input
        st.markdown(render_html_template(
            "monitor_page",
            content="""
            <div class="vitals-form">
                <h3>Enter Your Vital Signs</h3>
            </div>
            """
        ), unsafe_allow_html=True)
        
        with st.form("vitals_form"):
            cols = st.columns(3)
            with cols[0]:
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
            with cols[1]:
                spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97)
            with cols[2]:
                temp = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=36.6)
            
            if st.form_submit_button("Analyze Vitals"):
                # Analyze with ML model
                model = train_model()
                data = pd.DataFrame([[heart_rate, spO2, temp]], 
                                   columns=["heart_rate", "spO2", "temperature"])
                prediction = model.predict(data)[0]
                
                # Display results
                if prediction == -1:
                    st.error("⚠️ Anomaly detected! Please consult a doctor.")
                else:
                    st.success("✅ Vitals are normal")

# --- 7. Navigation ---
PAGES = {
    "Patient Profile": introduction_page,
    "Health Monitor": health_monitor_page
}

# Sidebar Navigation
st.sidebar.markdown(f"""
<div class="sidebar-header">
    <img src="data:image/png;base64,{st.session_state.images['logo']}" width="60">
    <h3>Navigation</h3>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", list(PAGES.keys()), label_visibility="collapsed")

# Doctor contact in sidebar
st.sidebar.markdown(f"""
<div class="sidebar-card">
    <h4><img src="data:image/png;base64,{st.session_state.images['doctor_icon']}" width="20"> Contact Doctor</h4>
    <p>Dr. Tony Wabuko<br>tonywabuko@gmail.com</p>
    <button class="emergency-btn" onclick="alert('Emergency contact initiated!')">
        <i class="fas fa-ambulance"></i> Emergency
    </button>
</div>
""", unsafe_allow_html=True)

# Display selected page
PAGES[page]()
