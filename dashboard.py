import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from model import load_model  # Ensure this is available

# Emergency illness prediction mapping
ILLNESS_MAPPING = {
    0: "Normal",
    1: "Pneumonia",
    2: "Tuberculosis (TB)",
    3: "Respiratory Distress",
    4: "Cardiac Issue",
    5: "Sepsis Risk"
}

# Normal ranges for vital signs
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2),
    "resp_rate": (12, 20),
    "blood_pressure_sys": (90, 120),
    "blood_pressure_dia": (60, 80)
}

# Page configuration
st.set_page_config(
    page_title="Health Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
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
    .metric-card h3 {
        color: #ffffff;
        margin-bottom: 12px;
    }
    .metric-card p {
        color: #e2e8f0;
        margin-bottom: 8px;
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
</style>
""", unsafe_allow_html=True)


def show_health_dashboard():
    st.title("🩺 Health Monitoring Dashboard")
    st.markdown("Monitor your vital signs and receive real-time health insights.")

    # Main metrics section
    st.header("📊 Vital Signs Monitoring")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        heart_rate = st.number_input(
            "Heart Rate (bpm)", 
            min_value=40, 
            max_value=200, 
            value=75,
            help=f"Normal range: {NORMAL_RANGES['heart_rate'][0]}-{NORMAL_RANGES['heart_rate'][1]} bpm"
        )
        resp_rate = st.number_input(
            "Respiratory Rate (breaths/min)", 
            min_value=8, 
            max_value=40, 
            value=16,
            help=f"Normal range: {NORMAL_RANGES['resp_rate'][0]}-{NORMAL_RANGES['resp_rate'][1]}"
        )
    
    with col2:
        spO2 = st.number_input(
            "Blood Oxygen (%)", 
            min_value=70, 
            max_value=100, 
            value=97,
            help=f"Normal range: {NORMAL_RANGES['spO2'][0]}-{NORMAL_RANGES['spO2'][1]}%"
        )
        bp_sys = st.number_input(
            "Blood Pressure (Systolic)", 
            min_value=70, 
            max_value=200, 
            value=120,
            help=f"Normal range: {NORMAL_RANGES['blood_pressure_sys'][0]}-{NORMAL_RANGES['blood_pressure_sys'][1]}"
        )
    
    with col3:
        temperature = st.number_input(
            "Temperature (°C)", 
            min_value=30.0, 
            max_value=42.0, 
            value=36.8, 
            step=0.1,
            help=f"Normal range: {NORMAL_RANGES['temperature'][0]}-{NORMAL_RANGES['temperature'][1]}°C",
            format="%.1f"
        )
        bp_dia = st.number_input(
            "Blood Pressure (Diastolic)", 
            min_value=40, 
            max_value=120, 
            value=80,
            help=f"Normal range: {NORMAL_RANGES['blood_pressure_dia'][0]}-{NORMAL_RANGES['blood_pressure_dia'][1]}"
        )

    # Prediction section
    st.header("🩺 Health Assessment")
    
    try:
        # Load model and predict
        model = load_model()
        input_data = pd.DataFrame([{
            "heart_rate": heart_rate,
            "spO2": spO2,
            "temperature": temperature,
            "resp_rate": resp_rate,
            "blood_pressure_sys": bp_sys,
            "blood_pressure_dia": bp_dia
        }])
        
        prediction = model.predict(input_data)[0]
        predicted_illness = ILLNESS_MAPPING.get(prediction, "Unknown Condition")
        
        # Manual range checks
        hr_normal = NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1]
        spo2_normal = NORMAL_RANGES["spO2"][0] <= spO2 <= NORMAL_RANGES["spO2"][1]
        temp_normal = NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1]
        resp_normal = NORMAL_RANGES["resp_rate"][0] <= resp_rate <= NORMAL_RANGES["resp_rate"][1]
        bp_sys_normal = NORMAL_RANGES["blood_pressure_sys"][0] <= bp_sys <= NORMAL_RANGES["blood_pressure_sys"][1]
        bp_dia_normal = NORMAL_RANGES["blood_pressure_dia"][0] <= bp_dia <= NORMAL_RANGES["blood_pressure_dia"][1]
        
        all_normal = all([hr_normal, spo2_normal, temp_normal, resp_normal, bp_sys_normal, bp_dia_normal])
        
        if not all_normal or predicted_illness != "Normal":
            st.markdown(f"""
            <div class="emergency-alert">
                <h3>⚠️ Emergency Alert!</h3>
                <p>Predicted Condition: <strong>{predicted_illness}</strong></p>
                <p>Abnormal Values Detected:</p>
                <ul>
                    {f"<li>Heart Rate: {heart_rate} bpm (Normal: 60-100)</li>" if not hr_normal else ""}
                    {f"<li>SpO2: {spO2}% (Normal: 95-100)</li>" if not spo2_normal else ""}
                    {f"<li>Temperature: {temperature:.1f}°C (Normal: 36.2-37.2)</li>" if not temp_normal else ""}
                    {f"<li>Respiratory Rate: {resp_rate} (Normal: 12-20)</li>" if not resp_normal else ""}
                    {f"<li>Blood Pressure: {bp_sys}/{bp_dia} (Normal: 90-120/60-80)</li>" if not (bp_sys_normal and bp_dia_normal) else ""}
                </ul>
                <p>Please consult a doctor immediately!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"""
            ✅ All vitals appear normal. No emergency conditions detected.
            
            ### Your Current Readings:
            - Heart rate: {heart_rate} bpm (Normal: 60-100)
            - SpO2: {spO2}% (Normal: 95-100)
            - Temperature: {temperature:.1f}°C (Normal: 36.2-37.2)
            - Respiratory Rate: {resp_rate} (Normal: 12-20)
            - Blood Pressure: {bp_sys}/{bp_dia} (Normal: 90-120/60-80)
            """)
            
    except Exception as e:
        st.error(f"Error in health assessment: {str(e)}")
        st.info("Using basic range checks instead of AI model")
        
        # Basic range checks if model fails
        hr_normal = NORMAL_RANGES["heart_rate"][0] <= heart_rate <= NORMAL_RANGES["heart_rate"][1]
        spo2_normal = NORMAL_RANGES["spO2"][0] <= spO2 <= NORMAL_RANGES["spO2"][1]
        temp_normal = NORMAL_RANGES["temperature"][0] <= temperature <= NORMAL_RANGES["temperature"][1]
        
        if not all([hr_normal, spo2_normal, temp_normal]):
            st.warning("""
            ⚠️ Abnormal Values Detected!
            
            Please consult a doctor if you feel unwell.
            
            Abnormal Values:
            """ + 
            (f"- Heart Rate: {heart_rate} bpm (Normal: 60-100)\n" if not hr_normal else "") +
            (f"- SpO2: {spO2}% (Normal: 95-100)\n" if not spo2_normal else "") +
            (f"- Temperature: {temperature:.1f}°C (Normal: 36.2-37.2)\n" if not temp_normal else ""))
        else:
            st.success("All basic vitals appear normal.")

    # Doctors section
    st.header("👨‍⚕️ Available Doctors")
    with st.expander("View Doctors", expanded=True):
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Tony Wabuko</h4>
                <p>tonywabuko@gmail.com</p>
                <p>+254 700 000000</p>
                <p>General Practitioner</p>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown("""
            <div class="metric-card">
                <h4>Dr. Brian Sangura</h4>
                <p>sangura.bren@gmail.com</p>
                <p>+254 700 000001</p>
                <p>ICU Specialist</p>
            </div>
            """, unsafe_allow_html=True)

    # Contact form
    with st.form("doctor_form"):
        st.subheader("📩 Contact a Doctor")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        
        submitted = st.form_submit_button("Send Request")
        if submitted:
            # Basic input validation
            if not name or not email or not message or '@' not in email:
                st.error("Please provide a valid name, email, and message.")
            else:
                new_entry = pd.DataFrame([{
                    "name": name,
                    "email": email,
                    "message": message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                try:
                    existing = pd.read_csv("doctor_requests.csv")
                    updated = pd.concat([existing, new_entry], ignore_index=True)
                except Exception:
                    updated = new_entry
                
                try:
                    updated.to_csv("doctor_requests.csv", index=False)
                    st.success("✅ Request submitted successfully!")
                except Exception as e:
                    st.error(f"Error saving request: {str(e)}")

if __name__ == "__main__":
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        show_health_dashboard()
    else:
        st.warning("Please log in to access the health dashboard")
        st.page_link("app.py", label="Go to Login Page")
