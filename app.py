import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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

# Page Config
st.set_page_config(
    page_title="AI-Powered Health Monitor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login page if not logged in
if not st.session_state.logged_in:
    st.title("Login to Health Monitor")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Simple authentication (replace with your actual auth logic)
        if username == "admin" and password == "password":  # Example credentials
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
        st.rerun()

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
