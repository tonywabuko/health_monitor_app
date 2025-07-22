import streamlit as st
import pandas as pd
import hashlib
import os

# User data storage
USER_DATA = "users.csv"

# Initialize user data file
if not os.path.exists(USER_DATA):
    pd.DataFrame(columns=["username", "email", "password"]).to_csv(USER_DATA, index=False)

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def login_user(username, password):
    users_df = pd.read_csv(USER_DATA)
    if username in users_df['username'].values:
        stored_password = users_df.loc[users_df['username'] == username, 'password'].values[0]
        return check_hashes(password, stored_password)
    return False

def create_user(username, email, password):
    users_df = pd.read_csv(USER_DATA)
    if username in users_df['username'].values:
        return False
    hashed_password = make_hashes(password)
    new_user = pd.DataFrame([[username, email, hashed_password]], 
                           columns=["username", "email", "password"])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv(USER_DATA, index=False)
    return True

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    
    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
        st.experimental_rerun()

def signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Create Account"):
        if password != confirm_password:
            st.error("Passwords don't match")
        elif create_user(username, email, password):
            st.success("Account created successfully! Please log in.")
            st.session_state.show_signup = False
            st.experimental_rerun()
        else:
            st.error("Username already exists")
    
    if st.button("Already have an account? Sign in"):
        st.session_state.show_signup = False
        st.experimental_rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    if not st.session_state.logged_in:
        if st.session_state.show_signup:
            signup_page()
        else:
            login_page()
    else:
        st.success(f"Welcome {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()
        # Your main app content goes here

if __name__ == "__main__":
    main()
