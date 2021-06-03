from lib2to3.fixes.fix_input import context

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ForceReply, bot, update

import constants as keys
from telegram.ext import *
import responses as R
from datetime import datetime
import telebot
import schedule
import time
import logging
import Repcheck as Rep
import sched, time
import telegram as t

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


print("Current Time =", current_time)
print("Bot started...")

#logging.basicConfig(
   # format='%(message)s', level=logging.INFO
#)
#logger = logging.getLogger(__name__)

DAY, TIME = range(2)


def start_command(update, context):
    update.message.reply_text("Welcome to the UpdateParadeStateBot! Here is a list of our commands to get you started!")
    update.message.reply_text("/help will show what each command does!"
                              "/schedule helps to schedule new reminders!"
                              "/list shows you all your set reminders!"
                              )


# while current_time == '17:28:00':
#  send_reminder_message()

def remindertestmessage():
    remindertext = "This is a Reminder to Update your Parade State by Wednesday, 2200H"
    tb = telebot.TeleBot(keys.API_KEY)
    CHAT_ID = '551111942'
    # lucas chatid 25057684
    ret_msg = tb.send_message(CHAT_ID, remindertext)
    assert ret_msg.message_id


def help_command(update, context):
    update.message.reply_text("/schedule to set time that message is sent "
                              "/setaddress to set link of paradestate")


def handle_message(update, context):
    # global text
    text = str(update.message.text)  # .lower() #receive text from user


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def timefromuser (update:Update, context: CallbackContext) -> int:
    global timeusertext
    timeusertext = str(update.message.text)
    #update.message.reply_text(timeusertext)
    timeresponse = R.time_response(timeusertext) # process time given under responses.py
    update.message.reply_text(timeresponse)  # first reply
    scheduletest(update, context)

def dayfromuser(update: Update, context: CallbackContext) -> int:
    global dayusertext
    global dayresponse
    dayusertext = str(update.message.text)
    # update.message.reply_text(dayusertext)
    dayresponse = R.day_response(dayusertext)  # process the text under responses.py
    update.message.reply_text("At what time do you want to set the reminder?", reply_markup=ForceReply())  # first reply

    return TIME


def schedule_command(update, context):
        reply_keyboard = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']]
        update.message.reply_text("Which day would you like me to send the Reminder?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        global userchatid  # create a global variable
        userchatid = update.message.chat.id  # assign global variable to get chatID
        print(userchatid)
        # scheduletest(update, context)

        return DAY

    # text = str(update.message.text) #receive text from user
    # dayresponse = R.day_response(dayusertext) #process the text under responses.py
    # update.message.reply_text(dayresponse) #first reply

    # update.message.reply_text("Now, at what time would you like me to send the Reminder? (Format: e.g 17:30 for 5.30pm)")
    # text = update.message.text.lower()  # receive text from user
    # response = R.sample_responses(text)  # process the text under responses.py
    # update.message.reply_text(response)  #second reply

    # schedule.every(10).seconds.do(Send_Reminder_Message, update, context)
    # update.message.reply_text(R.sample_responses(R.reply))
    # schedule.every(10).seconds.do(print("hello"))
    # call schedule test function


def list_command(update, context):
    # update.message.reply_text("hello! here are your set reminders : (work in progress)")
    print(update.message.chat.id)


def Send_Reminder_Message(update, context):
    #remindertext = "This is a Reminder to Update your Parade State by Wednesday, 2200H"
    remindertext = "Time and Date is working"
    # update.message.text = remindertext
    # context.bot.send_message(chat_id=update.effective_chat.id, text=remindertext)
    #global userchatid
    #userchatid2 = str(userchatid)
    bot = context.bot
    global dbchatid
    context.bot.send_message(chat_id=dbchatid, text=remindertext)
    # update.message.reply_text(text=remindertext)
    #print(userchatid2)

def schedulecheck(context:CallbackContext):
    Rep.dict_read() # read DB
    print("DB Reading....")
    for IDitem, DAY, Time in sorted([(d['IDitem'],d['DAY'],d['Time']) for d in Rep.Inputs], key=lambda t: t[1] ):
        now = datetime.now()
        today = now.strftime("%A") #return today's day
        tdytime = now.strftime("%H:%M")
        if(today == DAY):
            if(tdytime == Time):
                global dbchatid
                dbchatid = str(IDitem)
                Send_Reminder_Message(update,context)
                print("sucess")
        else:
            print("Today not Thurs")




def scheduletest(update, context):
        global userchatid
        Rep.IDchat = userchatid
        Rep.day_r = dayusertext
        Rep.time_r = timeusertext
        Rep.text_r = 'Text'


        # To prepopulate the IDlist from a file
        ID_List = Rep.read_db()
        print("afterlist")
        print(ID_List)

        # Using Repetition checking function
        if Rep.repcheck(userchatid, ID_List):
            print("There are duplicates.")
            print("Override original schedule or add 1 more schedule")
            Rep.dict_read()
            Rep.dict_update(Rep.Inputs)
            print(Rep.Inputs)

            # Add user option to choose

        else:
            print("No duplicates.")

            # Adding new ID to IDList
            ID_List.append(userchatid)
            Rep.update_db(ID_List)
            print(ID_List)

            # Adding to dictionary database
            Rep.dict_read()
            Rep.dict_update(Rep.Inputs)
            print(Rep.Inputs)





        print("schedule set!")




# Function Not in Use
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]

    return chat_id
    print(chat_id)


def error(update, context):
    print(f"update {update} caused error {context.error}")

def printmessage(context: CallbackContext):
    print("helo")

def main():
        updater = Updater(keys.API_KEY, use_context=True)
        dp = updater.dispatcher

        j = updater.job_queue
        job_minute = j.run_repeating(schedulecheck, interval=10, first=0)
        print("checking on DB started")

        conv_handler = (ConversationHandler(
            entry_points=[CommandHandler('schedule', schedule_command)],
            states={
                DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday)$'), dayfromuser)],
                TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)], },
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("help", help_command))
        # dp.add_handler(CommandHandler("schedule", schedule_command))
        dp.add_handler(conv_handler)
        dp.add_handler(CommandHandler("list", list_command))
        dp.add_handler(CommandHandler("apple", scheduletest))
        dp.add_handler(CommandHandler("pear", schedulecheck))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        dp.add_error_handler(error)

        updater.start_polling(0)  # seconds on how often bot check for input
        updater.idle()





main()


