# 🧠 ATA University Chatbot

A simple and interactive chatbot web app that answers frequently asked questions about ATA University. Built with a **Flask backend** and a **vanilla JavaScript frontend**, it features multilingual support (🇬🇧 EN / 🇹🇷 TR / 🇵🇱 PL) and user-specific modes for students, professors, and deans.

---

## ⚙️ Features

- 💬 Smart keyword-based Q&A chatbot  
- 🧑‍🎓 Student, 🧑‍🏫 Professor, and 🎓 Dean modes with themed UI  
- 🌐 Multilingual: English, Turkish, Polish  
- 📢 Announcement panel (for admin modes)  
- 📎 Quick links to university platforms  
- 📄 Simple CSV-based knowledge base  

---

## 🛠️ Technologies Used

- 🐍 Python 3.8+
- 🔥 Flask
- 🔄 Flask-CORS
- 🌐 HTML, CSS, JavaScript
- 📊 CSV file for local data storage (`answers.csv`)

---

## 📂 Project Structure
```
ATA-University-Chatbot/
├── backend/
│ ├── app.py
│ ├── knowledge_base.py
│ ├── answers.csv
│ ├── .env.sample
│ └── requirements.txt
├── frontend/
│ ├── index.html
│ ├── script.js
│ ├── style.css
│ ├── bear-mascot.png
│ ├── bear-mascot1.png
│ └── wseiz_page.png
├── .gitignore
└── README.md

```
---

## 🚀 Getting Started

### 🔧 Backend Setup (Flask API)

#### ✅ Requirements

- Python **3.8+**
- `pip` (Python package manager)

#### 🔌 Installation & Running

```bash
# 1. Go to the backend directory
cd backend

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# 3. Activate the virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create a .env file from the sample
cp .env.sample .env

# 6. Run the Flask app (on port 8000)
python app.py

```
<img width="1919" height="927" alt="image" src="https://github.com/user-attachments/assets/2de04caf-1984-4fb8-92f1-89653f21c479" />


