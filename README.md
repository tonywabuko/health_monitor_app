# 🏥 Health Companion Pro

**AI-Powered Health Monitoring System**  
_Deployed at: [https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app](https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app)_

---

## 🌍 SDG Alignment

**Primary SDG**: SDG 3 – *Good Health and Well-being*

**Problem Addressed**:  
Limited access to timely health monitoring contributes to preventable complications and delayed interventions. Many communities lack early detection systems for non-communicable disease (NCD) indicators like abnormal heart rate, SpO₂, and body temperature.

**Solution**:  
Health Companion Pro is an AI-powered web application that enables real-time anomaly detection using vital sign inputs. Users receive actionable health insights and can immediately contact a doctor for follow-up care.

---

## ⚙️ Features

- 🔐 **User Authentication** (Sign up/Login with password hashing)
- 🧠 **AI Anomaly Detection** (Isolation Forest model trained on synthetic vital data)
- 🤖 **AI Health Chatbot** (Predefined logic for basic health advice)
- 🩺 **Symptom Checker** (Multi-select symptoms with smart suggestions)
- 📊 **Health Dashboard** (Input-based health scoring and trend analysis)
- 📞 **Contact Doctor** (Message form with data saved to CSV for offline triage)
- 🧘 **Clean UI/UX** (Custom CSS, dark mode ready, mobile responsive)

---

## 🧠 AI/ML Approach

- **Model**: Isolation Forest for unsupervised anomaly detection
- **Inputs**: Heart Rate (bpm), SpO₂ (%), Temperature (°C)
- **Output**: Binary anomaly classification with score and guidance
- **Data**: Synthetic training data with normal distributions

---

## 🛠 Tools & Tech Stack

| Category           | Tool/Framework             |
|--------------------|----------------------------|
| Frontend           | Streamlit                  |
| Machine Learning   | Scikit-learn (Isolation Forest) |
| Data Handling      | Pandas, NumPy, CSV, JSON   |
| Styling            | Custom CSS with dark mode  |
| Authentication     | SHA-256 password hashing   |
| Deployment         | Streamlit Cloud            |
| Version Control    | Git & GitHub               |

---

## 🚀 Deployment

The application is live and accessible at:  
🔗 [https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app](https://healthmonitorapp-jmvho9hf9kcqcpyhdf2amb.streamlit.app)

---

## ✅ Ethical & Sustainability Considerations

| Consideration      | Implementation                                                 |
|--------------------|----------------------------------------------------------------|
| **Bias Mitigation**     | Trained on diverse synthetic data representing typical vitals     |
| **Privacy**             | Local storage of user info (JSON/CSV); no third-party data used   |
| **Energy Efficiency**   | Lightweight ML model ensures low compute resource use             |
| **Scalability**         | Ready for deployment on low-cost infrastructure (Streamlit Cloud) |

---

## 📁 Project Structure

├── app.py # Main Streamlit application
├── model.py # Isolation Forest training and prediction
├── users.json # Registered user credentials
├── doctor_requests.csv # Contact form submissions
├── users.csv # (Optional) legacy or backup user info
├── devcontainer.json # Container settings for development
└── pages/ # Future scope: modular page splitting

yaml
Copy
Edit

---

## 👥 Authors

- **Tony Wabuko** – [tonywabuko@gmail.com](mailto:tonywabuko@gmail.com)  
- **Brian Sangura** – [sangura.bren@gmail.com](mailto:sangura.bren@gmail.com)  
- **John Kuria** – [kuria4115@gmail.com](mailto:kuria4115@gmail.com)

---

## 🧭 Future Enhancements

- 📈 Save and plot historical vital signs per user
- 🔔 Real-time alerts (SMS/Email) for abnormal readings
- 🔐 Use bcrypt or Argon2 for stronger password hashing
- 🌐 API integration with wearable devices (e.g., Fitbit, Apple Health)
- 📊 Admin dashboard for doctors to monitor incoming requests

---

## 📜 License

This project is released under the **MIT License**. You are free to use, modify, and distribute it with credit to the original authors.

---

## 🙌 Acknowledgements

- Streamlit for the intuitive frontend framework  
- scikit-learn for easy ML implementation  
- UN SDG Framework for guiding purpose-driven tech innovation

> "By blending AI and software engineering with real-world health needs, we empower users to take control of their wellness — one heartbeat at a time."
