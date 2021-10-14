import time

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ForceReply, bot, update
import constants as keys
from telegram.ext import *
import responses as R
from datetime import datetime
import logging
import Repcheck as Rep
import GrpIDUpdate as Gid
import Dic_Lock as Loc  #Change to Com fdr getr Security ltrr
import WhitelistUpdate as wlu

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

print("Current Time =", current_time)
print("Bot started...")

#logging.basicConfig(format='%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

MASTERDELETE,EDITCON, EDITINDB, EDITCHOICE, EDIT, GRP, DELETE, NAME, DAY, TIME, MESSAGE = range(11)

def start_command(update, context):
    update.message.reply_text("Welcome to the Parakeet! \U0001F917")
    update.message.reply_text("Parakeet is a Bot to help you with your scheduling needs! A simple registration is all it takes to do so. \n\nTo get started, simply type /help to view all operational commands \U0001F4C4")

def register_command(update, context):
    global duplicatevalue
    duplicatevalue = False
    groupname = str(update.message.chat.title)
    groupchatid = update.message.chat.id
    groupchatid2 = str(update.message.chat.id)
    groupusername = update.message.from_user.username
    Gid.dict_read()
    wlu.dict_read() # reads whitelist update db
    #update.message.reply_text(groupchatid)
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in wlu.Inputs], key=lambda t: t[1]):
        if(groupchatid in chatid):
            update.message.reply_text("This is a Whitelisted Group, Checking Authorisation.....")
            if(groupusername in username):
                Gid.grpchatid = groupchatid
                Gid.grpusername = groupusername
                if (groupname == "None"):
                    Gid.grpchatname = "PM Chat"
                else:
                    Gid.grpchatname = groupname
                for chatid, grpname, username in sorted(
                        [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                    if (groupchatid == chatid and groupusername == username):
                        duplicatevalue = True
                        update.message.reply_text("You Are Already Registered! Feel Free to set a Reminder")
                if(duplicatevalue == False):
                    Gid.dict_update(Gid.Inputs)
                    update.message.reply_text("You Are an Authorised User, Your details are now Registered!")
                    userpmid = update.message.from_user.id
                    context.bot.send_message(chat_id=userpmid,
                                             text="You are now a Registered Member in  Whitelisted Group: " + groupname + ", Feel free to set Reminders!")
            elif(groupusername != username):
                update.message.reply_text("Apologies, You are not an Authorised Member")
        else:
            #update.message.reply_text("group not whitelisted")
            print("group is not whitelisted")
            Gid.grpchatid = groupchatid
            Gid.grpusername = groupusername
            if (groupname == "None"):
                Gid.grpchatname = "PM Chat"
            else:
                Gid.grpchatname = groupname

            for chatid, grpname, username in sorted(
                    [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                if(groupchatid == chatid and groupusername == username):
                    duplicatevalue = True
                    update.message.reply_text("You Are Already Registered! Feel Free to set a Reminder")


            if(duplicatevalue == False):
                Gid.dict_update(Gid.Inputs)
                update.message.reply_text("This Group is not Whitelisted, Registration Completed!")
                userpmid = update.message.from_user.id
                context.bot.send_message(chat_id=userpmid,
                                         text="You are now a Registered Member in " + Gid.grpchatname + " Feel free to set Reminders!")



def help_command(update, context):
    update.message.reply_text("This bot enables you to create, delete, and edit reminders. Please follow the commands stated below to get started! \U0001f60A \n\n"
                              "/register to register as a user to set reminders in that chat!\n"
                              "/schedule to set a new reminder\n"
                              "/list shows you a list of reminders that you have set\n"
                              "/delete allows for you to delete reminders based on the Reminder Names\n"
                              "/edit allows for you to edit existing reminders")

def list_command(update, context):
    # update.message.reply_text("hello! here are your set reminders : (work in progress)")
    #print(update.message.chat.idj)
    usernameofuser = str(update.message.from_user.username)
    Gid.dict_read()
    replylist = []
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            global userchatidingroup
            userchatidingroup = update.message.message_id
            Loc.dict_lock_read()  # read DB
            #global userchatid
            #userchatid = update.message.chat.id
            #for IDitem, DAY, Time, Text in Loc.Inputs:
            for ReminderName,IDitem, DAY, Time, Text, dbusername in sorted([(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],key=lambda t: t[1]):
                if(IDitem == dbchatid): #check userchatid against db id
                    if(usernameofuser == dbusername):
                        dbRemName = str(ReminderName)
                        dbday = str(DAY)
                        dbtime= str(Time)
                        dbmsg = str(Text)
                        dbgrpname = grpname
                        stringreply ="Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday  + "\n" + "Time: " + dbtime + "\n" +  "Message: "  + dbmsg + "\n\n" #crafting string
                        replylist.append(stringreply) #append into the list\

    if not replylist:
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else: #checking if list is empty
        update.message.reply_text("\U0001F4D1Here are your List of Reminders: \n\n" + "".join(replylist),
                                  reply_to_message_id=userchatidingroup)  # sentence + joining the list


def del_command(update,context):
    global dbchatid
    Gid.dict_read()
    namelist = []
    replylist = []
    global dbreminderchatid
    usernameofuser = update.message.from_user.username
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            dbgrpname = grpname
            global userchatidingroup
            userchatidingroup = update.message.message_id
            Loc.dict_lock_read()  # read DB
            for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                    key=lambda t: t[1]):
                if (IDitem == dbchatid):  # check userchatid against db id
                    if (usernameofuser == dbUser):
                        dbreminderchatid = IDitem
                        dbRemName = str(ReminderName)
                        dbday = str(DAY)
                        dbtime = str(Time)
                        dbmsg = str(Text)
                        stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                        replylist.append(stringreply)  # append into the list
                        namelist.append(dbRemName)  # append all names relating to this chatid into local list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist] # get each item in namelist and put in custom keyboard
        update.message.reply_text(
            "\u274C DELETE \u274C\n\n"
            "Here are your List of Reminders: \n\n" + "".join(replylist) + "\n\nPlease Select the Reminder you would like to delete according to ReminderName", reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True),)  # sentence + joining the list + custom keyboard

        return DELETE


def deletefromdb(update: Update, context: CallbackContext)-> int:
    replylist = []
    usernameofuser = update.message.from_user.username
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global usernamechoice
    usernamechoice = str(update.message.text)
    userchatidingroup = str(update.message.message_id)
    #print(dbreminderchatid)
    #Loc.usercid_r = dbreminderchatid
    print(usernamechoice)
    Loc.name_r = usernamechoice
    Loc.dict_del(Loc.Inputs)
    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            dbgrpname = grpname

            for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d["User"]) for d in Loc.Inputs], key=lambda t: t[1]):
                if (IDitem == dbchatid):  # check userchatid against db id
                    if (usernameofuser == dbUser):
                        dbRemName = str(ReminderName)
                        dbday = str(DAY)
                        dbtime = str(Time)
                        dbmsg = str(Text)
                        stringreply = "Reminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                        replylist.append(stringreply)  # append into the list


    if not replylist:
        update.message.reply_text("Your Reminder has been deleted and you currently do not have any Reminders.")
    #update.message.reply_text(userchatidingroup)
    #update.message.reply_text(userchatid)

    else:
        update.message.reply_text(
            "Your Reminder has been deleted, Here is your Updated List of Reminders: \n\n" + "".join(replylist),
            reply_to_message_id=userchatidingroup)
        userchatidingroup = str(update.message.from_user.id)

    return ConversationHandler.END


