from flask import Flask, request, jsonify
import telebot
from telebot.handler_backends import WebhookHandler

# Initialize Flask and bot
app = Flask(__name__)
bot = telebot.TeleBot("7826918701:AAGmBIL9xOrHN6JlQDJHQdBqYkkL2r9KSqI", threaded=False)

# Webhook configuration
WEBHOOK_URL = 'https://farmipole-69ae5776284b.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{bot.token}'

# Bot handlers
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Flask routes
@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

@app.route('/set_webhook')
def set_webhook():
    webhook_url = f'{WEBHOOK_URL}{WEBHOOK_PATH}'
    bot.remove_webhook()
    webhook_info = bot.set_webhook(url=webhook_url)
    return jsonify({
        'webhook_url': webhook_url,
        'success': webhook_info,
        'webhook_info': bot.get_webhook_info().to_dict()
    })

@app.route('/webhook_info')
def get_webhook_info():
    return jsonify(bot.get_webhook_info().to_dict())

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)