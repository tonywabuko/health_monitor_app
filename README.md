# 🩺 AI-Powered Health Monitoring System

An intelligent, Streamlit-based web application that uses real-time health data (heart rate, oxygen levels, temperature) to detect anomalies and provide personalized recommendations. It also allows users to reach out to doctors for consultation.

📍 **Live Demo**: [healthmonitorapp.streamlit.app](https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app/)

---

## 🚀 Features

- 🔍 **Anomaly Detection**: Uses an Isolation Forest model to flag abnormal health metrics.
- 📊 **Real-time Visualization**: Interactive charts for health data trends.
- 📝 **Doctor Contact Form**: Users can reach out to available doctors.
- 📁 **CSV Logging**: Doctor requests are saved to `doctor_requests.csv` for easy access.
- 🔁 **Retrains Model on Deployment**: Model training occurs dynamically during app startup.

---

## 🧠 How It Works

1. **Model Training**
   - On deployment, the app trains an Isolation Forest model using sample health metrics.
   - The model detects outliers (anomalies) in user-input data.

2. **Health Metric Input**
   - Users manually enter their vitals: heart rate, SpO2, and temperature.

3. **Anomaly Result**
   - The app flags whether the input values are within normal range or potentially concerning.

4. **Contact a Doctor**
   - Users can submit their name, email, and message to consult a doctor.
   - Submissions are stored in `doctor_requests.csv`.

---

## 👨‍⚕️ Contactable Doctors

| Name           | Email                   |
|----------------|-------------------------|
| Tony Wabuko    | tonywabuko@gmail.com    |
| Brian Sangura  | sangura.bren@gmail.com  |

---

## 📂 Project Structure

health_monitor_app/
│
├── app.py # Streamlit app interface
├── model.py # Isolation Forest training logic
├── health_data.py # Simulated health data generator
├── doctor_requests.csv # Stores doctor contact form submissions
├── requirements.txt # Python package dependencies
├── .gitignore # Git ignored files
└── README.md # Project documentation

yaml
Copy
Edit

---

## ✅ Setup Instructions

To run locally:

```bash
# Clone the repository
git clone https://github.com/tonywabuko/health_monitor_app.git
cd health_monitor_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
⚠️ Notes
The app uses mock data for demonstration purposes.

You may customize the data or connect with real-time IoT devices.

Anomaly model is retrained on every deployment to avoid serialization issues with cloud environments.

📃 License
This project is open-source under the MIT License.

🙌 Contributors
Tony Wabuko – tonywabuko@gmail.com 

Brian Sangura – sangura.bren@gmail.com

John Kuria - kuria4115@gmail.com

Feel free to contribute, give feedback, or fork the project!

yaml
Copy
Edit

---

