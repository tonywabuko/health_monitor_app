import streamlit as st
import pandas as pd
import bcrypt
from pathlib import Path

# Constants
USER_FILE = "users.csv"
SESSION_KEY = "logged_in"

# Initialize user file
def init_user_file():
    if not Path(USER_FILE).exists():
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)

# Hashing and verification
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# User validation
def validate_user(username, password):
    if not Path(USER_FILE).exists():
        return False
    users = pd.read_csv(USER_FILE)
    user = users[users["username"] == username]
    if not user.empty:
        return verify_password(password, user.iloc[0]["password"])
    return False

# Add user
def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        return False
    hashed = hash_password(password).decode()
    new_user = pd.DataFrame([{"username": username, "password": hashed}])
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_csv(USER_FILE, index=False)
    return True

# Login/Signup Page
def login_page():
    st.title("🩺 AI-Powered Health Monitor")
    st.subheader("Please log in or sign up to continue.")

    option = st.radio("Choose an option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if option == "Login":
            if validate_user(username, password):
                st.session_state[SESSION_KEY] = True
                st.session_state["username"] = username
                st.success("✅ Logged in successfully!")
                st.switch_page("pages/1_health_monitor.py")  # redirect to Health Monitor
            else:
                st.error("❌ Invalid username or password.")
        else:
            if add_user(username, password):
                st.success("✅ Account created successfully! Please log in.")
            else:
                st.error("❌ Username already exists.")

# Run
def main():
    init_user_file()

    if SESSION_KEY not in st.session_state or not st.session_state[SESSION_KEY]:
        login_page()
    else:
        st.switch_page("pages/1_health_monitor.py")

if __name__ == "__main__":
    main()
