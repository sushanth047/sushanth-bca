from flask import Flask, render_template, request, jsonify
import nltk
import sqlite3
from nltk.chat.util import Chat, reflections

# Ensure NLTK data is downloaded
nltk.download('punkt')

app = Flask(__name__)

# Define the chatbot pairs and reflections
pairs = [
    [r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']],
    [r'how are you?', ['I am doing well, thank you!', 'I am fine, how about you?']],
    [r'what is your name?', ['I am BCA-ChatBot. I am created to assist BCA-Students', 'You can call me bca-bot.']],
    [r'bye|exit', ['Goodbye!', 'It was nice talking to you. Goodbye!']],
[r'tell me about bca|bca', ['hm']]
]

reflections = {
    "i am": "you are",
    "i was": "you were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

chat = Chat(pairs, reflections)

# Initialize the database
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, sender TEXT, message TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Store message in the database
def store_message(sender, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, message) VALUES (?, ?)", (sender, message))
    conn.commit()
    conn.close()

# Retrieve chat history
def get_chat_history():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT sender, message FROM messages")
    chat_history = c.fetchall()
    conn.close()
    return chat_history

@app.route("/")
def home():
    chat_history = get_chat_history()
    return render_template("index.html", chat_history=chat_history)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    store_message("user", user_input)
    response = chat.respond(user_input)
    store_message("bot", response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
