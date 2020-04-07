from flask import Flask,request,jsonify
from config import TELEGRAM_WEBHOOK_URL
from telegram_process import TelegramBot

app = Flask(__name__)
TelegramBot.webhook_init(TELEGRAM_WEBHOOK_URL)
bot = TelegramBot()


@app.route('/hook', methods = ['POST'])
def main():
    req_data = request.get_json()
    bot.process_data(req_data)
    success = bot.data_message_judge()
    return jsonify(success = success)

if __name__ == '__main__':
    app.run(port = 5000)
