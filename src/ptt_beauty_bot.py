"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import time
import logging
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, InputMediaPhoto, InputMediaAnimation

import beauty

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

welcome_msg = '''歡迎使用表特板機器人
每天自動更新 2000 張表特板 50 推以上的圖
品質有保障，此專案由 CodingMan 開發

使用方法
請說「正妹」或「一群正妹」'''

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""

    custom_keyboard = [['正妹', '一群正妹']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="請稍後",
                             reply_markup=reply_markup)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('請說「正妹」或「一群正妹」')


def echo(update, context):
    """Echo the user message."""

    chat_id = update.message.chat.username
    print(f'[{chat_id}][{update.message.text}]')

    if '正妹' in update.message.text:
        picture = 0
        if '正妹' == update.message.text:
            picture = 1
        if '一群正妹' == update.message.text:
            picture = 3

        if picture == 0:
            update.message.reply_text(welcome_msg)
            return

        picture_list = beauty.pickup(picture)

        send_file_list = []
        for p in picture_list:

            current_file = None
            if p.endswith('jpg') or p.endswith('png'):
                # context.bot.send_photo(chat_id=update.effective_chat.id, photo=p)
                current_file = InputMediaPhoto(p)
            elif p.endswith('gif'):
                # context.bot.send_animation(update.effective_chat.id, 'https://i.imgur.com/QqMJj4K.gif')
                # current_file = InputMediaAnimation(p)
                pass
            if current_file is None:
                continue

            send_file_list.append(current_file)

        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=send_file_list)
    else:
        update.message.reply_text(welcome_msg)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    try:
        with open('./token.txt', 'r') as f:
            token = f.read()
    except FileNotFoundError:
        print('Please set your token in token.txt')
        sys.exit()
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    beauty.start()
    time.sleep(5)

    while beauty.in_update:
        time.sleep(1)

    print('表特板機器人啟動')
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
