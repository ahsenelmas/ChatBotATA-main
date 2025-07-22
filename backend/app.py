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

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # 1. Check for mode input (professor, student, etc.)
        mode_data = get_mode_or_student_response(question)
        if mode_data:
            return jsonify(mode_data)

        # 2. Check for manual/static responses
        manual_answer = get_manual_answer(question.lower())
        if manual_answer:
            return jsonify(manual_answer)

        # 3. Forward to n8n webhook
        if not WEBHOOK_URL:
            print("⚠️ ERROR: WEBHOOK_URL is not set.")
            return jsonify({"error": "Server misconfiguration"}), 500

        res = requests.post(WEBHOOK_URL, json={"question": question}, timeout=10)

        try:
            response_data = res.json()
        except Exception as json_err:
            print("❌ Failed to parse JSON from webhook:", json_err)
            print("Response text:", res.text)
            return jsonify({"error": "Invalid response from webhook"}), 502

        # DEBUG: See what n8n returned
        print("✅ Webhook response:", response_data)

        if res.status_code != 200:
            print("❌ Webhook HTTP error:", res.status_code)
            return jsonify({"error": "n8n webhook error"}), 502

        # 4. Check for expected 'answer' field
        answer = response_data.get("answer")
        if not answer:
            return jsonify({"error": "No answer provided from webhook"}), 502

        return jsonify({"answer": answer})

    except Exception as e:
        print("🔥 Internal error:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
