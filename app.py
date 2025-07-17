import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from model import detect_anomalies, load_model
from health_data import simulate_data
import os
from datetime import datetime

# Load the trained model
model = load_model()

st.set_page_config(page_title="AI Health Monitor", layout="centered")
st.title("🩺 AI-Powered Health Monitoring System")

# Sidebar for data entry
st.sidebar.header("Input Your Vitals")
heart_rate = st.sidebar.slider("Heart Rate (bpm)", 40, 180, 72)
blood_oxygen = st.sidebar.slider("SpO2 (%)", 70, 100, 98)

# Simulate or use real-time input
input_data = pd.DataFrame([{
    'heart_rate': heart_rate,
    'blood_oxygen': blood_oxygen
}])

# Anomaly detection
results = detect_anomalies(input_data, model)

st.subheader("📊 Vitals Overview")
st.write(results)

# Visualization
chart = alt.Chart(results.reset_index()).mark_bar().encode(
    x='index',
    y='heart_rate',
    color=alt.condition(
        alt.datum.anomaly == 'Anomaly',
        alt.value('red'),
        alt.value('green')
    )
).properties(title="Heart Rate Trend")
st.altair_chart(chart, use_container_width=True)

# Recommendations
st.subheader("🧠 Health Recommendation")
anomaly = results.iloc[0]["anomaly"]
recommendation = ""

if anomaly == "Anomaly":
    if heart_rate > 120:
        recommendation = "High heart rate detected. Seek medical advice."
    elif heart_rate < 50:
        recommendation = "Low heart rate detected. Monitor for dizziness or fatigue."
    elif blood_oxygen < 90:
        recommendation = "Low oxygen saturation. Use a pulse oximeter or consult a doctor."
    else:
        recommendation = "Vitals are unusual. Monitor your symptoms closely."
else:
    recommendation = "Your vitals are within the normal range. Keep monitoring."

st.success(recommendation)

# Contact a doctor
st.subheader("📞 Contact a Doctor")
doctors = {
    "Tony Wabuko": {"phone": "0799104517", "email": "tonywabuko@gmail.com"},
    "Brian Sangura": {"phone": "0720638389", "email": "sangura.bren@gmail.com"}
}

selected_doc = st.selectbox("Select a doctor", list(doctors.keys()))
user_name = st.text_input("Your Name")
user_phone = st.text_input("Your Phone")
user_msg = st.text_area("Message")

if st.button("Send Request"):
    if user_name and user_phone and user_msg:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = {
            "Timestamp": timestamp,
            "Patient Name": user_name,
            "Patient Phone": user_phone,
            "Doctor": selected_doc,
            "Doctor Phone": doctors[selected_doc]["phone"],
            "Doctor Email": doctors[selected_doc]["email"],
            "Message": user_msg
        }
        df = pd.DataFrame([record])
        file_path = "doctor_requests.csv"
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', index=False, header=False)
        else:
            df.to_csv(file_path, index=False)
        st.success(
            "✅ Your request was sent to the doctor and logged for follow-up.")
    else:
        st.error("❗Please fill in all the fields.")
