from flask import Flask, request, jsonify, session, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import requests
from datetime import datetime, timedelta
from models import db, User, Conversation, Message

# -------------------- App Config --------------------
app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Load secret key from environment or use fallback (for dev only)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_dev_key")

# Set session lifetime
app.permanent_session_lifetime = timedelta(days=3)

db.init_app(app)
CORS(app)

# Groq API key
GROQ_API_KEY = "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"

# -------------------- Routes --------------------

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if 'user_id' in session:
        return send_from_directory('.', 'chat.html')
    return send_from_directory('.', 'login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

@app.route('/start_conversation', methods=['POST'])
def start_conversation():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conv = Conversation(user_id=session['user_id'], title=request.json.get('title', 'Untitled'))
    db.session.add(conv)
    db.session.commit()
    return jsonify({'conversation_id': conv.id})

@app.route('/get_conversations', methods=['GET'])
def get_conversations():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conversations = Conversation.query.filter_by(user_id=session['user_id']).order_by(Conversation.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'created_at': c.created_at.isoformat()
    } for c in conversations])

@app.route('/delete_conversation/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    convo = Conversation.query.filter_by(id=conversation_id, user_id=session['user_id']).first()
    if convo:
        Message.query.filter_by(conversation_id=convo.id).delete()
        db.session.delete(convo)
        db.session.commit()
        return jsonify({'message': 'Conversation deleted'})
    return jsonify({'error': 'Conversation not found'}), 404

@app.route('/get_messages/<int:conversation_id>', methods=['GET'])
def get_messages(conversation_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
    return jsonify([{
        'role': m.role,
        'content': m.content,
        'timestamp': m.timestamp.isoformat()
    } for m in messages])

@app.route('/chat/<int:conversation_id>', methods=['POST'])
def chat(conversation_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.timestamp).all()
    history = [{"role": m.role, "content": m.content} for m in messages]
    history.append({"role": "user", "content": user_message})

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama3-70b-8192",
            "messages": history,
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": False
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]

        db.session.add(Message(conversation_id=conversation_id, role="user", content=user_message))
        db.session.add(Message(conversation_id=conversation_id, role="assistant", content=ai_reply))
        db.session.commit()

        return jsonify({'reply': ai_reply})

    except requests.exceptions.RequestException as e:
        print(f"Error from Groq: {e}")
        return jsonify({'reply': "⚠️ Failed to get AI response"}), 500

# -------------------- Main --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