def edit_command(update, context):
    global usernameofuser
    usernameofuser = update.message.from_user.username
    Gid.dict_read()
    namelist = []
    replylist = []
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            global dbgrpname
            dbgrpname = grpname

            global userchatidingroup
            userchatidingroup = update.message.message_id
            Loc.dict_lock_read()  # read DB
            global userchatid
            userchatid = update.message.chat.id
            # for IDitem, DAY, Time, Text in Loc.Inputs:

            for ReminderName, IDitem, DAY, Time, Text, username in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs], key=lambda t: t[1]):
                if (IDitem == dbchatid):  # check userchatid against db id
                    if(usernameofuser == username):
                        dbRemName = str(ReminderName)
                        dbday = str(DAY)
                        dbtime = str(Time)
                        dbmsg = str(Text)
                        stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
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
    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            global dbgrpname
            dbgrpname = grpname
    replylist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editnameuser
    editnameuser = str(update.message.text)
    Loc.dict_lock_read()  # read DB
    for ReminderName,IDitem, DAY, Time, Text in sorted([(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Loc.Inputs],key=lambda t: t[1]):
        if(ReminderName == editnameuser):
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime = str(Time)
            dbmsg = str(Text)
            global reminderchatid
            reminderchatid = IDitem
            stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
            replylist.append(stringreply)  # append into the list
            reply_keyboard = [["Reminder Name"], ["Day"], ["Time"], ["Message"]]  # get each item in namelist and put in custom keyboard
            update.message.reply_text("Here are the details for this Reminder: \n\n" + "".join(replylist) + "\nPlease Select which field you would like to edit.",
                                      reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))  # sentence + joining the list
            return EDITCHOICE

