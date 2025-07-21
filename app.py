import streamlit as st
import pandas as pd
import hashlib
import os

# File path for storing user info
USER_FILE = "users.csv"

# Ensure users.csv exists
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# Add new user
def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        return False  # Username taken
    hashed = hash_password(password)
    users = pd.concat([users, pd.DataFrame([{"username": username, "password": hashed}])], ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

# Authenticate user
def login_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        stored_hashed = users[users["username"] == username]["password"].values[0]
        return verify_password(password, stored_hashed)
    return False

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# UI
def login_signup():
    st.title("🏥 Welcome to the AI Health Monitoring App")
    st.subheader("Please log in or sign up to continue")

    choice = st.radio("Choose an option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.success("✅ Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")
    else:
        if st.button("Sign Up"):
            if add_user(username, password):
                st.success("✅ Account created! Please log in.")
            else:
                st.warning("⚠️ Username already taken")

# Main
def main():
    if not st.session_state.logged_in:
        login_signup()
        st.stop()

    # Show sidebar nav only if logged in
    st.sidebar.title(f"👋 Hello, {st.session_state.username}")
    page = st.sidebar.radio("Navigation", ["Health Monitor", "Contact Doctor"])

    if page == "Health Monitor":
        from pages import 1_health_monitor as health_monitor
        health_monitor.run()
    elif page == "Contact Doctor":
        from pages import 2_contact_doctor as contact_doctor
        contact_doctor.run()

if __name__ == "__main__":
    main()
