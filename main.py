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

EDITINDB, EDITCHOICE, EDIT, DELETE, NAME, DAY, TIME, MESSAGE = range(8)

def start_command(update, context):
    update.message.reply_text("Welcome to the UpdateParadeStateBot! \U0001F917")
    update.message.reply_text("To get started, simply type /help to view all the operational commands\U0001F4C4")

def help_command(update, context):
    update.message.reply_text("This bot enables you to create, delete, and edit reminders. Please follow the commands stated below to get started! \U0001f60A \n\n"
                              "/schedule is to set a new reminder\n"
                              "/list shows you a list of reminders that you have set\n"
                              "/delete allows for you to delete reminders based on the Reminder Names")

def list_command(update, context):
    # update.message.reply_text("hello! here are your set reminders : (work in progress)")
    #print(update.message.chat.idj)
    global userchatidingroup
    userchatidingroup = update.message.message_id
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
        update.message.reply_text("\U0001F4D1Here are your List of Reminders: \n\n" + "".join(replylist),reply_to_message_id=userchatidingroup) #sentence + joining the list

def del_command(update,context):
    namelist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
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
            "\u274C DELETE \u274C\n\n"
            "Here are your List of Reminders: \n\n" + "".join(replylist) + "\n\nPlease Select the Reminder you would like to delete according to ReminderName", reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True),)  # sentence + joining the list + custom keyboard

        return DELETE


def deletefromdb(update: Update, context: CallbackContext)-> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global usernamechoice
    usernamechoice = str(update.message.text)
    userchatidingroup = str(update.message.message_id)
    Rep.usercid_r = userchatid
    Rep.name_r = usernamechoice
    Rep.dict_del(Rep.Inputs)
    Rep.dict_read()  # read DB
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
    update.message.reply_text(
        "Your Reminder has been deleted, Here is your Updated List of Reminders: \n\n" + "".join(replylist), reply_to_message_id=userchatidingroup)
    userchatidingroup = str(update.message.from_user.id)
    update.message.reply_text(userchatidingroup)
    update.message.reply_text(userchatid)

    return ConversationHandler.END


def edit_command(update, context):
    namelist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
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
        namelist.append(dbRemName)  # append all names relating to this chatid into local list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist]  # get each item in namelist and put in custom keyboard
        update.message.reply_text(
            "\U0001F4DD EDITING \U0001F4DD \n\n"
            "Here are your List of Reminders: \n\n" + "".join(
                replylist) + "\n\n" + "Please Select the Reminder you would like to Edit",
            reply_to_message_id=userchatidingroup,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                             selective=True), )  # sentence + joining the list + custom keyboard
        return EDIT

def editfromuser(update: Update, context: CallbackContext)-> int:
    replylist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
    editnameuser = str(update.message.text)
    Rep.dict_read()  # read DB
    for ReminderName,IDitem, DAY, Time, Text in sorted([(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Rep.Inputs],key=lambda t: t[1]):
        if(ReminderName == editnameuser):
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime = str(Time)
            dbmsg = str(Text)
            stringreply = "Reminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
            replylist.append(stringreply)  # append into the list
            reply_keyboard = [["Reminder Name"], ["Day"], ["Time"], ["Message"]]  # get each item in namelist and put in custom keyboard
            update.message.reply_text("Here are the details for this Reminder: \n\n" + "".join(replylist) + "\nPlease Select which field you would like to edit.",
                                      reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))  # sentence + joining the list
            return EDITCHOICE

def useredits(update: Update, context: CallbackContext)-> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editchoiceuser
    editchoiceuser = str(update.message.text)
    if(editchoiceuser == "Time"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser + " (Format: HH:MM, e.g: 17:30)",reply_to_message_id=userchatidingroup, reply_markup=ForceReply(userchatidingroup))
    if(editchoiceuser == "Day"):
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday']]
        update.message.reply_text("Please select the new details for " + editchoiceuser, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))
    if(editchoiceuser == "Reminder Name"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(userchatidingroup))
    if (editchoiceuser == "Message"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(userchatidingroup))
    return EDITINDB

