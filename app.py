import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
from passlib.hash import pbkdf2_sha256

try:
    from model import load_model
except ImportError as e:
    st.error(f"Error importing model: {str(e)}")
    st.stop()

# Constants
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2)
}

# Database Setup
def init_db():
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS health_data
                 (user_id INTEGER,
                  heart_rate REAL,
                  spO2 REAL,
                  temperature REAL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Page Config
st.set_page_config(
    page_title="AI-Powered Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS - Added new styles for auth forms
st.markdown("""
<style>
    .doctor-card {
        background-color: #1e293b !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        color: white !important;
        border-left: 4px solid #6366f1;
    }
    .doctor-card h4 {
        color: #ffffff !important;
        margin-bottom: 12px;
    }
    .doctor-card p {
        color: #e2e8f0 !important;
        margin-bottom: 8px;
    }
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #f0f9ff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Session State Management
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# Authentication Functions
def create_user(name, email, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    hashed_pw = pbkdf2_sha256.hash(password)
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                 (name, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("SELECT id, name, password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    
    if result and pbkdf2_sha256.verify(password, result[2]):
        return {'id': result[0], 'name': result[1]}
    return None

# Authentication Page
def auth_page():
    with st.container():
        st.title("🔐 Health Monitor Login")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login"):
                    user = verify_user(email, password)
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['current_user'] = user
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("register_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_pw = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Register"):
                    if password != confirm_pw:
                        st.error("Passwords don't match!")
                    elif create_user(name, email, password):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Email already exists")

# Main App Page
def main_app():
    # Header - Now personalized
    st.title(f"🩺 Welcome, {st.session_state['current_user']['name']}")
    st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

    # Health Metrics in Cards
    st.header("📊 Your Health Metrics")
    
    with st.container():
        cols = st.columns(3)
        with cols[0]:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75, 
                                           help=f"Normal range: {NORMAL_RANGES['heart_rate'][0]}-{NORMAL_RANGES['heart_rate'][1]} bpm")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                spO2 = st.number_input("Blood Oxygen (%)", min_value=70, max_value=100, value=97,
                                      help=f"Normal range: {NORMAL_RANGES['spO2'][0]}-{NORMAL_RANGES['spO2'][1]}%")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[2]:
            with st.container():
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8, step=0.1,
                                            help=f"Normal range: {NORMAL_RANGES['temperature'][0]}-{NORMAL_RANGES['temperature'][1]}°C",
                                            format="%.1f")
                st.markdown('</div>', unsafe_allow_html=True)

    # Save health data to database
    if st.button("Save Health Data"):
        conn = sqlite3.connect('health_app.db')
        c = conn.cursor()
        c.execute("""INSERT INTO health_data 
                     (user_id, heart_rate, spO2, temperature) 
                     VALUES (?, ?, ?, ?)""",
                  (st.session_state['current_user']['id'], heart_rate, spO2, temperature))
        conn.commit()
        conn.close()
        st.success("Health data saved successfully!")

    # Rest of your existing code remains unchanged...
    # [Keep all your existing model prediction, doctor cards, and contact form code here]
    
    # Add logout button
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

# App Flow Control
if not st.session_state['authenticated']:
    auth_page()
else:
    main_app()
