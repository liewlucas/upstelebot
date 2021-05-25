from telegram import Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import *
from datetime import datetime
import logging

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

print("Current Time =", current_time)
print("Bot started...")

logging.basicConfig(
    format='%(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

DAY, TIME = range(2)


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def timefromuser(update: Update, context: CallbackContext) -> int:
    print("hello")
    global timeusertext
    timeusertext = str(update.message.text)
    update.message.reply_text(timeusertext)


def dayfromuser(update: Update, context: CallbackContext) -> int:
    global dayusertext
    dayusertext = str(update.message.text)
    update.message.reply_text(dayusertext)
    update.message.reply_text("At what time do you want to set the reminder?",reply_markup=ForceReply())  # first reply

    return TIME


def schedule_command(update, context):
    reply_keyboard = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
    update.message.reply_text("Which day would you like me to send the Reminder? (Format: Monday or Wednesday)",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                               resize_keyboard=True), )

    global userchatid  # create a global variable
    userchatid = update.message.chat.id  # assign global variable to get chatID
    print(userchatid)

    return DAY


def main():
    updater = Updater("1801853201:AAGy29WlJOunvUpO75unKo11_lOA7kyOfmc", use_context=True)
    dp = updater.dispatcher

    conv_handler = (ConversationHandler(
        entry_points=[CommandHandler('schedule', schedule_command)],
        states={
            DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday)$'), dayfromuser)],
            TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)], },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    dp.add_handler(conv_handler)

    updater.start_polling(0)  # seconds on how often bot check for input
    updater.idle()


main()