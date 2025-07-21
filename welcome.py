import streamlit as st
import time

def welcome_page():
    st.set_page_config(page_title="Welcome to HealthGuard", page_icon="👋")
    
    st.markdown("""
    <style>
        .welcome-header {
            font-size: 2.5em;
            color: #1e88e5;
            text-align: center;
            margin-bottom: 30px;
        }
        .feature-card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f9ff;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .get-started-btn {
            background-color: #1e88e5 !important;
            color: white !important;
            font-weight: bold !important;
            padding: 10px 24px !important;
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-header">👋 Welcome to HealthGuard</div>', unsafe_allow_html=True)
    
    st.image("https://i.imgur.com/3JmBJqU.png", width=300)  # Replace with your image
    
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Real-time Health Monitoring</h3>
        <p>Track your vital signs with AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>⚠️ Anomaly Detection</h3>
        <p>Get instant alerts for abnormal readings</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>👨‍⚕️ Doctor Connect</h3>
        <p>Consult healthcare professionals when needed</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Get Started", key="get_started", help="Begin your health journey"):
        st.session_state['show_welcome'] = False
        st.rerun()

# In your app.py
if 'show_welcome' not in st.session_state:
    st.session_state['show_welcome'] = True

if st.session_state['show_welcome']:
    welcome_page()
else:
    # Your existing app logic here
    pass
