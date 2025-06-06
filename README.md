
# 🏥 Medical Diagnosis & Appointment System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/UI-Streamlit-orange)](https://streamlit.io/)
[![Gemini API](https://img.shields.io/badge/AI-Google_Gemini-blueviolet)](https://ai.google.dev/)

A comprehensive AI-powered platform that assists with medical diagnosis, treatment recommendations, specialist referrals, and appointment coordination — all through conversational AI and intelligent agents.

🎥 [**Watch Demo Video**](https://vimeo.com/1091245465?share=copy#t=0)

---

## ✨ Features

- 🧠 **Symptom Analyzer** – Uses LLMs to assess user-reported symptoms.
- 💊 **Treatment Advisor** – Recommends medicine and lifestyle changes.
- 👨‍⚕️ **Specialist Referral** – Matches patients with appropriate medical specialists.
- 📅 **Appointment Coordinator** – Generates email templates for scheduling with doctors.

---

## 🛠️ Tech Stack

| Layer      | Technologies                               |
|------------|--------------------------------------------|
| Frontend   | Streamlit                                  |
| Backend    | Python, [CrewAI](https://docs.crewai.com/), [Gemini API](https://ai.google.dev) |
| Agents     | Diagnostician, Treatment Advisor, Specialist Referral, Appointment Coordinator |
| Tools/APIs | Serper (search), Gemini (generation)       |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/gautax/medical-ai-app-with-agents.git
cd medical-ai-app-with-agents

2️⃣ Create and Activate Virtual Environment (Recommended)

python -m venv venv
# For Linux/macOS
source venv/bin/activate
# For Windows
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set Up API Keys
Create a .env file in the root directory:

touch .env
Paste the following content and replace with your actual keys:

GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
If you don't have the keys yet:

🔑 Get a Gemini API key

🔍 Get a Serper API key

5️⃣ Run the App

streamlit run interface/streamlit_app.py
Visit the running app at: http://localhost:8501

📁 Project Structure

medical-diagnosis-app/
├── agents/                # CrewAI agents
│   ├── diagnostician.py
│   ├── treatment_advisor.py
│   ├── specialist_referral.py
│   └── appointment_coordinator.py
│
├── crew/                  # Crew definitions
│   ├── medical_crew.py
│   └── appointment_crew.py
│
├── interface/             # Streamlit frontend interface
│   └── streamlit_app.py
│
├── tasks/                 # Task logic (optional/expandable)
├── utils/                 # Helper functions and configs
├── .env                   # API keys and secrets
├── main.py                # Optional main controller
├── requirements.txt       # Dependencies
├── setup.py               # Package setup file
└── README.md              # Project documentation

🧪 Testing
To test specific components manually:

# Run the main orchestrator
python main.py
Or call specific agent modules from the terminal or test files.

📝 License
This project is licensed under the MIT License.
See the LICENSE file for more details.

🤝 Contributing
Contributions are welcome! Please follow the steps below:

Fork the repository.

Create your feature branch:

git checkout -b feature/amazing-feature
Commit your changes:

git commit -m "Add amazing feature"
Push to the branch:

git push origin feature/amazing-feature
Open a Pull Request.

📬 Contact
For issues, ideas, or improvements — feel free to open an issue or reach out via LinkedIn.

Built with ❤️ using AI to enhance medical workflows and accessibility.
