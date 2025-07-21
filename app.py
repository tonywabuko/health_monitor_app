import streamlit as st
import pandas as pd
import bcrypt
import os
from model import train_and_save_model

# Ensure the model is trained on first run
def retrain_model_if_needed():
    if not os.path.exists("anomaly.pkl"):
        train_and_save_model()

retrain_model_if_needed()

USERS_CSV = "users.csv"
st.set_page_config(page_title="AI Health Monitor", page_icon="🩺", layout="centered")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_signup():
    st.title("🔐 Welcome to AI Health Monitoring System")
    choice = st.radio("Login or Signup", ["Login", "Signup"], horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if os.path.exists(USERS_CSV):
                users = pd.read_csv(USERS_CSV)
            else:
                users = pd.DataFrame(columns=["email", "password"])
            if email in users["email"].values:
                st.warning("Email already registered. Please log in.")
            else:
                hashed_pw = hash_password(password)
                new_user = pd.DataFrame([[email, hashed_pw]], columns=["email", "password"])
                users = pd.concat([users, new_user], ignore_index=True)
                users.to_csv(USERS_CSV, index=False)
                st.success("Account created! Please log in.")

    elif choice == "Login":
        if st.button("Log In"):
            if os.path.exists(USERS_CSV):
                users = pd.read_csv(USERS_CSV)
                if email in users["email"].values:
                    hashed = users.loc[users["email"] == email, "password"].values[0]
                    if verify_password(password, hashed):
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("User not found.")
            else:
                st.error("No users registered yet.")

def main():
    if st.session_state.logged_in:
        import pages.health_monitor as health_monitor
        health_monitor.run()
    else:
        login_signup()

if __name__ == "__main__":
    main()