def editindb(update: Update, context: CallbackContext)-> int:
    usersconfirmationedit = str(update.message.text)
    if(editchoiceuser == "Time"):
        Rep.time_r = usersconfirmationedit
        update.message.reply_text("Your Update is : " + usersconfirmationedit)
    if(editchoiceuser == "Day"):
        Rep.day_r = usersconfirmationedit
        update.message.reply_text("Your Update is : " + usersconfirmationedit)
    if(editchoiceuser == "Reminder Name"):
        Rep.RemName = usersconfirmationedit
        update.message.reply_text("Your Update is : " + usersconfirmationedit)
    if(editchoiceuser == "Message"):
        Rep.text_r = usersconfirmationedit
        update.message.reply_text("Your Update is : " + usersconfirmationedit)

    return ConversationHandler.END






def schedule_command(update, context):
        global userchatidingroup
        userchatidingroup = update.message.message_id
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday']]
        update.message.reply_text(
            "\U0001F570 SCHEDULE \U0001F570 \n\n"
            "Which day would you like me to set the Reminder?",
                                  reply_to_message_id=userchatidingroup,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True), )
        global userchatid  # create a global variable
        userchatid = update.message.chat.id  # assign global variable to get chatID
        print(userchatid)
        # scheduletest(update, context)

        return DAY

def namefromuser(update: Update, context: CallbackContext)-> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global userchatid
    userchatid = update.message.chat.id
    global nameusertext
    nameusertext = str(update.message.text)
    #update.message.reply_text(nameusertext)
    scheduletest(update, context)
    update.message.reply_text("\u2705Your Reminder has been scheduled! Here are the details: \n\n" + "Reminder Name: " + nameusertext + "\n\n" + timeresponse + "\n\nYour Reminder Message: " + messagefromuser, reply_to_message_id=userchatidingroup)
    successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    context.bot.send_message(chat_id=userchatid, text=successtext)

    return ConversationHandler.END

def dayfromuser(update: Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global dayusertext
    global dayresponse
    dayusertext = str(update.message.text)
    # update.message.reply_text(dayusertext)
    dayresponse = R.day_response(dayusertext)  # process the text under responses.py
    update.message.reply_text("At what time do you want to set the reminder? (Format: HH:MM, e.g: 17:30)", reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))  # first reply

    return TIME

def timefromuser (update:Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global timeusertext
    timeusertext = str(update.message.text)
    #update.message.reply_text(timeusertext)
    global timeresponse
    timeresponse = R.time_response(timeusertext) # process time given under responses.py
    update.message.reply_text("What would you like the Reminder Message to be?",reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True),)
    #update.message.reply_text(timeresponse)  # first reply
    #scheduletest(update, context)

    return MESSAGE

def messagefromuser (update:Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global userchatid
    userchatid = update.message.chat.id
    global messagefromuser
    messagefromuser = str(update.message.text)
     # process time given under responses.py
    update.message.reply_text("Lastly, what would you like to name this Reminder?", reply_markup=ForceReply(selective=True),reply_to_message_id=userchatidingroup)
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
            #Rep.reno = Rep.reno + 1
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
            #Rep.reno = Rep.reno + 1
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
        'Set reminder cancelled. Hope to talk to you again. Bye!', reply_markup=ReplyKeyboardRemove(),reply_to_message_id=userchatidingroup
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

        scheduleconv_handler = (ConversationHandler(
            entry_points=[CommandHandler('schedule', schedule_command)],
            states={
                NAME:[MessageHandler(Filters.all, namefromuser)],
                DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday)$'), dayfromuser)],
                TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)],
                MESSAGE: [MessageHandler(Filters.all, messagefromuser)],
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        deleteconvhandler = (ConversationHandler(
            entry_points=[CommandHandler('delete', del_command)],
            states={DELETE:[MessageHandler(Filters.all, deletefromdb)],},
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        editconvhandler = (ConversationHandler(
            entry_points=[CommandHandler('edit', edit_command)],
            states={EDIT:[MessageHandler(Filters.all, editfromuser)],
                    EDITCHOICE:[MessageHandler(Filters.all, useredits)],
                    EDITINDB:[MessageHandler(Filters.all, editindb)]},
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("help", help_command))
        #dp.add_handler(CommandHandler("schedule", schedule_command))
        dp.add_handler(scheduleconv_handler)
        dp.add_handler(deleteconvhandler)
        dp.add_handler(editconvhandler)
        dp.add_handler(CommandHandler("list", list_command))
        dp.add_handler(CommandHandler("apple", scheduletest))
        dp.add_handler(CommandHandler("pear", edit_command))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        dp.add_error_handler(error)

        updater.start_polling(0)  # seconds on how often bot check for input
        updater.idle()


main()


