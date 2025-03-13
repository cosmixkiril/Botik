import os
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

import openai
openai.api_key = OPENAI_API_KEY

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")

    if user_message:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            answer = response["choices"][0]["message"]["content"]
        except Exception as e:
            answer = "Ошибка при обращении к OpenAI."
    else:
        answer = "Я понимаю только текст."

    requests.post(API_URL, json={"chat_id": chat_id, "text": answer})
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "BotCosmixGpT is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
