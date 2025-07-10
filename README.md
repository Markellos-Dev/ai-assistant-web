# AI Assistant Web Application

This project is a web-based AI assistant that allows users to interact with an AI model via a simple chat interface. It supports persistent conversation history, user authentication, and optional speech synthesis. The backend is built using Flask and stores data locally using SQLite. The application is designed for local deployment and runs entirely on the user's machine.

## Features

- User registration and login with password authentication
- Multiple conversation threads per user
- Persistent chat history saved in a local SQLite database
- Integration with the Groq API (LLaMA3 model) for generating AI responses
- Optional speech synthesis using the Web Speech API
- Dark mode user interface
- Secure automatic logout after inactivity
- Frontend built with HTML/CSS/JS and backend with Python Flask

## Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- API Integration: Groq API (llama3-70b-8192)
- Optional: SpeechSynthesis (browser-based)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/ai-assistant-web.git
   cd ai-assistant-web
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Groq API key in the environment:
   ```bash
   set GROQ_API_KEY=your_key_here   # Windows
   export GROQ_API_KEY=your_key_here # macOS/Linux
   ```

5. Run the app:
   ```bash
   python server.py
   ```

6. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Screenshots

*(You can include a screenshot of the UI here if available)*

## Directory Structure

```
ai-assistant-web/
├── static/
├── templates/
├── server.py
├── database.db
├── requirements.txt
├── README.md
└── ...
```

## Future Improvements

- Speech-to-text support for full voice interaction
- Profile settings for users
- Deployment on cloud platforms
- Support for multilingual chat (e.g., Greek)

## License

This project is open for review as part of a job application and is not yet licensed for commercial use.
