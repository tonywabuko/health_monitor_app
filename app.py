import streamlit as st
import pandas as pd
import hashlib
import os

# User data storage
USER_DATA = "users.csv"

# Initialize user data file with proper columns
def init_user_data():
    if not os.path.exists(USER_DATA):
        pd.DataFrame(columns=["username", "email", "password"]).to_csv(USER_DATA, index=False)
    else:
        # Ensure the file has the correct columns
        try:
            df = pd.read_csv(USER_DATA)
            if not all(col in df.columns for col in ["username", "email", "password"]):
                pd.DataFrame(columns=["username", "email", "password"]).to_csv(USER_DATA, index=False)
        except:
            pd.DataFrame(columns=["username", "email", "password"]).to_csv(USER_DATA, index=False)

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def login_user(username, password):
    try:
        users_df = pd.read_csv(USER_DATA)
        if not users_df.empty and 'username' in users_df.columns:
            user_match = users_df[users_df['username'] == username]
            if not user_match.empty:
                stored_password = user_match['password'].values[0]
                return check_hashes(password, stored_password)
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def create_user(username, email, password):
    try:
        users_df = pd.read_csv(USER_DATA)
        
        # Check if username exists (only if dataframe isn't empty)
        if not users_df.empty and 'username' in users_df.columns:
            if username in users_df['username'].values:
                return False, "Username already exists"
        
        # Create new user
        hashed_password = make_hashes(password)
        new_user = pd.DataFrame([[username, email, hashed_password]], 
                              columns=["username", "email", "password"])
        
        # Concatenate only if existing data is valid
        if not users_df.empty and all(col in users_df.columns for col in ["username", "email", "password"]):
            users_df = pd.concat([users_df, new_user], ignore_index=True)
        else:
            users_df = new_user
            
        users_df.to_csv(USER_DATA, index=False)
        return True, "Account created successfully!"
    except Exception as e:
        return False, f"Error creating account: {str(e)}"

def login_page():
    st.title("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username and password:
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
        st.rerun()

def signup_page():
    st.title("Sign Up")
    
    with st.form("signup_form"):
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if not (username and email and password and confirm_password):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords don't match")
            else:
                success, message = create_user(username, email, password)
                if success:
                    st.success(message)
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(message)

    if st.button("Already have an account? Sign in"):
        st.session_state.show_signup = False
        st.rerun()

def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    # Initialize user data file
    init_user_data()
    
    # Show appropriate page
    if not st.session_state.logged_in:
        if st.session_state.show_signup:
            signup_page()
        else:
            login_page()
    else:
        st.success(f"Welcome {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        # Your main app content goes here
        st.write("You are now logged in!")

if __name__ == "__main__":
    main()
