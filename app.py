# Add this import at the top
from model import predict_anomaly

# Add this function to the Helper Functions section
def check_vital_signs(vitals):
    """Check vitals against normal ranges and model for anomalies"""
    results = []
    anomaly_detected = False
    
    # Check against clinical ranges
    for param, value in vitals.items():
        if param in NORMAL_RANGES:
            low, high = NORMAL_RANGES[param]
            if value < low or value > high:
                results.append(f"⚠️ {param} is outside normal range ({low}-{high})")
    
    # Check with anomaly detection model
    try:
        prediction, score = predict_anomaly(vitals)
        if prediction == -1:  # -1 indicates anomaly
            anomaly_detected = True
            results.append(f"🚨 AI detected potential anomaly (confidence: {abs(score):.2f})")
    except Exception as e:
        st.error(f"Error in anomaly detection: {str(e)}")
    
    return results, anomaly_detected

# Add this new section to the Health Monitor page
if st.session_state.current_page == "Health Monitor":
    # ... (existing code)
    
    # Add this new expander after the existing ones
    with st.expander("🩹 Vital Signs Checker", expanded=True):
        st.subheader("Enter Your Vital Signs")
        
        col1, col2 = st.columns(2)
        with col1:
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=72)
            spO2 = st.number_input("Blood Oxygen (SpO2 %)", min_value=70, max_value=100, value=98)
            temperature = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=36.8, step=0.1)
        
        with col2:
            resp_rate = st.number_input("Respiratory Rate (breaths/min)", min_value=8, max_value=40, value=16)
            bp_sys = st.number_input("Blood Pressure Systolic (mmHg)", min_value=70, max_value=200, value=120)
            bp_dia = st.number_input("Blood Pressure Diastolic (mmHg)", min_value=40, max_value=120, value=80)
        
        if st.button("Check Vital Signs"):
            vitals = {
                "heart_rate": heart_rate,
                "spO2": spO2,
                "temperature": temperature,
                "resp_rate": resp_rate,
                "blood_pressure_sys": bp_sys,
                "blood_pressure_dia": bp_dia
            }
            
            results, anomaly_detected = check_vital_signs(vitals)
            
            if results:
                if anomaly_detected:
                    st.error("### Anomaly Detected in Vital Signs!")
                else:
                    st.warning("### Potential Issues Found")
                
                for result in results:
                    st.write(result)
                
                if anomaly_detected:
                    st.error("Recommendation: Please consult a doctor immediately")
            else:
                st.success("All vital signs appear normal!")
