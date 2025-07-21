import streamlit as st
import pandas as pd
import bcrypt
from model import train_and_save_model, load_model
import os

# Constants
USER_CSV = "users.csv"
MODEL_FILE = "anomaly.pkl"

st.set_page_config(page_title="Health Monitor", layout="wide")

# --- Utility Functions ---

def load_users():
    if not os.path.exists(USER_CSV):
        return pd.DataFrame(columns=["email", "password"])
    return pd.read_csv(USER_CSV)

def save_user(email, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    df = pd.DataFrame([[email, hashed_pw]], columns=["email", "password"])
    df.to_csv(USER_CSV, mode="a", index=False, header=not os.path.exists(USER_CSV))

def verify_user(email, password):
    users = load_users()
    if email in users["email"].values:
        stored_pw = users.loc[users["email"] == email, "password"].values[0]
        return bcrypt.checkpw(password.encode(), stored_pw.encode())
    return False

def retrain_model_if_needed():
    import numpy as np
    import pandas as pd
    if not os.path.exists(MODEL_FILE):
        sample_data = pd.DataFrame(
            np.random.normal(loc=[80, 98, 36.8, 16], scale=[10, 1, 0.4, 2], size=(100, 4)),
            columns=["heart_rate", "spo2", "temperature", "respiration_rate"]
        )
      train_and_save_model()


# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login / Signup Interface ---
def login_signup():
    st.title("🔐 Welcome to AI-Powered Health Monitor")
    option = st.radio("Choose an option", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if verify_user(email, password):
                st.success("✅ Login successful!")
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("❌ Incorrect email or password.")
    else:
        if st.button("Sign Up"):
            users = load_users()
            if email in users["email"].values:
                st.warning("⚠️ Email already registered. Please log in.")
            else:
                save_user(email, password)
                st.success("🎉 Account created. You can now log in.")
                st.experimental_rerun()

# --- Main App Logic ---
def main():
    retrain_model_if_needed()

    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Go to", ["Vitals Monitor", "Contact Doctor"])

        if page == "Vitals Monitor":
            import pages.health_monitor as health_monitor
            health_monitor.run()
        elif page == "Contact Doctor":
            import pages.contact_doctor as contact_doctor
            contact_doctor.run()
    else:
        login_signup()

# --- Run App ---
if __name__ == "__main__":
    main()
