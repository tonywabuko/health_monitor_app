import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import os
import random
from pathlib import Path
import base64

# ===== 1. File Path Helpers =====
def file_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

# ===== 2. Custom Theme Injection =====
def inject_custom_theme():
    # Read CSS file
    css_path = file_path("assets/css/style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    # Read JS file
    js_path = file_path("assets/js/script.js")
    if os.path.exists(js_path):
        with open(js_path) as f:
            js = f.read()
            st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)
    
    # Inject custom HTML structure
    html_path = file_path("templates/base.html")
    if os.path.exists(html_path):
        with open(html_path) as f:
            html = f.read()
            st.components.v1.html(html, height=0, width=0)

# ===== 3. Sample Data Generation =====
def generate_sample_trends(base_hr, base_spo2, base_temp, days=5):
    """Generate realistic sample trend data"""
    return pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Heart Rate': [base_hr + random.randint(-5,5) for _ in range(days)],
        'SpO2': [base_spo2 + random.randint(-1,1) for _ in range(days)],
        'Temperature': [round(base_temp + random.uniform(-0.3,0.3), 2) for _ in range(days)]
    })

# ===== 4. Page Config =====
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom theme at the start
inject_custom_theme()

# GitHub CSV URL
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

# Constants for normal ranges
HR_MIN, HR_MAX = 60, 100
SPO2_MIN, SPO2_MAX = 95, 100
TEMP_MIN, TEMP_MAX = 36.2, 37.2

# ===== 5. Page 1: Introduction =====
def introduction_page():
    # Custom HTML header
    st.markdown("""
    <div class="main-content">
        <div class="card">
            <div class="card-header">
                <h1 class="card-title"><i class="fas fa-user"></i> Patient Profile</h1>
            </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Complete Your Health Profile")
    
    with st.form("patient_intro"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=120)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
        
        medical_history = st.text_area("Medical History (Allergies, Chronic Conditions, etc.)")
        
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state['patient_profile'] = {
                'name': name,
                'age': age,
                'gender': gender,
                'weight': weight,
                'medical_history': medical_history
            }
            st.success("Profile saved successfully!")
    
    if 'patient_profile' in st.session_state:
        st.markdown("### Your Profile Summary")
        profile_df = pd.DataFrame.from_dict(st.session_state['patient_profile'], orient='index', columns=['Value'])
        st.table(profile_df)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ===== 6. Page 2: Health Monitor =====
def health_monitor_page():
    # Custom HTML header
    st.markdown("""
    <div class="main-content">
        <div class="card">
            <div class="card-header">
                <h1 class="card-title"><i class="fas fa-heartbeat"></i> Health Monitoring</h1>
            </div>
    """, unsafe_allow_html=True)
    
    # User input section
    st.markdown("### 📊 Enter Your Vital Signs")
    col1, col2, col3 = st.columns(3)
    with col1:
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
    with col2:
        spO2 = st.number_input("Blood Oxygen Level (%)", min_value=70, max_value=100, value=97)
    with col3:
        temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

    # Train model and predict
    model = train_model()
    data = pd.DataFrame([[heart_rate, spO2, temperature]], 
                       columns=["heart_rate", "spO2", "temperature"])
    prediction = model.predict(data)[0]

    # Enhanced detection
    is_hr_abnormal = heart_rate < HR_MIN or heart_rate > HR_MAX
    is_spo2_abnormal = spO2 < SPO2_MIN
    is_temp_abnormal = temperature < TEMP_MIN or temperature > TEMP_MAX
    is_anomaly = prediction == -1 or is_hr_abnormal or is_spo2_abnormal or is_temp_abnormal

    # Results display with custom styling
    if is_anomaly:
        st.markdown("""
        <div class="metric-card danger">
            <h3><i class="fas fa-exclamation-triangle"></i> Anomaly Detected!</h3>
            <p>Please consult a doctor immediately.</p>
        </div>
        """, unsafe_allow_html=True)
        
        anomaly_details = []
        if is_hr_abnormal:
            anomaly_details.append(f"Heart Rate: {heart_rate} bpm (Normal: 60-100)")
        if is_spo2_abnormal:
            anomaly_details.append(f"SpO2: {spO2}% (Normal: ≥95%)")
        if is_temp_abnormal:
            anomaly_details.append(f"Temperature: {temperature}°C (Normal: 36.2-37.2)")
        
        st.markdown("#### Abnormal Values:")
        for detail in anomaly_details:
            st.markdown(f"- ❌ {detail}")
    else:
        st.markdown("""
        <div class="metric-card normal">
            <h3><i class="fas fa-check-circle"></i> Vitals Normal</h3>
            <p>All readings within expected ranges.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        #### Your Readings:
        - Heart rate: {heart_rate} bpm (normal: 60-100)
        - SpO2: {spO2}% (normal: 95-100)
        - Temperature: {temperature}°C (normal: 36.2-37.2)
        """)

    # Health trends visualization
    st.markdown("### 📈 Health Trends")
    trend_data = generate_sample_trends(heart_rate, spO2, temperature)
    st.line_chart(trend_data.set_index('Day'))

    # Doctor contact form
    st.markdown("### 📞 Contact a Doctor")
    with st.form("doctor_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Describe your symptoms or concerns")

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
                updated = new_entry

            updated.to_csv("doctor_requests.csv", index=False)
            st.success("Your request has been submitted successfully!")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ===== 7. Navigation =====
PAGES = {
    "Patient Profile": introduction_page,
    "Health Monitor": health_monitor_page
}

# Custom sidebar navigation
st.sidebar.markdown("""
<div class="sidebar">
    <div class="logo-container">
        <img src="https://via.placeholder.com/100x100?text=HM" alt="Logo">
        <h2>AI Health Monitor</h2>
    </div>
</div>
""", unsafe_allow_html=True)

selection = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    format_func=lambda x: f"📌 {x}" if x == "Patient Profile" else f"🩺 {x}"
)

# Display the selected page
page = PAGES[selection]
page()

# Emergency button in sidebar
st.sidebar.markdown("""
<div class="emergency-contact">
    <button id="emergency-btn" class="btn btn-danger">
        <i class="fas fa-ambulance"></i> Emergency
    </button>
</div>
""", unsafe_allow_html=True)

# Doctor contacts in sidebar
st.sidebar.markdown("""
<div class="card">
    <div class="card-header">
        <h3 class="card-title"><i class="fas fa-user-md"></i> Available Doctors</h3>
    </div>
    <p><strong>Dr. Tony Wabuko</strong><br>
    <a href="mailto:tonywabuko@gmail.com">tonywabuko@gmail.com</a></p>
    
    <p><strong>Dr. Brian Sangura</strong><br>
    <a href="mailto:sangura.bren@gmail.com">sangura.bren@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)
