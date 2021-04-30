import constants as keys
from telegram import bot
from telegram.ext import *
import responses as R
from datetime import datetime
import telebot


now = datetime.now()
current_time= now.strftime("%H:%M:%S")

print("Current Time =",current_time)
print ("Bot started...")

def start_command(update, context):
    update.message.reply_text("Welcome to the UpdateParadeStateBot! Here is a list of our commands to get you started!")
    update.message.reply_text("/help will show what each command does!"
                              "/schedule helps to schedule new reminders!"
                              "/list shows you all your set reminders!"
                            )
   # while current_time == '17:28:00':
      #  send_reminder_message()

def send_reminder_message():
    remindertext = "This is a Reminder to Update your Parade State by Wednesday, 2200H"
    tb = telebot.TeleBot(keys.API_KEY)
    CHAT_ID = '551111942'
    #lucas chatid 25057684
    ret_msg = tb.send_message(CHAT_ID, remindertext)
    assert ret_msg.message_id

def help_command(update, context):
    update.message.reply_text("/schedule to set time that message is sent "
                              "/setaddress to set link of paradestate")

def handle_message(update, context):
    text = str(update.message.text).lower() #receive text from user
    response = R.sample_responses(text) #process the text

    update.message.reply_text(response) # reply the text

def schedule_command(update,context):
    update.message.reply_text("What time would you like me to send the Reminder? (Format: e.g 17:30 for 5.30pm)")
    text = update.message.text.lower()  # receive text from user
    response = R.sample_responses(text)  # process the text

def list_command(update,context):
    update.message.reply_text("hello! here are your set reminders : (work in progress)")

def Send_Reminder_Message(update, context):
    remindertext = "This is a Reminder to Update your Parade State by Wednesday, 2200H"
    update.message.text = remindertext

def error(update, context):
    print(f"update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("schedule", schedule_command))
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))


    dp.add_error_handler(error)

    updater.start_polling(0) #seconds on how often bot check for input
    updater.idle()

main()