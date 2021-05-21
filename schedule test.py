from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
import logging
from telegram.ext import *
import constants as keys
logging.basicConfig(
    format='%(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

DAY = range(1)

def schedule(update, context):
    reply_keyboard = [['Monday', 'Tuesday', 'Wednesday']]
    update.message.reply_text("Which day would you like me to send the Reminder? (Format: Monday or Wednesday)",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                              )
    return DAY
# i want to get which day the user input as a string

def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def dayfromuser (update:Update, _: CallbackContext) -> int:
    text = str(logger.info(update.message.text))
    return text
# this code is trying to get user's message

def error(update, context):
    print(f"update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    conv_handler =(ConversationHandler(
        entry_points=[CommandHandler('schedule',schedule)],
        states={
        DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday)$'), dayfromuser)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        ))

    dp.add_error_handler(error)

    updater.start_polling(0)  # seconds on how often bot check for input
    updater.idle()

