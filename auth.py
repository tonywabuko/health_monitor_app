from db_utils import create_user, verify_user
import streamlit as st

def auth_page():
    st.title("🔐 HealthGuard Authentication")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pw")
            
            if st.form_submit_button("Login"):
                user = verify_user(email, password)
                if user:
                    st.session_state['user'] = user
                    st.session_state['authenticated'] = True
                    st.success(f"Welcome back {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_pw = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Create Account"):
                if password != confirm_pw:
                    st.error("Passwords don't match!")
                elif create_user(name, email, password):
                    st.success("Account created! Please login.")
                else:
                    st.error("Email already exists")