def useredits(update: Update, context: CallbackContext)-> int:
    global usernameofuser
    usernameofuser = str(update.message.from_user.username)
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editchoiceuser
    editchoiceuser = str(update.message.text)
    if(editchoiceuser == "Time"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser + " (Format: HH:MM, e.g: 17:30)",reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if(editchoiceuser == "Day"):
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday'], ['Saturday'], ['Sunday'], ['Everyday']]
        update.message.reply_text("Please select the new details for " + editchoiceuser, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))
    if(editchoiceuser == "Reminder Name"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if (editchoiceuser == "Message"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    return EDITINDB

def editindb(update: Update, context: CallbackContext)-> str:
    global usersconfirmationedit
    global usernameofuser
    global dbgrpname
    global usernameofuser
    global dbchatid

    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            dbchatid = chatid
            global dbgrpname
            dbgrpname = grpname


    usersconfirmationedit = str(update.message.text)
    if(editchoiceuser == "Time"):

        try:
            usernameofuser = update.message.from_user.username
            time.strptime(usersconfirmationedit, '%H:%M')
            Loc.time_r = usersconfirmationedit
            Loc.usercid_r = reminderchatid
            Loc.name_r = editnameuser
            Loc.dict_lock_read()
            Loc.lock_edit_Time(Loc.Inputs)
            replylist = []
            for ReminderName, IDitem, DAY, Time, Text in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Loc.Inputs],
                    key=lambda t: t[1]):
                        if (ReminderName == editnameuser):
                            dbRemName = str(ReminderName)
                            dbday = str(DAY)
                            dbtime = str(Time)
                            dbmsg = str(Text)
                            stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                            replylist.append(stringreply)  # append into the list
                            reply_keyboard = [["Yes"], ["No"]]
                            update.message.reply_text(
                                "Would you like to continue Editing? Select Yes to continue or No to Finish Editing."
                                , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   selective=True))
        except:
            return "Sorry, Your Date Time format is wrong. Please Follow Example: 17:30"


    if(editchoiceuser == "Day"):
        usernameofuser = update.message.from_user.username
        Loc.dict_lock_read()
        Loc.day_r = usersconfirmationedit
        Loc.usercid_r = reminderchatid
        Loc.name_r = editnameuser
        Loc.lock_edit_Day(Loc.Inputs)
        replylist = []
        for ReminderName, IDitem, DAY, Time, Text in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Loc.Inputs],
                key=lambda t: t[1]):
            if (ReminderName == editnameuser):
                dbRemName = str(ReminderName)
                dbday = str(DAY)
                dbtime = str(Time)
                dbmsg = str(Text)
                stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                replylist.append(stringreply)  # append into the list
                reply_keyboard = [["Yes"], ["No"]]
                update.message.reply_text("Would you like to continue Editing? Select Yes to continue or No to Finish Editing."
                                          , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))


    if(editchoiceuser == "Reminder Name"):
        usernameofuser = update.message.from_user.username
        Loc.dict_lock_read()
        Loc.usercid_r = reminderchatid
        Loc.name_r = editnameuser
        Loc.useredit_r = usersconfirmationedit
        Loc.lock_edit_Name(Loc.Inputs)
        replylist = []

        for ReminderName, IDitem, DAY, Time, Text, username in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d["User"]) for d in Loc.Inputs],
                key=lambda t: t[1]):
            if (ReminderName == usersconfirmationedit):
                dbRemName = str(ReminderName)
                dbday = str(DAY)
                dbtime = str(Time)
                dbmsg = str(Text)
                stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                replylist.append(stringreply)  # append into the list
                reply_keyboard = [["Yes"], ["No"]]
                update.message.reply_text(
                    "Would you like to continue Editing? Select Yes to continue or No to Finish Editing."
                    , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    if(editchoiceuser == "Message"):

        usernameofuser = update.message.from_user.username
        Loc.dict_lock_read()
        Loc.text_r = usersconfirmationedit
        Loc.usercid_r = reminderchatid
        Loc.name_r = editnameuser

        Loc.lock_edit_Text(Loc.Inputs)
        replylist = []
        for ReminderName, IDitem, DAY, Time, Text in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Loc.Inputs],
                key=lambda t: t[1]):
            if (ReminderName == editnameuser):
                dbRemName = str(ReminderName)
                dbday = str(DAY)
                dbtime = str(Time)
                dbmsg = str(Text)
                stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                replylist.append(stringreply)  # append into the list
                reply_keyboard = [["Yes"], ["No"]]
                update.message.reply_text(
                    "Would you like to continue Editing? Select Yes to continue or No to Finish Editing."
                    , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return EDITCON


def editcontinue(update: Update, context: CallbackContext)-> int:
    Gid.dict_read()
    usereditcon = str(update.message.text)
    if(usereditcon == "Yes"):
        return edit_command(update,context)
    if (usereditcon == "No"):
        Loc.dict_lock_read()
        replylist = []
        for ReminderName, IDitem, DAY, Time, Text, username in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'],d['User']) for d in Loc.Inputs],
                key=lambda t: t[1]):
            for chatid, grpname, username in sorted(
                    [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                if (IDitem == chatid):
                    global dbgrpname
                    dbgrpname = grpname
            if(editchoiceuser != "Reminder Name"):
                if (ReminderName == editnameuser):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    update.message.reply_text("Here are the details for the new Reminder: \n\n" + "".join(replylist))
            elif(editchoiceuser == "Reminder Name"):
                if(ReminderName == usersconfirmationedit):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    update.message.reply_text(
                        "Here are the new details for the Reminder: \n\n" + "".join(replylist))


        return ConversationHandler.END




def schedule_command(update, context):
        global userchatidingroup
        userchatidingroup = update.message.message_id
        reply_keyboard = [['Monday','Tuesday'], ['Wednesday','Thursday'], ['Friday','Saturday'], ['Sunday','Everyday']]
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

def dayfromuser(update: Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global dayusertext
    global dayresponse
    dayusertext = str(update.message.text)
    # update.message.reply_text(dayusertext)
    dayresponse = R.day_response(dayusertext)  # process the text under responses.py
    update.message.reply_text("At  what time do you want to set the reminder? (Format: HH:MM, e.g: 17:30)", reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))  # first reply

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
    global usernamefromuser
    usernamefromuser = str(update.message.from_user.username)
     # process time given under responses.py
    update.message.reply_text("What would you like to name this Reminder?", reply_markup=ForceReply(selective=True),reply_to_message_id=userchatidingroup)
    return NAME
    #update.message.reply_text(timeresponse + "\n\nYour Reminder Message: " + messagefromuser)
    #scheduletest(update, context)
    #successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    #context.bot.send_message(chat_id=userchatid, text=successtext)


    #return ConversationHandler.END

def namefromuser(update: Update, context: CallbackContext)-> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global userchatid
    userchatid = update.message.chat.id
    global nameusertext
    nameusertext = str(update.message.text)
    usernameofuser = update.message.from_user.username
    global groupname
    groupname = str(update.message.chat.title)
    if(groupname == "None"):
        groupname = "PM Chat"
    Gid.dict_read()
    namelist = []
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser == username):
            if(groupname == grpname):
                dbchatname = "This Chat"
                namelist.append(dbchatname)
            else:
                dbchatname = str(grpname)
                namelist.append(dbchatname)

    reply_keyboard = [[name] for name in namelist]  # get each item in namelist and put in custom keyboard
    update.message.reply_text(
        "Lastly, where would you like to set this Reminder?",
        reply_to_message_id=userchatidingroup,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                         selective=True), )  # sentence + joining the list + custom keyboard
    return GRP

