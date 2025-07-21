# pages/contact_doctor.py
import streamlit as st
import pandas as pd
from datetime import datetime

DOCTOR_FILE = "doctor_requests.csv"


def run():
    st.title("👨‍⚕️ Contact a Doctor")
    st.write("If you need personalized advice, submit your query below.")

    name = st.text_input("Your Full Name")
    email = st.text_input("Email Address")
    message = st.text_area("Describe your health issue or question")

    if st.button("Submit Request"):
        if name and email and message:
            data = {
                "name": name,
                "email": email,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            df = pd.DataFrame([data])
            if not os.path.exists(DOCTOR_FILE):
                df.to_csv(DOCTOR_FILE, index=False)
            else:
                df.to_csv(DOCTOR_FILE, mode='a', header=False, index=False)
            st.success(
                "📨 Your request has been submitted. A doctor will reach out to you soon.")
        else:
            st.warning("⚠️ Please fill out all fields.")
