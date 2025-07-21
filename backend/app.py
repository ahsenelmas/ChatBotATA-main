from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from knowledge_base import get_manual_answer, get_mode_or_student_response

load_dotenv()

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        # Mode check
        mode_data = get_mode_or_student_response(question)
        if mode_data:
            return jsonify(mode_data)

        # Static answer
        manual_answer = get_manual_answer(question.lower())
        if manual_answer:
            return jsonify(manual_answer)

        # Forward to webhook
        res = requests.post(WEBHOOK_URL, json={"question": question}, timeout=10)

        try:
            response_data = res.json()
        except Exception as json_err:
            print("Failed to parse JSON from webhook:", json_err)
            return jsonify({"error": "Invalid response from webhook"}), 502

        if res.status_code != 200:
            print("Webhook error:", res.status_code, response_data)
            return jsonify({"error": "n8n webhook error"}), 502

        return jsonify(response_data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
