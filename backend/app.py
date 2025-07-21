from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os
from dotenv import load_dotenv
from knowledge_base import get_manual_answer, get_mode_or_student_response

load_dotenv()
app = Flask(__name__)
CORS(app)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def send_to_webhook(question, response):
    if not WEBHOOK_URL:
        return
    try:
        requests.post(WEBHOOK_URL, json={"question": question, "response": response}, timeout=3)
    except requests.RequestException as e:
        print("Webhook error:", e)

@app.route("/")
def index():
    return "✅ ATA Chatbot backend is running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip().lower()
    if not question:
        return jsonify({"error": "Missing question"}), 400

    mode_response = get_mode_or_student_response(question)
    if mode_response:
        send_to_webhook(question, mode_response)
        return jsonify(mode_response)

    manual = get_manual_answer(question)
    if manual:
        send_to_webhook(question, manual)
        return jsonify(manual)

    unknown = {"answer": "❓ I didn’t understand that question."}
    send_to_webhook(question, unknown)
    return jsonify(unknown)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=(os.getenv("FLASK_ENV") == "development"), port=port)
