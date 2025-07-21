import streamlit as st
import pandas as pd
import bcrypt
from pathlib import Path
from health_monitor import show_health_monitor
from contact_doctor import show_contact_doctor

# Constants
USER_FILE = "users.csv"
SESSION_KEY = "logged_in"

# Initialize users file if not present
def init_user_file():
    if not Path(USER_FILE).exists():
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Validate user
def validate_user(username, password):
    if not Path(USER_FILE).exists():
        return False
    users = pd.read_csv(USER_FILE)
    user = users[users["username"] == username]
    if not user.empty:
        return verify_password(password, user.iloc[0]["password"])
    return False

# Add new user
def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users["username"].values:
        return False  # User exists
    hashed = hash_password(password).decode()
    new_user = pd.DataFrame([{"username": username, "password": hashed}])
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_csv(USER_FILE, index=False)
    return True

# Login/Signup Page
def login_page():
    st.title("Welcome to Health Monitor App")
    st.subheader("Login or Sign Up to Continue")

    option = st.radio("Choose an option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if option == "Login":
            if validate_user(username, password):
                st.session_state[SESSION_KEY] = True
                st.session_state["username"] = username
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")
        else:
            if add_user(username, password):
                st.success("✅ Account created successfully! Please log in.")
            else:
                st.error("❌ Username already exists.")

# Main App Navigator
def main():
    init_user_file()

    if SESSION_KEY not in st.session_state or not st.session_state[SESSION_KEY]:
        login_page()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        selection = st.sidebar.radio("Navigation", ["Health Monitor", "Contact Doctor"])

        if selection == "Health Monitor":
            show_health_monitor()
        elif selection == "Contact Doctor":
            show_contact_doctor()

if __name__ == "__main__":
    main()
