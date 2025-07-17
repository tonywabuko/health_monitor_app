import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import os
import random  # For generating sample data

# ===== 1. Modern UI Theme =====
def load_css():
    """Load the CSS styles from the assets directory"""
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles', 'main.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styles.")
        st.markdown("""
        <style>
            .stApp { font-family: Arial, sans-serif; }
            .metric-card { padding: 10px; border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)

# Initialize the app
load_css()
st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GitHub CSV URL (raw file link)
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

# Constants for normal ranges
HR_MIN, HR_MAX = 60, 100
SPO2_MIN, SPO2_MAX = 95, 100
TEMP_MIN, TEMP_MAX = 36.2, 37.2

# ===== Sample Data Generation =====
def generate_sample_trends(base_hr, base_spo2, base_temp, days=5):
    """Generate realistic sample trend data"""
    return pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Heart Rate': [base_hr + random.randint(-5,5) for _ in range(days)],
        'SpO2': [base_spo2 + random.randint(-1,1) for _ in range(days)],
        'Temperature': [round(base_temp + random.uniform(-0.3,0.3),2) for _ in range(days)]
    })

# ===== Page 1: Introduction =====
def introduction_page():
    st.title("🩺 Welcome to AI Health Monitor")
    st.image("https://via.placeholder.com/800x200?text=Health+Monitoring+Banner", use_column_width=True)
    
    st.markdown("""
    ## Your Personal Health Companion
    Monitor your vital signs in real-time and get personalized health insights.
    """)
    
    with st.expander("📌 How It Works"):
        st.markdown("""
        1. **Complete your profile** on this page
        2. **Navigate to Health Monitor** in the sidebar
        3. **Enter your vitals** or connect wearable devices
        4. **Get instant analysis** and recommendations
        """)
    
    st.header("About You")
    with st.form("patient_intro"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        medical_history = st.text_area("Medical History (Optional)")
        
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state['patient_profile'] = {
                'name': name,
                'age': age,
                'gender': gender,
                'medical_history': medical_history
            }
            st.success("Profile saved! Proceed to Health Monitor.")
    
    if 'patient_profile' in st.session_state:
        st.subheader("Your Profile Summary")
        st.json(st.session_state['patient_profile'])

# ===== Page 2: Health Monitor =====
def health_monitor_page():
    st.title("🩺 AI-Powered Health Monitoring System")
    
    # User input section
    with st.container():
        st.header("📊 Enter Health Metrics")
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

    # Results display
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

    # Health trends visualization using generated sample data
    st.header("📈 Health Trends")
    try:
        trend_data = generate_sample_trends(heart_rate, spO2, temperature)
        st.line_chart(trend_data.set_index('Day'))
    except Exception as e:
        st.warning(f"Couldn't display trends: {str(e)}")

    # Doctor contact form (preserved from original)
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

# ===== Navigation =====
PAGES = {
    "Introduction": introduction_page,
    "Health Monitor": health_monitor_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()
