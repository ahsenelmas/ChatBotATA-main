from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import requests
from knowledge_base import get_manual_answer, get_mode_or_student_response

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://tufan34568.app.n8n.cloud/webhook/001e62bf-e1e7-4476-8b83-4d4774940d77/chat"

def send_to_webhook(question, answer):
    payload = {
        "question": question,
        "answer": answer
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("✅ Sent to webhook:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("❌ Webhook error:", e)

@app.route('/ask', methods=['POST'])
def ask():
    data_in = request.json
    question = data_in.get('question', '').strip().lower()

    mode_or_student = get_mode_or_student_response(question)
    if mode_or_student:
        send_to_webhook(question, mode_or_student.get("answer", ""))
        return jsonify(mode_or_student)

    answer = get_manual_answer(question)
    if answer:
        send_to_webhook(question, answer.get("answer", ""))
        return jsonify(answer)

    fallback = {"answer": "Sorry, I don't know the answer to that question."}
    send_to_webhook(question, fallback["answer"])
    return jsonify(fallback)

if __name__ == '__main__':
    app.run(debug=True ,port=8000)
