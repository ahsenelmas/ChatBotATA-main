import os
import uuid
import logging
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from knowledge_base import get_manual_answer, get_mode_or_student_response

# -----------------------------------------------------------------------------
# Environment & logging
# -----------------------------------------------------------------------------
# Load .env no matter where the process is started from
dotenv_path = find_dotenv() or Path(__file__).with_name(".env")
load_dotenv(dotenv_path, override=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("app")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))
FLASK_ENV = os.getenv("FLASK_ENV", "development")

log.info("Loaded .env from: %s", dotenv_path)
log.info("WEBHOOK_URL: %s", WEBHOOK_URL)

# Optional fallback to avoid hard crashes if env is missing
DEFAULT_WEBHOOK = None  # put a default URL here if you want
if not WEBHOOK_URL and DEFAULT_WEBHOOK:
    WEBHOOK_URL = DEFAULT_WEBHOOK
    log.warning("WEBHOOK_URL was missing. Falling back to DEFAULT_WEBHOOK: %s", WEBHOOK_URL)

# -----------------------------------------------------------------------------
# HTTP session with retries (for n8n webhook)
# -----------------------------------------------------------------------------
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=0.4,
    status_forcelist=(408, 429, 500, 502, 503, 504),
    allowed_methods=frozenset(["POST", "GET"]),
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# -----------------------------------------------------------------------------
# Flask
# -----------------------------------------------------------------------------
app = Flask(__name__)
# In production lock this down: CORS(app, resources={r"/ask": {"origins": "https://your-frontend.com"}})
CORS(app)


def error(message: str, code: int):
    return jsonify({"error": message}), code


@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/health", methods=["GET"])
def health():
    ok = bool(WEBHOOK_URL)
    return jsonify({"status": "ok" if ok else "misconfigured", "webhook_url_present": ok}), (200 if ok else 500)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        if not WEBHOOK_URL:
            log.error("WEBHOOK_URL is not set.")
            return error("Server misconfiguration", 500)

        data = request.get_json(silent=True) or {}
        question = (data.get("question") or "").strip()
        session_id = data.get("sessionId") or str(uuid.uuid4())
        lang = data.get("lang") or "en"

        if not question:
            return error("No question provided", 400)

        # 1) Local mode checks (professor/dean/student)
        mode_data = get_mode_or_student_response(question)
        if mode_data:
            # Keep same contract so the frontend can branch on 'mode'
            mode_data.setdefault("sessionId", session_id)
            return jsonify(mode_data)

        # 2) Manual/static answers
        manual_answer = get_manual_answer(question.lower())
        if manual_answer:
            manual_answer.setdefault("sessionId", session_id)
            return jsonify(manual_answer)

        # 3) Forward to n8n webhook
        payload = {"question": question, "sessionId": session_id, "lang": lang}
        log.info("→ Forwarding to n8n (%s): %s", WEBHOOK_URL, payload)

        res = session.post(WEBHOOK_URL, json=payload, timeout=15)

        # Attempt to parse JSON
        try:
            response_data = res.json()
        except Exception as json_err:
            log.exception("Failed to parse JSON from webhook. Text: %s", res.text)
            return error("Invalid response from webhook", 502)

        log.info("← n8n responded (%s): %s", res.status_code, response_data)

        if res.status_code != 200:
            return error("n8n webhook error", 502)

        # Optionally attach sessionId back so the frontend can see/keep it (harmless)
        if isinstance(response_data, dict):
            response_data.setdefault("sessionId", session_id)

        return jsonify(response_data)

    except requests.RequestException as net_err:
        log.exception("Network error while calling n8n")
        return error("Upstream webhook network error", 502)
    except Exception as e:
        log.exception("Internal error")
        return error("Internal server error", 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=(FLASK_ENV == "development"))
