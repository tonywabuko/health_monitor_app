import streamlit as st
import pandas as pd
import bcrypt
import os

# Session setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

USERS_FILE = "users.csv"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_signup():
    st.title("👤 Welcome to AI-Powered Health Monitor")
    choice = st.selectbox("Login / Signup", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Sign Up"):
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
                return

            hashed_pw = hash_password(password)
            user_data = {"email": email, "password": hashed_pw}
            df = pd.DataFrame([user_data])

            if os.path.exists(USERS_FILE):
                existing = pd.read_csv(USERS_FILE)
                if email in existing['email'].values:
                    st.warning("⚠️ User already exists.")
                    return
                df = pd.concat([existing, df], ignore_index=True)

            df.to_csv(USERS_FILE, index=False)
            st.success("✅ Account created! Please log in.")

    elif choice == "Login":
        if st.button("Login"):
            if not os.path.exists(USERS_FILE):
                st.error("❌ No users found.")
                return

            users = pd.read_csv(USERS_FILE)
            user = users[users['email'] == email]

            if not user.empty and check_password(password, user.iloc[0]['password']):
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials.")

def main():
    if st.session_state.logged_in:
        # Hide sidebar menu before login
        with st.sidebar:
            st.markdown("## Navigation")
            page = st.selectbox("Choose a page", ["🏥 Monitor Vitals", "📨 Contact Doctor"])

        if page == "🏥 Monitor Vitals":
            import pages.health_monitor as health_monitor
            health_monitor.run()
        elif page == "📨 Contact Doctor":
            import pages.contact_doctor as contact_doctor
            contact_doctor.run()
    else:
        login_signup()

if __name__ == "__main__":
    main()
