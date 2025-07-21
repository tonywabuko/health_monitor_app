import streamlit as st
import pandas as pd
from model import load_model

def run():
    st.title("🩺 Health Monitoring")
    st.write("Please input your vitals:")

    heart_rate = st.number_input("Heart Rate (bpm)", 40, 200, 75)
    spO2 = st.number_input("SpO2 (%)", 70, 100, 98)
    temperature = st.number_input("Temperature (°C)", 30.0, 43.0, 36.8)

    if st.button("Check Vitals"):
        model = load_model()
        input_data = pd.DataFrame([[heart_rate, spO2, temperature]],
                                  columns=["heart_rate", "spO2", "temperature"])
        prediction = model.predict(input_data)

        if prediction[0] == -1:
            st.error("⚠️ Anomaly Detected! Please consult a medical professional.")
        else:
            st.success("✅ Your vitals appear normal.")
