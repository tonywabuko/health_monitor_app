import streamlit as st
import pandas as pd
import hashlib
import os

USER_FILE = "users.csv"

# --- Utilities ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
        return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["username", "password"])

def save_users(users):
    users.to_csv(USER_FILE, index=False)

def validate_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return any((users['username'] == username) & (users['password'] == hashed))

def add_user(username, password):
    users = load_users()
    if username in users['username'].values:
        return False
    hashed = hash_password(password)
    users = pd.concat([users, pd.DataFrame([{"username": username, "password": hashed}])], ignore_index=True)
    save_users(users)
    return True

# --- UI Pages ---
def login_signup():
    st.title("🩺 Welcome to the AI Health Monitoring System")

    page = st.radio("Choose an option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if page == "Login":
        if st.button("Login"):
            if validate_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
                st.switch_page("pages/health_monitor.py")
            else:
                st.error("❌ Invalid credentials. Try again.")
    else:
        if st.button("Sign Up"):
            if add_user(username, password):
                st.success("✅ Account created. You can now log in.")
            else:
                st.warning("⚠️ Username already exists.")

# --- Main Logic ---
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_signup()
    else:
        st.switch_page("pages/health_monitor.py")

if __name__ == "__main__":
    main()
