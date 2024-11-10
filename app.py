from flask import Flask, request, jsonify
import telebot
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# from dotenv import load_dotenv
# load_dotenv()

bot_token="7826918701:AAGmBIL9xOrHN6JlQDJHQdBqYkkL2r9KSqI"

# Initialize Flask and bot
app = Flask(__name__)
bot = telebot.TeleBot(bot_token, threaded=False)

# Webhook configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'farmipole-69ae5776284b.herokuapp.com')  # Your actual Heroku domain
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
    logger.info(f"Setting webhook to: {webhook_url}")
    
    try:
        bot.remove_webhook()
        response = bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set response: {response}")
        return f"Webhook set to {webhook_url}"
    except Exception as e:
        logger.error(f"Error setting webhook: {str(e)}")
        return f"Failed to set webhook: {str(e)}", 500

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