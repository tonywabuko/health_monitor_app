# pages/contact_doctor.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os

DOCTOR_FILE = "doctor_requests.csv"

def run():
    st.title("👨‍⚕️ Contact a Doctor")
    st.write("Need expert health advice? Submit your issue and a doctor will get back to you promptly.")

    st.subheader("📨 Submit Your Health Concern")
    with st.form("doctor_contact_form"):
        name = st.text_input("Your Full Name")
        email = st.text_input("Email Address")
        message = st.text_area("Describe your health issue or question")

        submitted = st.form_submit_button("Submit Request")
        if submitted:
            if name and email and message:
                new_request = {
                    "name": name,
                    "email": email,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }

                new_df = pd.DataFrame([new_request])
                if not os.path.exists(DOCTOR_FILE) or os.stat(DOCTOR_FILE).st_size == 0:
                    new_df.to_csv(DOCTOR_FILE, index=False)
                else:
                    existing_df = pd.read_csv(DOCTOR_FILE)
                    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                    updated_df.to_csv(DOCTOR_FILE, index=False)

                st.success("✅ Your request has been submitted. A doctor will contact you soon.")
            else:
                st.warning("⚠️ Please fill in all fields.")

    st.markdown("---")

    st.subheader("📇 Doctor Contact Information")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Dr. Tony Wabuko**")
        st.markdown("- 📞 Phone: 0799104517")
        st.markdown("- 📧 Email: tonywabuko@gmail.com")

    with col2:
        st.markdown("**Dr. Brian Sangura**")
        st.markdown("- 📧 Email: sangura.bren@gmail.com")
        st.markdown("- 🕒 Available: Mon - Fri, 9AM to 5PM")

    st.markdown("---")
    st.info("We value your privacy. All data submitted is confidential and used solely for medical follow-up.")
