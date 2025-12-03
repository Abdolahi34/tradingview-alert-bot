from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return {"error": "No JSON body received"}, 400

    # TradingView معمولاً alert_message می فرستد
    message = data.get("alert_message") or data.get("message") or str(data)

    if not message:
        return {"error": "Message not found in payload"}, 400

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(TELEGRAM_URL, json=payload, timeout=5)

        if response.status_code != 200:
            return {"error": "Telegram rejected request"}, 500

        return {"status": "sent"}, 200

    except Exception as e:
        return {"error": f"Telegram Send Failed: {str(e)}"}, 500


@app.route("/", methods=["GET"])
def home():
    return {"status": "running"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
