from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Bot
import logging
from flask import Flask, request

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

# Dictionary to store user links and letters
user_links = {}
user_letters = {}

# Define a function to handle incoming messages from users who clicked the unique link
@app.route('/receive_letter', methods=['POST'])
def receive_letter():
    user_id = request.form['user_id']
    letter = request.form['letter']

    if user_id not in user_letters:
        user_letters[user_id] = []

    user_letters[user_id].append(letter)
    return "نامه با موفقیت به دست عزیزتون رسید!"

def main():
    bot = Bot(token="7160482684:AAEPA4K8StP2Z3W9rJTC4N6ROgh0HfcEceE")
    updater = Updater(bot=bot, request_kwargs={'pool_connections': 8, 'pool_maxsize': 8})
    dispatcher = updater.dispatcher

    # Define a function to handle the /start command (welcome message)
    def start(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="سلام دوستان! خوش اومدید. لطفاً از منو یا لینک مد نظر خودتونو دریافت کنید و یا نامه‌های خودتونو مشاهده کنید")

    # Define a function to handle the /give_me_my_link command
    def give_me_my_link(update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        user_links[user_id] = f'https://t.me/AnonNowruzLettersBot?start={user_id}'
        update.message.reply_text(f"لینک خاص خود خود شما: {user_links[user_id]}. لطفاً نامه‌تون رو بنویسید و ارسال کنید")

    # Define a function to handle the /see_my_letters command
    def see_my_letters(update: Update, context: CallbackContext) -> None:
        user_id = update.message.from_user.id
        if user_id in user_letters:
            letters = user_letters[user_id]
            update.message.reply_text(f"نامه‌های دریافت شده:\n{', '.join(letters)}")
        else:
            update.message.reply_text("شما هنوز نامه‌ای ندارید. لطفاً لینکتون رو با بقیه به اشتراک بذارید :)")

    # Add command handlers for /start, /give_me_my_link, and /see_my_letters
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("give_me_my_link", give_me_my_link))
    dispatcher.add_handler(CommandHandler("see_my_letters", see_my_letters))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    app.run()
