from flask import Flask, request, jsonify
import telebot
import os

# Initialize Flask and bot
app = Flask(__name__)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'), threaded=False)

# Webhook configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://farmipole-69ae5776284b.herokuapp.com')
WEBHOOK_PATH = f'/webhook/{bot.token}'

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False, 'error': 'Invalid content type'}), 400

# Route for setting webhook
@app.route('/set_webhook')
def set_webhook():
    webhook_url = f'https://{WEBHOOK_URL}{WEBHOOK_PATH}'
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook set to {webhook_url}"

# Simple health check route
@app.route('/')
def health():
    return 'Bot is running'

# Your message handlers here
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your bot.")

if __name__ == '__main__':
    app.run()