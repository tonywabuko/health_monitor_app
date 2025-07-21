import streamlit as st
import pandas as pd
from datetime import datetime
import os

DOCTOR_FILE = "doctor_requests.csv"

def run():
    st.title("👨‍⚕️ Contact a Doctor")
    st.write("If you need personalized advice, submit your query below.")

    name = st.text_input("Your Full Name")
    email = st.text_input("Email Address")
    message = st.text_area("Describe your health issue or question")

    if st.button("Submit Request"):
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

            st.success("📨 Your request has been submitted. A doctor will reach out to you soon.")
        else:
            st.warning("⚠️ Please fill out all fields.")

    st.markdown("---")
    st.subheader("📇 Contact Information")

    st.info("""
    **Dr. Tony Wabuko**  
    📞 Phone: 0799104517

    **Dr. Brian Sangura**  
    📧 Email: sangura.bren@gmail.com
    """)

    if os.path.exists(DOCTOR_FILE):
        st.markdown("### 🗂️ Previous Submissions")
        df = pd.read_csv(DOCTOR_FILE)
        st.dataframe(df.tail(10))
