import streamlit as st
import pandas as pd
import numpy as np
from model import train_model

# Try to import visualization libraries with fallbacks
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.sidebar.warning("Plotly not available - using simple charts")

# GitHub CSV URL (raw file link)
CSV_URL = "https://raw.githubusercontent.com/tonywabuko/health_monitor_app/main/doctor_requests.csv"

st.set_page_config(page_title="AI-Powered Health Monitor", layout="centered")

st.title("🩺 AI-Powered Health Monitoring System")
st.markdown("Monitor your vital signs in real-time and get personalized health insights.")

# User input
st.header("📊 Enter Health Metrics")
heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
spO2 = st.number_input("Blood Oxygen Level (%)", min_value=70, max_value=100, value=97)
temperature = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=42.0, value=36.8)

# Train model on deployment
model = train_model()

# Predict
data = pd.DataFrame([[heart_rate, spO2, temperature]], columns=["heart_rate", "spO2", "temperature"])
prediction = model.predict(data)[0]

if prediction == -1:
    st.error(f"""
    ⚠️ Anomaly Detected! Please consult a doctor.
    
    Normal ranges:
    - Heart rate: 60-100 bpm (yours: {heart_rate})
    - SpO2: 95-100% (yours: {spO2})
    - Temperature: 36.2-37.2°C (yours: {temperature})
    """)
else:
    st.success(f"""
    ✅ All vitals appear normal.
    
    Your readings:
    - Heart rate: {heart_rate} bpm (normal: 60-100)
    - SpO2: {spO2}% (normal: 95-100)
    - Temperature: {temperature}°C (normal: 36.2-37.2)
    """)

# Simple historical data visualization (works without Plotly)
st.header("📈 Health Trends")
try:
    # Sample data - replace with your actual data source
    trend_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Heart Rate': [72, 75, 71, 69, 68],
        'SpO2': [98, 97, 99, 96, 97],
        'Temperature': [36.7, 36.8, 37.0, 36.5, 36.6]
    })
    
    if PLOTLY_AVAILABLE:
        fig = px.line(trend_data, x='Day', y=['Heart Rate', 'SpO2', 'Temperature'],
                     title='Weekly Health Trends')
        st.plotly_chart(fig)
    else:
        st.line_chart(trend_data.set_index('Day'))
except Exception as e:
    st.warning(f"Couldn't display trends: {str(e)}")

# Doctor contact form
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
