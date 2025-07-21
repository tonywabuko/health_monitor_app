import streamlit as st
import pandas as pd
import os
import bcrypt

USER_FILE = "users.csv"

# Ensure users.csv exists and has correct headers
if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# Hash the password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Check hashed password
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Add new user with hashed password
def add_user(username, password):
    users = pd.read_csv(USER_FILE)
    if username in users['username'].values:
        return False
    hashed_password = hash_password(password)
    new_user = pd.DataFrame([{"username": username, "password": hashed_password}])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_FILE, index=False)
    return True

# Validate login with hashed password
def validate_user(username, password):
    try:
        users = pd.read_csv(USER_FILE)
    except pd.errors.EmptyDataError:
        return False

    if username not in users['username'].values:
        return False

    stored_hashed_pw = users[users['username'] == username]['password'].values[0]
    return check_password(password, stored_hashed_pw)

# Login/signup form
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
                st.session_state["page"] = "Health Monitor"
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Invalid credentials.")
    else:
        if st.button("Sign Up"):
            if add_user(username, password):
                st.success("✅ Account created. You can now log in.")
            else:
                st.warning("⚠️ Username already exists.")

# Main app logic
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

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
            st.session_state["page"] = "Login"
            st.success("👋 You have been logged out.")

if __name__ == "__main__":
    main()
