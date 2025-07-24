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

# Updated CSS for better visibility in dark mode
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
        background-color: #2d3748;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .anomaly-details {
        background-color: #2d3748;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: white;
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
    .anomaly-alert {
        background-color: #2a1a1a;
        border-left: 6px solid #ff4b4b;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        color: #ffffff;
    }
    .normal-results {
        background-color: #1a2a1a;
        border-left: 6px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        color: #ffffff;
    }
    .stChatMessage {
        background-color: #1e293b;
    }
    .stTextInput input {
        background-color: #1e293b;
        color: white;
    }
    .symptom-checker {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .symptom-item {
        background-color: #2d3748;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        display: flex;
        align-items: center;
    }
    .symptom-item input {
        margin-right: 1rem;
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

# Health Analysis Functions - Expanded Knowledge Base
def generate_health_response(prompt):
    prompt = prompt.lower().strip()
    
    medical_knowledge = {
        "fever": """**Fever Treatment:**
- Paracetamol 1g every 6 hours (max 4g/day)
- Ibuprofen 400mg every 8 hours with food
- Cool compresses and stay hydrated
- Rest and monitor temperature
⚠️ Seek medical help if:
- Temperature >39°C or persists >3 days
- Accompanied by stiff neck, confusion, or rash""",
        
        "headache": """**Headache Relief:**
- Hydrate well (dehydration causes headaches)
- Rest in a quiet, dark room
- Cold compress on forehead
- Gentle neck stretches
- Paracetamol 500-1000mg every 4-6 hours
⚠️ Emergency if:
- Sudden, severe "thunderclap" headache
- Headache after head injury
- With fever, rash, confusion, or vision changes""",
        
        "cough": """**Cough Management:**
- Stay hydrated with warm liquids
- Honey (1-2 tsp) can help soothe throat
- Steam inhalation for congestion
- Cough drops or lozenges
- Elevate head while sleeping
⚠️ See doctor if:
- Cough lasts >3 weeks
- Blood in phlegm
- Shortness of breath or wheezing""",
        
        "chest pain": """🚨 **Chest Pain Warning:**
This could indicate serious conditions like heart attack
- Stop activity and sit down
- Call emergency services immediately
- Chew 325mg aspirin if available (unless allergic)
⚠️ Especially concerning if:
- Radiates to arm/jaw
- With sweating, nausea, shortness of breath""",
        
        "fatigue": """**Fatigue Management:**
- Ensure 7-9 hours quality sleep
- Stay hydrated and eat balanced meals
- Regular moderate exercise
- Check for anemia (iron-rich foods)
- Manage stress with relaxation techniques
⚠️ Concerning if:
- Persistent despite adequate rest
- With weight loss, fever, or other symptoms""",
        
        "dizziness": """**Dizziness Care:**
- Sit or lie down immediately
- Hydrate with water or electrolyte drink
- Avoid sudden position changes
- Check blood pressure if possible
⚠️ Emergency if:
- With chest pain, palpitations
- Severe headache or vision changes
- Difficulty speaking or weakness""",
        
        "abdominal pain": """**Abdominal Pain Advice:**
- Clear fluids if nauseous
- Avoid fatty/spicy foods
- Warm compress on abdomen
- Peppermint tea may help
⚠️ Seek urgent care if:
- Severe, worsening pain
- Pain with vomiting blood
- Black/tarry stools
- Unable to keep fluids down""",
        
        "rash": """**Rash Care:**
- Keep area clean and dry
- Apply fragrance-free moisturizer
- Cool compress for itching
- OTC hydrocortisone cream
⚠️ See doctor if:
- Covers large area or worsens
- With fever or difficulty breathing
- Blisters or open sores develop""",
        
        "back pain": """**Back Pain Relief:**
- Heat or ice packs
- Gentle stretching
- OTC pain relievers
- Maintain good posture
⚠️ Emergency if:
- After trauma or fall
- With leg weakness/numbness
- Loss of bowel/bladder control"""
    }
    
    # Check for exact matches first
    for term, response in medical_knowledge.items():
        if term in prompt:
            return response
    
    # Check for related terms
    related_terms = {
        "temperature": "fever",
        "migraine": "headache",
        "tired": "fatigue",
        "vertigo": "dizziness",
        "stomach ache": "abdominal pain",
        "skin irritation": "rash",
        "sore throat": "cough"
    }
    
    for term, mapped_term in related_terms.items():
        if term in prompt:
            return medical_knowledge[mapped_term]
    
    # General health advice
    general_responses = [
        "For accurate medical advice, please consult with a healthcare professional.",
        "I can provide general information, but serious symptoms should be evaluated by a doctor.",
        "Monitor your symptoms and seek medical attention if they worsen or persist.",
        "Maintaining hydration and rest is often helpful for general illness recovery."
    ]
    
    return """I can help with information about:
- Fever and infections
- Headaches and migraines
- Respiratory symptoms like cough
- Chest and abdominal pain
- Fatigue and dizziness
- Skin rashes and irritations
- Back and muscle pain

For emergencies or serious symptoms, please contact medical services immediately.""" + "\n\n" + np.random.choice(general_responses)

def analyze_symptoms(symptoms):
    symptoms = [s.lower() for s in symptoms]
    conditions = []
    emergency = False
    
    symptom_conditions = {
        "chest pain": ("Possible cardiac issue", True),
        "fever": ("Infection or inflammatory condition", False),
        "shortness of breath": ("Respiratory or cardiac issue", True),
        "severe headache": ("Possible migraine or neurological issue", True),
        "dizziness with weakness": ("Possible neurological or cardiovascular issue", True),
        "abdominal pain with vomiting": ("Gastrointestinal issue", False),
        "rash with fever": ("Possible infectious disease", True),
        "confusion": ("Neurological issue", True),
        "unexplained weight loss": ("Metabolic or systemic illness", True),
        "persistent fatigue": ("Possible anemia or chronic condition", False),
        "swelling in legs": ("Possible cardiovascular or renal issue", False),
        "frequent urination": ("Possible diabetes or UTI", False),
        "back pain with fever": ("Possible kidney infection", True),
        "vision changes": ("Ophthalmological or neurological issue", True),
        "numbness or tingling": ("Neurological issue", True)
    }
    
    for symptom, (condition, is_emergency) in symptom_conditions.items():
        if symptom in symptoms:
            conditions.append(condition)
            if is_emergency:
                emergency = True
    
    if not conditions:
        conditions.append("General illness - monitor symptoms")
    
    return {
        "conditions": conditions,
        "recommendation": "🚨 Seek immediate medical care" if emergency else "Monitor and consult doctor if symptoms persist",
        "emergency": emergency,
        "severity": "High" if emergency else "Moderate" if conditions else "Low"
    }

# Session State Management
if 'logged_in' not in st.session_state:
    st.session_state.update({
        'logged_in': False,
        'show_signup': False,
        'current_page': "Health Monitor",
        'username': None,
        'health_chat': [],
        'symptom_history': []
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
            ("Contact Doctor", "Contact Doctor"),
            ("Symptom History", "Symptom History")
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
        
        # Health Tips Section
        st.markdown("""
        <div class="sidebar-section">
            <hr class="sidebar-divider">
            <p class="sidebar-title">HEALTH TIPS</p>
            <div class="health-tip">
                <p><b>💧 Stay Hydrated</b><br>Drink at least 8 glasses of water daily</p>
            </div>
            <div class="health-tip">
                <p><b>🛌 Quality Sleep</b><br>Aim for 7-9 hours nightly</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        with st.expander("🩺 Symptom Checker", expanded=True):
            st.markdown("""
            <div class="symptom-checker">
                <h4 style="color: #6366f1;">Select your symptoms</h4>
                <p>Choose all that apply to get personalized advice</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Organized symptom categories
            categories = {
                "General": ["Fever", "Fatigue", "Unexplained weight loss", "Night sweats"],
                "Head/Neurological": ["Headache", "Dizziness", "Confusion", "Vision changes"],
                "Chest/Respiratory": ["Chest pain", "Shortness of breath", "Cough", "Palpitations"],
                "Abdominal": ["Abdominal pain", "Nausea/Vomiting", "Diarrhea", "Constipation"],
                "Musculoskeletal": ["Back pain", "Joint pain", "Muscle weakness", "Swelling in limbs"],
                "Skin": ["Rash", "Itching", "Skin discoloration", "New moles/lumps"]
            }
            
            selected_symptoms = []
            
            for category, symptoms in categories.items():
                with st.expander(f"{category} Symptoms"):
                    for symptom in symptoms:
                        if st.checkbox(symptom, key=f"symptom_{symptom}"):
                            selected_symptoms.append(symptom)
            
            if st.button("Analyze Symptoms", type="primary"):
                if selected_symptoms:
                    analysis = analyze_symptoms(selected_symptoms)
                    
                    # Save to symptom history
                    st.session_state.symptom_history.append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "symptoms": selected_symptoms,
                        "analysis": analysis
                    })
                    
                    # Display results
                    st.subheader("Analysis Results")
                    
                    if analysis['emergency']:
                        st.markdown("""
                        <div class="emergency-alert">
                            <h3>🚨 Emergency Condition Detected</h3>
                            <p>Please seek immediate medical attention</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write(f"**Potential Conditions:**")
                    for condition in analysis['conditions']:
                        st.write(f"- {condition}")
                    
                    st.write(f"**Recommendation:** {analysis['recommendation']}")
                    st.write(f"**Severity Level:** {analysis['severity']}")
                    
                    # Add general advice based on severity
                    if analysis['severity'] == "High":
                        st.error("Call emergency services or go to the nearest hospital immediately.")
                    elif analysis['severity'] == "Moderate":
                        st.warning("Schedule a doctor's appointment within 24-48 hours.")
                    else:
                        st.info("Monitor symptoms and consult a doctor if they persist beyond 3 days.")
                else:
                    st.warning("Please select at least one symptom to analyze")
    
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
        
        if st.button("Check for Anomalies", type="primary"):
            result = predict_anomalies(hr, spo2, temp)
            
            if result['is_anomaly']:
                st.markdown(f"""
                <div class="anomaly-alert">
                    <h4 style='color: #ff8080; margin-top: 0;'>⚠️ Anomaly Detected</h4>
                    <p style='font-size: 1.1rem;'>{result['message']}</p>
                    <p><b>Anomaly Score:</b> {result['score']:.2f}</p>
                    <div style='margin-top: 1rem;'>
                        <h5 style='color: #ff8080;'>🔍 Details:</h5>
                        <ul>
                            <li><b>Heart Rate:</b> {hr} bpm (Normal: 60-100)</li>
                            <li><b>SpO2:</b> {spo2}% (Normal: 95-100)</li>
                            <li><b>Temperature:</b> {temp}°C (Normal: 36.2-37.2)</li>
                        </ul>
                    </div>
                    <p style='color: #ff8080; font-weight: bold;'>
                        Please consult with a healthcare professional.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="normal-results">
                    <h4 style='color: #80ff80; margin-top: 0;'>✓ Normal Results</h4>
                    <p style='font-size: 1.1rem;'>{result['message']}</p>
                    <p><b>Health Score:</b> {result['score']:.2f}</p>
                    <div style='margin-top: 1rem;'>
                        <h5 style='color: #80ff80;'>Your Readings:</h5>
                        <ul>
                            <li><b>Heart Rate:</b> {hr} bpm</li>
                            <li><b>SpO2:</b> {spo2}%</li>
                            <li><b>Temperature:</b> {temp}°C</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
        
        # Health Trends
        st.header("Weekly Trends")
        trend_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Heart Rate': [72, 74, 71, 73, 75, 70, 68],
            'Steps': [4500, 6200, 5800, 7100, 6800, 8900, 5200],
            'Sleep (hrs)': [7.2, 6.8, 7.5, 7.0, 6.5, 8.2, 7.8]
        })
        
        tab1, tab2, tab3 = st.tabs(["Heart Rate", "Activity", "Sleep"])
        
        with tab1:
            st.line_chart(trend_data, x='Day', y='Heart Rate')
        with tab2:
            st.bar_chart(trend_data, x='Day', y='Steps')
        with tab3:
            st.area_chart(trend_data, x='Day', y='Sleep (hrs)')
    
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
            doctor = st.selectbox("Select Doctor", ["Dr. Wabuko", "Dr. Sangura", "Other Physician"])
            message = st.text_area("Your Message", height=150)
            urgency = st.select_slider("Urgency Level", ["Low", "Medium", "High", "Emergency"])
            
            if st.form_submit_button("Send Message", type="primary"):
                # Save the doctor request
                request_data = {
                    "name": st.session_state.username,
                    "email": load_users()[st.session_state.username]['email'],
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "doctor": doctor,
                    "urgency": urgency
                }
                
                # Append to existing requests
                try:
                    existing = pd.read_csv(DOCTOR_REQUESTS_FILE)
                    updated = pd.concat([existing, pd.DataFrame([request_data])], ignore_index=True)
                    updated.to_csv(DOCTOR_REQUESTS_FILE, index=False)
                except:
                    pd.DataFrame([request_data]).to_csv(DOCTOR_REQUESTS_FILE, index=False)
                
                st.success("Message sent to doctor!")
                time.sleep(1)
                st.rerun()
    
    elif st.session_state.current_page == "Symptom History":
        st.title("📋 Symptom History")
        
        if not st.session_state.symptom_history:
            st.info("No symptom history recorded yet")
        else:
            for entry in reversed(st.session_state.symptom_history):
                with st.expander(f"{entry['date']} - {len(entry['symptoms'])} symptoms"):
                    st.write("**Symptoms:**")
                    for symptom in entry['symptoms']:
                        st.write(f"- {symptom}")
                    
                    st.write("**Analysis:**")
                    st.write(f"- Conditions: {', '.join(entry['analysis']['conditions'])}")
                    st.write(f"- Recommendation: {entry['analysis']['recommendation']}")
                    st.write(f"- Severity: {entry['analysis']['severity']}")
                    
                    if entry['analysis']['emergency']:
                        st.error("This was flagged as an emergency situation")
                    elif entry['analysis']['severity'] == "Moderate":
                        st.warning("This was considered a moderate concern")
                    else:
                        st.success("This was considered a mild concern")
            
            if st.button("Clear History", type="secondary"):
                st.session_state.symptom_history = []
                st.rerun()
