AI Assistant Web Application
This is a personal project built to explore web development, user authentication, API integration, and persistent data storage. The application provides a local, browser-based chat interface that supports user login, conversation history, and optional voice output. Everything runs locally on the user's machine without requiring external servers.

Features
User registration and login with secure password authentication

Multiple chat threads per user

Persistent message history stored in a local SQLite database

Integration with a language model API to generate responses

Optional voice output using browser-based speech synthesis

Dark mode interface

Auto logout after inactivity for better security

Built using Python (Flask), HTML, CSS, and JavaScript

Tech Stack
Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite

API Integration: Language model API

Other: Web Speech API (optional)

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your_username/ai-assistant-web.git
cd ai-assistant-web
Set up a virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set your API key:

bash
Copy
Edit
set API_KEY=your_key_here         # On Windows
export API_KEY=your_key_here      # On macOS/Linux
Run the application:

bash
Copy
Edit
python server.py
Open your browser and visit:

arduino
Copy
Edit
http://localhost:5000
Directory Overview
cpp
Copy
Edit
ai-assistant-web/
├── static/
├── templates/
├── server.py
├── database.db
├── requirements.txt
├── README.md
└── ...
Possible Future Enhancements
Add speech-to-text support

Implement user profile settings

Cloud deployment support

Enable multilingual conversations

Notes
This project was created as a way to apply and strengthen web development skills and is part of a learning portfolio. It is not licensed for commercial use.