def grpfromuser(update: Update, context: CallbackContext)-> int:
    global chatidforschedule
    global userchatid
    global dbchatname
    userchatid = update.message.chat.id
    #update.message.reply_text(nameusertext)
    thisuserchatid = update.message.chat.id
    grpusertext = str(update.message.text)
    usernameofuser = update.message.from_user.username

    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if grpusertext == grpname:
            dbchatid = str(chatid)
            dbchatname = str(grpname)
            dbusername = str(username)
            chatidforschedule = chatid
        elif(grpusertext == "This Chat"):
             if(userchatid == chatid):
                 dbchatname = groupname
                 chatidforschedule = userchatid
    scheduletest(update, context)
    update.message.reply_text("\u2705Your Reminder has been scheduled! Here are the details: \n\n" + "Group: " + dbchatname +  "\n\nReminder Name: " + nameusertext + "\n\n" + timeresponse + "\n\nYour Reminder Message: " + messagefromuser, reply_to_message_id=userchatidingroup)
    successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    context.bot.send_message(chat_id=thisuserchatid, text=successtext)

    return ConversationHandler.END

def scheduletest(update, context):
        global chatidforschedule
        Loc.RemName = nameusertext
        Loc.IDchat = chatidforschedule
        Loc.day_r = dayusertext
        Loc.time_r = timeusertext
        Loc.text_r = messagefromuser
        Loc.username_r = usernamefromuser

        Loc.dict_lock_read()
        Loc.dict_lock_update(Loc.Inputs)
        print(Loc.Inputs)
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
    Loc.dict_lock_read() # read DB
    print("DB Reading....")
    for IDitem, DAY, Time, Text in sorted([(d['IDitem'],d['DAY'],d['Time'],d['Text']) for d in Loc.Inputs], key=lambda t: t[1] ):
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
                print("success")
        elif(DAY == 'Everyday'):
            if (tdytime == Time):
                dbchatid = str(IDitem)
                dbremindermsg = str(Text)
                Send_Reminder_Message(update, context)
                print("success")

        else:
            print(IDitem)
            print("This ChatID's Reminder is not Now ")

