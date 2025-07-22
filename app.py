import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import json
import os

# Import the dashboard module
try:
    from dashboard import show_health_dashboard
except ImportError:
    st.error("Dashboard module not found")
    show_health_dashboard = None

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
USER_DB_FILE = "users.json"

# Ensure the users.json file exists
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'w') as f:
        json.dump({}, f)

# Page Config
st.set_page_config(
    page_title="AI-Powered Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
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
        max-width: 400px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# User management functions
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
        'created_at': datetime.now().isoformat()
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

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.show_signup = False
    st.session_state.auth_message = None

# Authentication pages
if not st.session_state.logged_in:
    st.title("Health Monitoring System")
    
    if st.session_state.show_signup:
        # Signup form
        with st.container():
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.header("Create Account")
            
            with st.form("signup_form"):
                username = st.text_input("Username", key="signup_username")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
                
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    if not username or not email or not password:
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(username, email, password)
                        if success:
                            st.success(message)
                            st.session_state.show_signup = False
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error(message)
            
            if st.button("Already have an account? Login"):
                st.session_state.show_signup = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Login form
        with st.container():
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.header("Login")
            
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                submitted = st.form_submit_button("Login")
                if submitted:
                    if not username or not password:
                        st.error("Both fields are required")
                    else:
                        success, message = authenticate_user(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error(message)
            
            if st.button("Don't have an account? Sign up"):
                st.session_state.show_signup = True
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# If logged in, show the dashboard
else:
    # Show logout button in sidebar
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Show the health dashboard
    if show_health_dashboard:
        show_health_dashboard()
    else:
        st.error("Dashboard functionality not available")

# Footer
st.markdown("---")
st.markdown("AI Health Monitor © 2023 | Version 1.0")
