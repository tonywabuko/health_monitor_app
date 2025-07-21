import streamlit as st
import pandas as pd
import os

USER_FILE = "users.csv"

# Ensure user CSV exists and has headers
if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users['username'].values:
        return False

    new_user = pd.DataFrame([{"username": username, "password": password}])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

def validate_user(username, password):
    try:
        users = pd.read_csv(USER_FILE)
    except pd.errors.EmptyDataError:
        return False

    return any((users['username'] == username) & (users['password'] == password))

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