def error(update, context):
    print(f"update {update} caused error {context.error}")

def masterlist_command(update, context):
    global userchatidingroup
    userchatidingroup = update.message.message_id
    Loc.dict_lock_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id
    replylist = []
    for ReminderName,IDitem, DAY, Time, Text, User in sorted([(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],key=lambda t: t[1]):
        dbRemName = str(ReminderName)
        dbIDitem = str(IDitem)
        dbday = str(DAY)
        dbtime= str(Time)
        dbmsg = str(Text)
        grpname = update.message.chat.title # get group name
        dbuser = User
        Gid.dict_read()
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if(IDitem == chatid):
                chatname = grpname

        stringreply = "Group/ID: "  + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday  + "\n" + "Time: " + dbtime + "\n" + "User: " + dbuser + "\n\nMessage: "  + dbmsg + "\n\n\n\n" #crafting string


        replylist.append(stringreply) #append into the list

    if not replylist: #checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        update.message.reply_text("\U0001F4D1Here are your List of Reminders: \n\n" + "".join(replylist),reply_to_message_id=userchatidingroup) #sentence + joining the list
        update.message.reply_text(grpname)


def masterdel_command(update,context):
    global userchatidingroup
    userchatidingroup = update.message.message_id
    Loc.dict_lock_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id
    replylist = []
    namelist = []
    for ReminderName, IDitem, DAY, Time, Text, User in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        dbRemName = str(ReminderName)
        dbIDitem = str(IDitem)
        dbday = str(DAY)
        dbtime = str(Time)
        dbmsg = str(Text)
        grpname = update.message.chat.title  # get group name
        dbuser = User
        Gid.dict_read()
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if (IDitem == chatid):
                chatname = grpname

        stringreply = "Group/ID: " + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "User: " + dbuser + "\n\nMessage: " + dbmsg + "\n\n\n\n"  # crafting string

        replylist.append(stringreply)
        namelist.append(dbRemName)# append into the list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist] # get each item in namelist and put in custom keyboard
        update.message.reply_text(
            "\u274C DELETE \u274C\n\n"
            "Here are your List of Reminders: \n\n" + "".join(replylist) + "\n\nPlease Select the Reminder you would like to delete according to ReminderName", reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True),)  # sentence + joining the list + custom keyboard

        return MASTERDELETE

