import streamlit as st
import pandas as pd
import os
import bcrypt

st.set_page_config(page_title="AI Health Monitor", page_icon="🩺", layout="centered")

# Ensure session state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "mode" not in st.session_state:
    st.session_state.mode = "login"

def login_signup():
    st.title("🔐 Welcome to the AI Health Monitoring System")

    def switch_mode():
        st.session_state.mode = "signup" if st.session_state.mode == "login" else "login"

    st.button("🔄 Switch to Signup" if st.session_state.mode == "login" else "🔄 Switch to Login", on_click=switch_mode)

    with st.form(key="auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.session_state.mode == "signup":
            confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Login" if st.session_state.mode == "login" else "Sign Up")

        if submit:
            if os.path.exists("users.csv") and os.path.getsize("users.csv") > 0:
                existing = pd.read_csv("users.csv")
                if "email" not in existing.columns:
                    existing = pd.DataFrame(columns=["email", "password"])
            else:
                existing = pd.DataFrame(columns=["email", "password"])

            if st.session_state.mode == "signup":
                if password != confirm_password:
                    st.error("❌ Passwords do not match.")
                    return

                if email in existing["email"].values:
                    st.error("❌ Email already registered.")
                    return

                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                new_user = pd.DataFrame([[email, hashed_pw]], columns=["email", "password"])
                new_user.to_csv("users.csv", mode="a", header=not os.path.exists("users.csv"), index=False)
                st.success("✅ Signup successful! Please log in.")
                st.session_state.mode = "login"
                st.experimental_rerun()

            else:
                user = existing[existing["email"] == email]
                if not user.empty and bcrypt.checkpw(password.encode(), user["password"].values[0].encode()):
                    st.session_state.logged_in = True
                    st.success("✅ Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Invalid email or password.")

def main():
    if st.session_state.logged_in:
        # Show sidebar and redirect to health monitor
        with st.sidebar:
            st.write("📋 Navigation")
        import pages.health_monitor as health_monitor
        health_monitor.run()
    else:
        hide_sidebar_style = """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """
        st.markdown(hide_sidebar_style, unsafe_allow_html=True)
        login_signup()

if __name__ == "__main__":
    main()
