# Mail Automater 📨🤖

An automated cold emailing and scheduling system designed to optimize outreach workflows. This tool streamlines the process of sending personalized emails, managing custom resumes or templates tailored for specific roles (like Product Management), tracking communications via an interactive dashboard, and handling follow-up schedules automatically.

🔗 **Live Application:** [mailautomater-6.streamlit.app](https://mailautomater-6.streamlit.app/)  
📂 **Repository:** [Nishita6/mail_automater](https://github.com/Nishita6/mail_automater)

---

## 🚀 Features
* **Automated Cold Outreach:** Efficiently bulk-sends personalized emails using dynamic templates.
* **Role-Specific Targeting:** Easily swap templates and attachments tailored for specific career tracks (e.g., PM, data, analyst roles).
* **Interactive Monitoring Dashboard:** Visualizes outreach progress, email success metrics, and queue status in real time.
* **Smart Follow-up Scheduler:** Automatically tracks and schedules timely follow-ups for unreplied threads to maximize response rates.
* **Local Database Storage:** Persists contact lists, logs, and schedule pipelines securely via a localized SQL database setup.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 🐍
* **Frontend/Dashboard:** Streamlit (for `dashboard.py` / `app.py`)
* **Database:** SQLite / Local SQL execution 
* **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
├── data/                           # Contact lists, recipient configurations, and logs
├── modules/                        # Core application modules (email handling, logic pipelines)
├── resumes/                        # Target resumes/CVs to attach dynamically
├── templates/                      # Personalized email bodies (e.g., tailored for PM roles)
├── .gitignore                      # Specified files to stay untracked by Git
├── app.py                          # Main entry point for the application launch
├── dashboard.py                    # Streamlit interface for tracking email statistics
├── followup_scheduler.py           # Logic engine for queuing and managing follow-ups
├── requirements.txt                # List of required python dependencies
├── scheduler.py                    # Script orchestrating cron-like timing for outbox queues
└── setup_database.py               # Initializes the schema and tables for local tracking
```

---
## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com
cd mail_automater
```

### 2. Set up a virtual environment & install dependencies
```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Initialize the tracking database
```bash
python setup_database.py
```

### 4. Launch the application & dashboard
```bash
streamlit run app.py
```
