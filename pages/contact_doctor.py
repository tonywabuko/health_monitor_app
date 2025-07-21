import streamlit as st
import pandas as pd
from datetime import datetime
import os

DOCTOR_FILE = "doctor_requests.csv"

def run():
    st.title("📨 Contact a Doctor")
    st.write("Need help? Submit your health concern.")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    message = st.text_area("Describe your health issue")

    if st.button("Submit Request"):
        if name and email and message:
            new_request = {
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }

            df = pd.DataFrame([new_request])
            if not os.path.exists(DOCTOR_FILE) or os.stat(DOCTOR_FILE).st_size == 0:
                df.to_csv(DOCTOR_FILE, index=False)
            else:
                existing = pd.read_csv(DOCTOR_FILE)
                updated = pd.concat([existing, df], ignore_index=True)
                updated.to_csv(DOCTOR_FILE, index=False)

            st.success("✅ Request submitted! A doctor will contact you soon.")
        else:
            st.warning("⚠️ Please fill out all fields.")

    st.markdown("---")
    st.subheader("📞 Available Doctors")
    st.markdown("**Tony Wabuko** – 0799104517  \n**Brian Sangura** – sangura.bren@gmail.com")
