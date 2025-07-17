# 🩺 AI-Powered Health Monitoring System

**Live App**: [https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app/](https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app/)

## 📌 Overview

This project leverages artificial intelligence to monitor users' health using data from wearable devices. It detects anomalies in vital signs like heart rate and blood oxygen levels, provides personalized health insights, and facilitates medical consultations.

## 🔑 Key Features

- 📊 **Real-time Health Monitoring**: Uses simulated or wearable device data (e.g., heart rate, SpO₂).
- 🚨 **Anomaly Detection**: Identifies abnormal patterns using a trained Isolation Forest model.
- 🧠 **Personalized Recommendations**: Advises users based on current health metrics.
- 📥 **Doctor Contact Form**: Users can contact doctors directly via a built-in form.
- 📝 **Data Logging**: Saves doctor requests to a CSV file (`doctor_requests.csv`) for follow-up.

## ⚙️ Technologies Used

- **Python**
- **Streamlit** – Web app interface
- **Pandas, NumPy** – Data manipulation
- **Scikit-learn** – Anomaly detection model (Isolation Forest)
- **CSV** – Persistent local storage of user contact requests
- **GitHub + Streamlit Cloud** – Deployment

## 📁 Project Structure

health_monitor_app/
│
├── app.py # Main Streamlit app
├── model.py # ML model training (runs once on deployment)
├── healthdata.py # Simulated health data generator
├── doctor_requests.csv # Stores doctor consultation requests
├── requirements.txt # App dependencies
├── README.md # Project documentation
└── pycache/ # Python cache files (ignored)

markdown
Copy
Edit

## 🧪 How It Works

1. **User opens the app** → Inputs health data (simulated or real).
2. **Model processes input** → Detects anomalies using Isolation Forest.
3. **Output displayed** → Shows health status and recommendations.
4. **User fills contact form (optional)** → Stored in `doctor_requests.csv`.

## 👨‍⚕️ Doctor Contact Info

Users can reach out to the doctors below directly from the app:

- **Tony Wabuko** – [tonywabuko@gmail.com](mailto:tonywabuko@gmail.com)
- **Brian Sangura** – [sangura.bren@gmail.com](mailto:sangura.bren@gmail.com)

## 🧑‍💻 Contributors

- **Tony Wabuko** – AI Lead, Developer  
- **Brian Sangura** – Data Scientist  Developer
- **John Kuria** – Developer Frontend Integration & QA

## 🚀 Setup Instructions (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/tonywabuko/health_monitor_app.git
   cd health_monitor_app
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
streamlit run app.py
⚠️ Make sure doctor_requests.csv exists in the root folder. If not, create it manually with headers: Name,Email,Message.

📈 Model Retraining
The anomaly detection model is retrained automatically upon deployment using model.py. This avoids pickle incompatibility issues.

🧩 Future Improvements
Integration with real wearable APIs (e.g., Fitbit, Garmin)

Authentication and user profiles

Cloud database for persistent storage

SMS/Email alerts to doctors

✅ Project Status
🟢 Live and functional
Last updated: July 2025
Deployed on Streamlit Cloud

This project was built as part of the AI for Software Engineering course and demonstrates a real-world AI application for public health.
