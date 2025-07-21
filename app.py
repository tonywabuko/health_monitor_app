# app.py
import streamlit as st
import pandas as pd
import os

USER_FILE = "users.csv"

# Initialize user database
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# Authentication functions
def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users['username'].values:
        return False
    users = users.append({"username": username, "password": password}, ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

def validate_user(username, password):
    users = pd.read_csv(USER_FILE)
    return any((users['username'] == username) & (users['password'] == password))

# Login/Signup UI
def login_signup():
    st.title("🔐 Welcome to AI Health Monitor")
    choice = st.selectbox("Choose an option", ["Login", "Sign Up"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if validate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials.")
    else:
        if st.button("Sign Up"):
            if add_user(username, password):
                st.success("✅ Account created. You can now log in.")
            else:
                st.warning("⚠️ Username already exists.")

# App router
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_signup()
    else:
        st.sidebar.title(f"👤 Welcome, {st.session_state['username']}")
        page = st.sidebar.selectbox("Navigate", ["Health Monitor", "Contact Doctor", "Logout"])
        if page == "Health Monitor":
            import pages.health_monitor as health_monitor
            health_monitor.run()
        elif page == "Contact Doctor":
            import pages.contact_doctor as contact_doctor
            contact_doctor.run()
        elif page == "Logout":
            st.session_state["logged_in"] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
