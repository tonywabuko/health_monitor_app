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
        # Vital Signs Section
        st.markdown("### 📊 Enter Your Vital Signs", help="Provide your current health metrics")
        
        with st.form("vitals_form"):
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
                temp = st.number_input(
                    "🌡️ Temperature (°C)", 
                    min_value=35.0, 
                    max_value=42.0, 
                    value=36.6,
                    help="Normal range: 36.2-37.2°C"
                )
            
            submitted = st.form_submit_button(
                "Analyze Vitals",
                help="Get instant analysis of your health metrics"
            )
            
            if submitted:
                # Analyze with ML model
                model = train_model()
                data = pd.DataFrame([[heart_rate, spO2, temp]], 
                                   columns=["heart_rate", "spO2", "temperature"])
                prediction = model.predict(data)[0]
                
                # Manual range checks
                hr_abnormal = heart_rate < 60 or heart_rate > 100
                spo2_abnormal = spO2 < 95
                temp_abnormal = temp < 36.2 or temp > 37.2
                
                # Results container
                with st.container():
                    st.markdown("## 📝 Analysis Results")
                    
                    if prediction == -1 or hr_abnormal or spo2_abnormal or temp_abnormal:
                        st.error("""
                        ⚠️ **Anomaly Detected**  
                        We've detected unusual readings in your vital signs:
                        """)
                        
                        # Detailed anomaly report
                        anomaly_details = []
                        if hr_abnormal:
                            status = "HIGH" if heart_rate > 100 else "LOW"
                            anomaly_details.append(f"- ❤️ Heart Rate: {heart_rate} bpm ({status})")
                        if spo2_abnormal:
                            anomaly_details.append(f"- 🫁 Blood Oxygen: {spO2}% (LOW)")
                        if temp_abnormal:
                            status = "HIGH" if temp > 37.2 else "LOW"
                            anomaly_details.append(f"- 🌡️ Temperature: {temp}°C ({status})")
                        
                        st.markdown("\n".join(anomaly_details))
                        
                        st.warning("""
                        ### Recommended Actions:
                        - Rest and retake measurements
                        - Drink water if dehydrated
                        - Contact a doctor if symptoms persist
                        """)
                        
                        # Show emergency contacts
                        with st.expander("🆘 Immediate Assistance"):
                            st.markdown("""
                            **Available Doctors:**
                            - Dr. Tony Wabuko: tonywabuko@gmail.com (Cardiologist)
                            - Dr. Brian Sangura: sangura.bren@gmail.com (General Physician)
                            
                            **Emergency Services:**
                            - 🚑 Call 911 (US) or 112 (EU) for life-threatening conditions
                            """)
                    else:
                        st.success("""
                        ✅ **Vitals Normal**  
                        Your readings are within healthy ranges.
                        """)
                    
                    # Display ranges
                    st.markdown("""
                    ### Normal Ranges:
                    - ❤️ Heart Rate: 60-100 bpm
                    - 🫁 SpO2: 95-100%
                    - 🌡️ Temperature: 36.2-37.2°C
                    """)

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
    <h4><img src="data:image/png;base64,{st.session_state.images['doctor_icon']}" width="20"> Contact Doctors</h4>
    <p><strong>Dr. Tony Wabuko</strong><br>tonywabuko@gmail.com<br>(Cardiologist)</p>
    <p><strong>Dr. Brian Sangura</strong><br>sangura.bren@gmail.com<br>(General Physician)</p>
    <button class="emergency-btn" onclick="alert('Connecting to emergency services...')">
        <i class="fas fa-ambulance"></i> Emergency Call
    </button>
</div>
""", unsafe_allow_html=True)

# Display selected page
PAGES[page]()
