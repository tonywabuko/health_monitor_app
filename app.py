import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import json
import os
import time

# Constants and Config
USER_DB_FILE = "users.json"
DOCTOR_REQUESTS_FILE = "doctor_requests.csv"
NORMAL_RANGES = {
    "heart_rate": (60, 100),
    "spO2": (95, 100),
    "temperature": (36.2, 37.2),
    "resp_rate": (12, 20),
    "blood_pressure": (90, 120),
    "blood_pressure_dia": (60, 80)
}

# Initialize user database
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'w') as f:
        json.dump({}, f)

# Initialize doctor requests file
if not os.path.exists(DOCTOR_REQUESTS_FILE):
    pd.DataFrame(columns=["name", "email", "message", "timestamp"]).to_csv(DOCTOR_REQUESTS_FILE, index=False)

# Page Config
st.set_page_config(
    page_title="Health Companion Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .progress-container {
        height: 20px;
        background-color: #e0e0e0;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background-color: #4caf50;
        text-align: center;
        color: white;
        font-size: 12px;
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
        'health_data': {
            'last_checkup': None,
            'medications': [],
            'allergies': [],
            'conditions': []
        }
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

# Health Analysis Functions
def generate_health_response(prompt):
    """Simulate AI health assistant responses"""
    prompt = prompt.lower()
    
    if any(word in prompt for word in ["headache", "migraine"]):
        return """**Possible causes:** Tension, dehydration, or eyestrain.  
**Recommendations:**  
- Drink water  
- Rest in a quiet, dark room  
- Consider over-the-counter pain relief  
⚠️ Seek medical help if severe or persistent"""
    
    elif any(word in prompt for word in ["fever", "temperature"]):
        return """**Care advice:**  
- Stay hydrated  
- Rest  
- Use fever-reducing medication if needed  
⚠️ Contact doctor if fever > 39°C or lasts >3 days"""
    
    elif "heart" in prompt:
        return """**Important:**  
Chest pain or palpitations require immediate medical attention.  
For general heart health:  
- Maintain healthy diet  
- Regular exercise  
- Monitor blood pressure"""
    
    else:
        return """I'm your AI health assistant. For accurate medical advice, please consult with a healthcare professional.  
I can help with general health information about:  
- Common symptoms  
- Healthy living tips  
- Medication questions"""

def analyze_symptoms(symptoms):
    """Basic symptom analysis"""
    symptoms = [s.lower() for s in symptoms]
    conditions = []
    emergency = False
    
    if "chest pain" in symptoms or "shortness of breath" in symptoms:
        conditions.append("Possible cardiac issue")
        emergency = True
    if "fever" in symptoms and "cough" in symptoms:
        conditions.append("Respiratory infection")
    if "dizziness" in symptoms and "nausea" in symptoms:
        conditions.append("Possible vertigo or migraine")
    if "fatigue" in symptoms and "muscle aches" in symptoms:
        conditions.append("Viral infection")
    
    if not conditions:
        conditions.append("General illness")
    
    recommendation = "Rest and monitor symptoms" if not emergency else "Seek immediate medical care"
    
    return {
        "conditions": conditions,
        "recommendation": recommendation,
        "emergency": emergency
    }

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.show_signup = False
    st.session_state.current_page = "Health Monitor"
    st.session_state.username = None

# Authentication Pages
if not st.session_state.logged_in:
    st.title("Health Companion Pro")
    
    if st.session_state.show_signup:
        # Signup Form
        with st.container():
            st.header("Create Account")
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                submitted = st.form_submit_button("Sign Up")
                if submitted:
                    if not all([username, email, password, confirm_password]):
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        success, message = register_user(username, email, password)
                        if success:
                            st.success(message)
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error(message)
            
            if st.button("Already have an account? Login"):
                st.session_state.show_signup = False
                st.rerun()
    else:
        # Login Form
        with st.container():
            st.header("Login")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                submitted = st.form_submit_button("Login")
                if submitted:
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
else:
    # Main App Navigation
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.username}!")
        st.selectbox(
            "Navigation",
            ["Health Monitor", "Dashboard", "Contact Doctor"],
            key="page_selector",
            index=["Health Monitor", "Dashboard", "Contact Doctor"].index(st.session_state.current_page)
        )
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    # Update current page from sidebar
    st.session_state.current_page = st.session_state.page_selector
    
    # Page Routing
    if st.session_state.current_page == "Health Monitor":
        st.title("🤖 AI Health Assistant")
        
        # Health Assessment Chatbot
        with st.expander("💬 Talk to Health Assistant", expanded=True):
            if "health_chat" not in st.session_state:
                st.session_state.health_chat = []
            
            for message in st.session_state.health_chat:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            if prompt := st.chat_input("Ask me anything about your health..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.health_chat.append({"role": "user", "content": prompt})
                
                # Simulate AI response
                with st.chat_message("assistant"):
                    response = generate_health_response(prompt)
                    st.markdown(response)
                    st.session_state.health_chat.append({"role": "assistant", "content": response})
        
        # Symptom Checker
        with st.expander("🩺 Symptom Checker"):
            symptoms = st.multiselect(
                "Select your symptoms",
                ["Fever", "Cough", "Headache", "Fatigue", "Shortness of breath", 
                 "Chest pain", "Dizziness", "Nausea", "Muscle aches"]
            )
            
            if st.button("Analyze Symptoms"):
                if symptoms:
                    analysis = analyze_symptoms(symptoms)
                    st.markdown(f"**Possible conditions:** {', '.join(analysis['conditions'])}")
                    st.markdown(f"**Recommended actions:** {analysis['recommendation']}")
                    if analysis['emergency']:
                        st.error("⚠️ Seek immediate medical attention!")
                else:
                    st.warning("Please select at least one symptom")
        
        # Health Tips
        with st.expander("💡 Daily Health Tips"):
            tips = [
                "Stay hydrated - drink at least 8 glasses of water daily",
                "Get 7-9 hours of quality sleep each night",
                "Take a 5-minute break every hour if you sit for long periods",
                "Practice deep breathing for 5 minutes daily to reduce stress",
                "Include colorful vegetables in every meal"
            ]
            st.markdown(f"**Today's Tip:**\n\n{tips[datetime.now().day % len(tips)]}")
            if st.button("Get Another Tip"):
                st.rerun()
    
    elif st.session_state.current_page == "Dashboard":
        st.title("📊 Health Dashboard")
        
        # Health Metrics
        cols = st.columns(3)
        with cols[0]:
            st.metric("Heart Rate", "72 bpm", "-2 bpm from yesterday")
        with cols[1]:
            st.metric("Blood Oxygen", "98%", "Normal")
        with cols[2]:
            st.metric("Sleep", "7.2 hrs", "+0.5 hrs from avg")
        
        # Health Trends
        st.subheader("Weekly Trends")
        trend_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Heart Rate': [72, 74, 71, 73, 75, 70, 68],
            'Steps': [4500, 6200, 5800, 7100, 6800, 8900, 5200],
            'Sleep Hours': [6.5, 7.2, 6.8, 7.5, 7.0, 8.2, 7.8]
        })
        st.line_chart(trend_data.set_index('Day'))
        
        # Health Goals
        st.subheader("Your Goals")
        goal = st.selectbox("Select Goal", ["Weight Loss", "Better Sleep", "Increase Activity", "Reduce Stress"])
        current = st.slider("Current Progress (%)", 0, 100, 30)
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {current}%">{current}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Medication Tracker
        st.subheader("💊 Medication Tracker")
        meds = st.multiselect("Today's Medications", ["Metformin", "Lisinopril", "Atorvastatin", "Vitamin D"])
        if st.button("Mark as Taken"):
            st.success("Medications recorded for today!")
    
    elif st.session_state.current_page == "Contact Doctor":
        st.title("👨‍⚕️ Contact a Doctor")
        
        # Doctor Directory
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
        
        # Contact Form
        st.subheader("📩 Send Message")
        with st.form("contact_form"):
            doctor = st.selectbox("Select Doctor", ["Dr. Tony Wabuko", "Dr. Brian Sangura"])
            subject = st.text_input("Subject")
            message = st.text_area("Your Message")
            
            submitted = st.form_submit_button("Send Message")
            if submitted:
                if not all([subject, message]):
                    st.error("Please fill all fields")
                else:
                    try:
                        new_request = pd.DataFrame([{
                            "name": st.session_state.username,
                            "email": load_users()[st.session_state.username]['email'],
                            "message": f"To: {doctor}\nSubject: {subject}\n\n{message}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }])
                        
                        existing = pd.read_csv(DOCTOR_REQUESTS_FILE)
                        updated = pd.concat([existing, new_request], ignore_index=True)
                        updated.to_csv(DOCTOR_REQUESTS_FILE, index=False)
                        
                        st.success("Message sent successfully! The doctor will respond within 24 hours.")
                    except Exception as e:
                        st.error(f"Error sending message: {str(e)}")

if __name__ == "__main__":
    pass
