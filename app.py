import streamlit as st
import pandas as pd
import bcrypt
import os

# File path
USER_FILE = "users.csv"

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def load_users():
    if not os.path.exists(USER_FILE):
        return pd.DataFrame(columns=["username", "password"])
    return pd.read_csv(USER_FILE)

def save_user(username, hashed_password):
    df = load_users()
    df = pd.concat([df, pd.DataFrame([{"username": username, "password": hashed_password}])], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

def login(username, password):
    df = load_users()
    user = df[df['username'] == username]
    if not user.empty:
        stored_hashed = user.iloc[0]["password"].encode()
        return bcrypt.checkpw(password.encode(), stored_hashed)
    return False

def signup(username, password):
    df = load_users()
    if username in df["username"].values:
        return False
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    save_user(username, hashed_pw)
    return True

def login_signup():
    st.title("🔐 Welcome to AI Health Monitor")
    option = st.radio("Choose an option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.authenticated = True
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials.")
    else:
        if st.button("Sign Up"):
            if signup(username, password):
                st.success("✅ Account created. Please log in.")
            else:
                st.error("❌ Username already exists.")

def main():
    if not st.session_state.authenticated:
        login_signup()
    else:
        from pages import health_monitor as hm
        hm.run()

        from pages import contact_doctor as cd
        cd.run()

if __name__ == "__main__":
    main()
