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
import logging
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, InputMediaPhoto

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

welcome_msg = '''CodingMan 歡迎回來'''


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""

    update.message.reply_text(welcome_msg)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('這是 help 指令')


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def echo(update, context):
    """Echo the user message."""

    chat_id = update.message.chat.username
    print(f'[{chat_id}][{update.message.text}]')

    # update.message.reply_text(update.message.text)
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://i.imgur.com/QY7WdgG.jpg')
    # context.bot.send_animation(update.effective_chat.id, 'https://i.imgur.com/QqMJj4K.gif')

    file_list = [
        InputMediaPhoto('https://i.imgur.com/QY7WdgG.jpg')
    ] * 10

    context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=file_list)

    # custom_keyboard = [['正妹', '一群正妹']]
    # reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    # context.bot.send_message(chat_id=update.effective_chat.id,
    #                  text="Custom Keyboard Test",
    #                  reply_markup=reply_markup)



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    try:
        with open('./token_demo.txt', 'r') as f:
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

    print('測試機器人啟動')
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
