from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ForceReply, bot, update
import constants as keys
from telegram.ext import *
import responses as R
from datetime import datetime
import logging
import Repcheck as Rep

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

print("Current Time =", current_time)
print("Bot started...")

#logging.basicConfig(format='%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

NAME, DAY, TIME, MESSAGE = range(4)

def start_command(update, context):
    update.message.reply_text("Welcome to the UpdateParadeStateBot!")
    update.message.reply_text("To get started, simply type /help to view all the operational commands")

def help_command(update, context):
    update.message.reply_text("/schedule is to set a new reminder\n"
                              "/list shows you a list of reminders that you have set")

def list_command(update, context):
    # update.message.reply_text("hello! here are your set reminders : (work in progress)")
    #print(update.message.chat.idj)
    Rep.dict_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id
    #for IDitem, DAY, Time, Text in Rep.Inputs:
    replylist = []
    for ReminderName,IDitem, DAY, Time, Text in sorted([(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Rep.Inputs],key=lambda t: t[1]):
        if(userchatid == IDitem): #check userchatid against db id
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime= str(Time)
            dbmsg = str(Text)
            stringreply = "Reminder Name: " + dbRemName + "\nDay: " + dbday  + "\n" + "Time: " + dbtime + "\n" +  "Message: "  + dbmsg + "\n\n" #crafting string
            replylist.append(stringreply) #append into the list

    if not replylist: #checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        update.message.reply_text("Here are your List of Reminders: \n\n" + "".join(replylist)) #sentence + joining the list

def del_command(update,context):
    namelist = []
    Rep.dict_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id
    # for IDitem, DAY, Time, Text in Rep.Inputs:
    replylist = []
    for ReminderName, IDitem, DAY, Time, Text in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Rep.Inputs], key=lambda t: t[1]):
        if (userchatid == IDitem):  # check userchatid against db id
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime = str(Time)
            dbmsg = str(Text)
            stringreply = "Reminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
            replylist.append(stringreply)  # append into the list
        namelist.append(dbRemName) #append all names relating to this chatid into local list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist] # get each item in namelist and put in custom keyboard
        update.message.reply_text(
            "Here are your List of Reminders: \n\n" + "".join(replylist) + "\n\nPlease Select the Reminder you would like to delete according to ReminderName", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)  # sentence + joining the list








def schedule_command(update, context):
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday']]
        update.message.reply_text("Which day would you like me to set the Reminder?",
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

        global userchatid  # create a global variable
        userchatid = update.message.chat.id  # assign global variable to get chatID
        print(userchatid)
        # scheduletest(update, context)

        return DAY

def namefromuser(update: Update, context: CallbackContext)-> int:
    global userchatid
    userchatid = update.message.chat.id
    global nameusertext
    nameusertext = str(update.message.text)
    #update.message.reply_text(nameusertext)
    scheduletest(update, context)
    update.message.reply_text("Reminder Name: " + nameusertext + "\n\n" + timeresponse + "\n\nYour Reminder Message: " + messagefromuser)
    successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    context.bot.send_message(chat_id=userchatid, text=successtext)

    return ConversationHandler.END

def dayfromuser(update: Update, context: CallbackContext) -> int:
    global dayusertext
    global dayresponse
    dayusertext = str(update.message.text)
    # update.message.reply_text(dayusertext)
    dayresponse = R.day_response(dayusertext)  # process the text under responses.py
    update.message.reply_text("At what time do you want to set the reminder? (Format: HH:MM, e.g: 17:30)", reply_markup=ForceReply())  # first reply

    return TIME

def timefromuser (update:Update, context: CallbackContext) -> int:
    global timeusertext
    timeusertext = str(update.message.text)
    #update.message.reply_text(timeusertext)
    global timeresponse
    timeresponse = R.time_response(timeusertext) # process time given under responses.py
    update.message.reply_text("What would you like the Reminder Message to be?", reply_markup=ForceReply())
    #update.message.reply_text(timeresponse)  # first reply
    #scheduletest(update, context)

    return MESSAGE

def messagefromuser (update:Update, context: CallbackContext) -> int:
    global userchatid
    userchatid = update.message.chat.id
    global messagefromuser
    messagefromuser = str(update.message.text)
     # process time given under responses.py
    update.message.reply_text("Lastly, what would you like to name this Reminder?", reply_markup=ForceReply())
    return NAME
    #update.message.reply_text(timeresponse + "\n\nYour Reminder Message: " + messagefromuser)
    #scheduletest(update, context)
    #successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    #context.bot.send_message(chat_id=userchatid, text=successtext)


    #return ConversationHandler.END

def scheduletest(update, context):
        global userchatid
        Rep.RemName = nameusertext
        Rep.IDchat = userchatid
        Rep.day_r = dayusertext
        Rep.time_r = timeusertext
        Rep.text_r = messagefromuser


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
            Rep.reno = Rep.reno + 1
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
            Rep.reno = Rep.reno + 1
            print(Rep.Inputs)

        print("schedule set!")

def Send_Reminder_Message(update, context):
    remindertext = dbremindermsg
    # update.message.text = remindertext
    # context.bot.send_message(chat_id=update.effective_chat.id, text=remindertext)
    #global userchatid
    #userchatid2 = str(userchatid)
    bot = context.bot
    global dbchatid
    context.bot.send_message(chat_id=dbchatid, text=remindertext)
    # update.message.reply_text(text=remindertext)
    #print(userchatid2)


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Set reminder cancelled. Hope to talk to you again. Bye!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def handle_message(update, context):
    # global text
    text = str(update.message.text)  # .lower() #receive text from user

def schedulecheck(context:CallbackContext):
    Rep.dict_read() # read DB
    print("DB Reading....")
    for IDitem, DAY, Time, Text in sorted([(d['IDitem'],d['DAY'],d['Time'],d['Text']) for d in Rep.Inputs], key=lambda t: t[1] ):
        now = datetime.now()
        today = now.strftime("%A") #return today's day
        tdytime = now.strftime("%H:%M")
        if(today == DAY):
            if(tdytime == Time):
                global dbchatid
                dbchatid = str(IDitem)
                global dbremindermsg
                dbremindermsg = str(Text)
                Send_Reminder_Message(update,context)
                print("sucess")
        else:
            print(IDitem)
            print("This ChatID's Reminder is not Now ")

def error(update, context):
    print(f"update {update} caused error {context.error}")


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

def main():
        updater = Updater(keys.API_KEY2, use_context=True)
        dp = updater.dispatcher

        j = updater.job_queue
        job_minute = j.run_repeating(schedulecheck, interval=10, first=0)
        print("checking on DB started")

        conv_handler = (ConversationHandler(
            entry_points=[CommandHandler('schedule', schedule_command)],
            states={
                NAME:[MessageHandler(Filters.all, namefromuser)],
                DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday)$'), dayfromuser)],
                TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)],
                MESSAGE: [MessageHandler(Filters.all, messagefromuser)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("help", help_command))
        #dp.add_handler(CommandHandler("schedule", schedule_command))
        dp.add_handler(conv_handler)
        dp.add_handler(CommandHandler("delete", del_command))
        dp.add_handler(CommandHandler("list", list_command))
        dp.add_handler(CommandHandler("apple", scheduletest))
        dp.add_handler(CommandHandler("pear", schedulecheck))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        dp.add_error_handler(error)

        updater.start_polling(0)  # seconds on how often bot check for input
        updater.idle()


main()


