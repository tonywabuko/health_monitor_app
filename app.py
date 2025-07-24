import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import json
import os
import time
from model import predict_anomalies

# Constants and Config
USER_DB_FILE = "users.json"
DOCTOR_REQUESTS_FILE = "doctor_requests.csv"
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2)
}

# Initialize data files
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(DOCTOR_REQUESTS_FILE):
    pd.DataFrame(columns=["name", "email", "message", "timestamp"]).to_csv(DOCTOR_REQUESTS_FILE, index=False)

# Page Config
st.set_page_config(
    page_title="Health Companion Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: white;
        border-left: 4px solid #6366f1;
    }
    .emergency-alert {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    .health-tip {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .anomaly-details {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .sidebar-section {
        margin-bottom: 1.5rem;
    }
    .sidebar-title {
        color: #6366f1;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .sidebar-divider {
        margin: 0.5rem 0;
        border-color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# User Management Functions
def load_users():
    try:
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    users[username] = {
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'health_data': []
    }
    save_users(users)
    return True, "Registration successful"

def authenticate_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    if users[username]['password'] != hash_password(password):
        return False, "Invalid password"
    return True, "Authentication successful"

# Health Analysis Functions
def generate_health_response(prompt):
    prompt = prompt.lower().strip()
    
    medical_knowledge = {
        "fever": """**Treatment:**
- Paracetamol 1g every 6 hours (max 4g/day)
- Ibuprofen 400mg every 8 hours with food
- Cool compresses
⚠️ Seek help if >39°C or >3 days""",
        "headache": """**Relief:**
- Hydrate
- Rest in dark room
- Cold compress
- Paracetamol/Ibuprofen
⚠️ Emergency for severe pain"""
    }
    
    for term, response in medical_knowledge.items():
        if term in prompt:
            return response
    
    return """I can help with:
- Fever advice
- Headache relief
- Anomaly detection
Consult a doctor for serious concerns."""

def analyze_symptoms(symptoms):
    symptoms = [s.lower() for s in symptoms]
    conditions = []
    emergency = False
    
    if "chest pain" in symptoms:
        conditions.append("Possible cardiac issue")
        emergency = True
    if "fever" in symptoms:
        conditions.append("Infection")
    
    return {
        "conditions": conditions or ["General illness"],
        "recommendation": "Seek immediate care" if emergency else "Rest and monitor",
        "emergency": emergency
    }

# Session State Management
if 'logged_in' not in st.session_state:
    st.session_state.update({
        'logged_in': False,
        'show_signup': False,
        'current_page': "Health Monitor",
        'username': None,
        'health_chat': []
    })

# Authentication Flow
if not st.session_state.logged_in:
    st.title("Health Companion Pro")
    
    if st.session_state.show_signup:
        with st.form("signup_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Sign Up"):
                if password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    success, message = register_user(username, email, password)
                    if success:
                        st.session_state.update({
                            'logged_in': True,
                            'username': username,
                            'show_signup': False
                        })
                        st.rerun()
                    st.error(message)
        
        if st.button("Already have an account? Login"):
            st.session_state.show_signup = False
            st.rerun()
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                success, message = authenticate_user(username, password)
                if success:
                    st.session_state.update({
                        'logged_in': True,
                        'username': username
                    })
                    st.rerun()
                st.error(message)
        
        if st.button("Don't have an account? Sign up"):
            st.session_state.show_signup = True
            st.rerun()
else:
    # Main Application with Enhanced Sidebar
    with st.sidebar:
        # Welcome Section
        st.markdown(f"""
        <div class="sidebar-section">
            <h3 style="color: #6366f1; margin-bottom: 0;">Welcome,</h3>
            <h3 style="color: #6366f1; margin-top: 0;">{st.session_state.username}!</h3>
            <hr class="sidebar-divider">
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown("""
        <div class="sidebar-section">
            <p class="sidebar-title">NAVIGATION</p>
        """, unsafe_allow_html=True)
        
        # Navigation buttons without icons
        nav_options = [
            ("Health Monitor", "Health Monitor"),
            ("Dashboard", "Dashboard"),
            ("Contact Doctor", "Contact Doctor")
        ]
        
        for text, page in nav_options:
            if st.button(
                text,
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page else "secondary"
            ):
                st.session_state.current_page = page
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Account Section
        st.markdown("""
        <div class="sidebar-section">
            <hr class="sidebar-divider">
            <p class="sidebar-title">ACCOUNT</p>
        """, unsafe_allow_html=True)
        
        if st.button(
            "🚪 Logout",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.update({
                'logged_in': False,
                'username': None
            })
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Page Routing
    if st.session_state.current_page == "Health Monitor":
        st.title("🤖 AI Health Assistant")
        
        with st.expander("💬 Health Chatbot", expanded=True):
            for message in st.session_state.health_chat:
                st.chat_message(message["role"]).write(message["content"])
            
            if prompt := st.chat_input("Ask health questions..."):
                st.session_state.health_chat.append({"role": "user", "content": prompt})
                with st.chat_message("assistant"):
                    response = generate_health_response(prompt)
                    st.write(response)
                    st.session_state.health_chat.append({"role": "assistant", "content": response})
        
        with st.expander("🩺 Symptom Checker"):
            symptoms = st.multiselect(
                "Select symptoms",
                ["Fever", "Cough", "Headache", "Chest pain"]
            )
            if st.button("Analyze"):
                if symptoms:
                    analysis = analyze_symptoms(symptoms)
                    st.write(f"**Conditions:** {', '.join(analysis['conditions'])}")
                    st.write(f"**Action:** {analysis['recommendation']}")
    
    elif st.session_state.current_page == "Dashboard":
        st.title("📊 Health Dashboard")
        
        # Anomaly Detection Section
        st.header("Vital Signs Checker")
        col1, col2, col3 = st.columns(3)
        with col1:
            hr = st.number_input("Heart Rate (bpm)", 30, 200, 72)
        with col2:
            spo2 = st.number_input("SpO2 (%)", 70, 100, 98)
        with col3:
            temp = st.number_input("Temp (°C)", 35.0, 42.0, 36.8, 0.1)
        
        if st.button("Check for Anomalies"):
            result = predict_anomalies(hr, spo2, temp)
            
            if result['is_anomaly']:
                st.error(f"{result['message']} (Score: {result['score']:.2f})")
                with st.expander("Anomaly Details"):
                    st.markdown("""
                    <div class="anomaly-details">
                        <h4>⚠️ Abnormal Vital Signs Detected</h4>
                        <p>One or more of your readings are outside normal ranges:</p>
                        <ul>
                            <li><b>Heart Rate:</b> Normal (60-100 bpm)</li>
                            <li><b>SpO2:</b> Normal (95-100%)</li>
                            <li><b>Temperature:</b> Normal (36.2-37.2°C)</li>
                        </ul>
                        <p>Please consult with a doctor if you feel unwell.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success(f"{result['message']} (Score: {result['score']:.2f})")
                st.balloons()
        
        # Health Trends
        st.header("Weekly Trends")
        trend_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Heart Rate': [72, 74, 71, 73, 75, 70, 68],
            'Steps': [4500, 6200, 5800, 7100, 6800, 8900, 5200]
        })
        st.line_chart(trend_data.set_index('Day'))
    
    elif st.session_state.current_page == "Contact Doctor":
        st.title("👨‍⚕️ Contact Doctor")
        
        st.subheader("Available Doctors")
        doc_cols = st.columns(2)
        
        with doc_cols[0]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Wabuko</h4>
                <p>General Practitioner</p>
                <p>📧 tonywabuko@gmail.com</p>
                <p>📞 +254 799104517</p>
                <p>🕒 Available: Mon-Fri, 9AM-5PM</p>
            </div>
            """, unsafe_allow_html=True)
        
        with doc_cols[1]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Sangura</h4>
                <p>ICU Specialist</p>
                <p>📧 sangura.bren@gmail.com</p>
                <p>📞 +254 720638389</p>
                <p>🕒 Available: 24/7 Emergency</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            doctor = st.selectbox("Select Doctor", ["Dr. Wabuko", "Dr. Sangura"])
            message = st.text_area("Your Message")
            
            if st.form_submit_button("Send Message"):
                st.success("Message sent to doctor!")