def masterdel_fromdb(update,context):
    replylist = []
    usernameofuser = update.message.from_user.username
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global usernamechoice
    usernamechoice = str(update.message.text)
    userchatidingroup = str(update.message.message_id)
    # print(dbreminderchatid)
    # Loc.usercid_r = dbreminderchatid
    print(usernamechoice)
    Loc.name_r = usernamechoice
    Loc.dict_del(Loc.Inputs)
    Gid.dict_read()
  #  for chatid, grpname, username in sorted(
       #     [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        #dbchatid = chatid
        #dbgrpname = grpname
        #update.message.reply_text(dbchatid)

    for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d["User"]) for d in Loc.Inputs],
            key=lambda t: t[1]):
        #if (IDitem == dbchatid):  # check userchatid against db id
        dbRemName = str(ReminderName)
        dbday = str(DAY)
        dbtime = str(Time)
        dbmsg = str(Text)
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if (IDitem == chatid):
                chatname = grpname
        stringreply = "Group: " + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n\n\n"  # crafting string
        replylist.append(stringreply)  # append into the list

    if not replylist:
        update.message.reply_text("Your Reminder has been deleted and you currently do not have any Reminders.")
    # update.message.reply_text(userchatidingroup)
    # update.message.reply_text(userchatid)

    else:
        update.message.reply_text(
            "Your Reminder has been deleted, Here is your Updated List of Reminders: \n\n" + "".join(replylist),
            reply_to_message_id=userchatidingroup)
        userchatidingroup = str(update.message.from_user.id)

    return ConversationHandler.END


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
        updater = Updater(keys.API_MAINKEY, use_context=True)
        dp = updater.dispatcher

        j = updater.job_queue
        job_minute = j.run_repeating(schedulecheck, interval=30, first=0)
        print("checking on DB started")

        scheduleconv_handler = (ConversationHandler(
            entry_points=[CommandHandler('schedule', schedule_command)],
            states={
                NAME:[MessageHandler(Filters.all, namefromuser)],
                DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Everyday)$'), dayfromuser)],
                TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)],
                MESSAGE: [MessageHandler(Filters.all, messagefromuser)],
                GRP: [MessageHandler(Filters.all, grpfromuser)],
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
                    EDITINDB:[MessageHandler(Filters.all, editindb)],
                    EDITCON:[MessageHandler(Filters.all, editcontinue)],},
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        masterdeleteconvhandler = (ConversationHandler(
            entry_points=[CommandHandler('masterdelete', masterdel_command)],
            states={MASTERDELETE: [MessageHandler(Filters.all, masterdel_fromdb)], },
            fallbacks=[CommandHandler('cancel', cancel)],
        ))

        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("help", help_command))
        #dp.add_handler(CommandHandler("schedule", schedule_command))
        dp.add_handler(scheduleconv_handler)
        dp.add_handler(deleteconvhandler)
        dp.add_handler(editconvhandler)
        dp.add_handler(masterdeleteconvhandler)
        dp.add_handler(CommandHandler("list", list_command))
        dp.add_handler(CommandHandler("apple", scheduletest))
        dp.add_handler(CommandHandler("masterlist", masterlist_command))
        dp.add_handler(CommandHandler("register", register_command))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

        dp.add_error_handler(error)

        updater.start_polling(0)  # seconds on how often bot check for input
        updater.idle()


main()


