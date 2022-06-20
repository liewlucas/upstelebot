import time

import telegram
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, ForceReply, bot, update, constants, \
    InlineKeyboardButton, InlineKeyboardMarkup
import constants as keys
from telegram.ext import *
import responses as R
from datetime import datetime
import logging
import Repcheck as Rep
import GrpIDUpdate as Gid
import Dic_Lock as Loc  # Change to Com fdr getr Security ltrr
import WhitelistUpdate as wlu
import Link_Lock as LL
import pwdb_lock as pwl
import admindb_lock as adml

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
tb = telegram.Bot(token = keys.API_J)


print("Current Time =", current_time)
print("Bot started...")

# logging.basicConfig(format='%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

EDITLINKSDETAILS,EDITLINKSTYPE,EDITLINKSCONFIRM,EDITLINKSVALIDATION,EDITLINKS,DELETELINKCONFIRM,DELETELINKVALIDATION,DELETELINKS,ADDLINKTEXT,ADDLINKNAME,ADDLINKSVALIDATION,ADDLINKS,PASSWORDVALIDATION,PASSWORDPROMPT,LINKHANDLER,MASTEREDITCON, MASTEREDITINDB, MASTEREDITCHOICE, MASTEREDIT, MASTERDELETE, EDITCON, EDITINDB, EDITCHOICE, EDIT, GRP, DELETE, NAME, DAY, TIME, MESSAGE, REGISTER = range(
    31)

"------------------STARTING COMMANDS ------------------------"


def start_command(update, context):
    keyboard = []
    text = "ILkeyboard"
    callback = "nothing"
    reply_button = InlineKeyboardMarkup(keyboard)
    keyboard.append([InlineKeyboardButton(text, callback_data=callback)])
    update.message.reply_text("Welcome to the Parakeet! \U0001F917", reply_markup= reply_button)
    update.message.reply_text(
        "Parakeet is a Bot to help you with your scheduling needs! A simple registration is all it takes to do so. \n\nTo get started, simply type /help to view all operational commands \U0001F4C4")

'---------- VIEW  LINKS -------------'

def links_command(update,context):
    pwl.pw_read()
    namelist = []
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        platoonName= str(pltname)
        namelist.append(platoonName)
    stringreply = "Please Select which Links you would like to access"
    #reply_keyboard = [['A1', 'A2'], ['B1', 'B2']]
    #n =0
    #for name in namelist:
        #namelistfirstitem = namelist[n]
        #namelistnext = namelist[n+1]
    reply_keyboard = [[name] for name in namelist]
    update.message.reply_text(stringreply, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))
    return PASSWORDPROMPT
#updated 20 jun
def linkpassword(update,context):
    global platoon
    platoon = update.message.text
    update.message.reply_text("Please Enter Password for " + platoon +  " :", reply_markup=ForceReply(selective=True))
    return PASSWORDVALIDATION

def passwordvalidation(update,context):
    userchatid= update.message.chat.id
    messageid = update.message.message_id
    passwordfromuser = update.message.text
    LL.link_read()
    pwl.pw_read()
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        if(platoon == pltname):
            if(passwordfromuser == pltpassword):
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Password Verified!")
                replylist=[]
                for linkname, pltname, linktext in sorted(
                        [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
                    nameplt = str(pltname)
                    namelink=str(linkname)
                    textlink=str(linktext)
                    if (platoon == nameplt):
                        stringreply = "Name: " + namelink + "\nLink: " + textlink + "\n\n"  # crafting string
                        replylist.append(stringreply)

                if not replylist:
                    update.message.reply_text("Apologies, Your Platoon currently does not have any links set.")
                    return ConversationHandler.END

                else:
                    replydata = "Here are the links for " + platoon + "!\n\n" + "".join(replylist)
                    update.message.reply_text(replydata)
                    return ConversationHandler.END
            else:
                update.message.reply_text("Wrong Password! Try Again!")
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Please Enter Password for " + platoon + " :",
                                          reply_markup=ForceReply(selective=True))
                return PASSWORDVALIDATION

'---------- ADD LINKS -------------'

def add_links(update,context):
    pwl.pw_read()
    namelist = []
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        platoonName = str(pltname)
        namelist.append(platoonName)
    stringreply = "Please Select which Platoon you would like to ADD links to."
    # reply_keyboard = [['A1', 'A2'], ['B1', 'B2']]
    # n =0
    # for name in namelist:
    # namelistfirstitem = namelist[n]
    # namelistnext = namelist[n+1]
    reply_keyboard = [[name] for name in namelist]
    update.message.reply_text(stringreply,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return ADDLINKS

def addlinkpassword(update,context):
    global addlinkplatoon
    addlinkplatoon = str(update.message.text)
    update.message.reply_text("Please Enter Password for " + addlinkplatoon + " :", reply_markup=ForceReply(selective=True))

    return ADDLINKSVALIDATION

def addinglinkname(update,context):
    userchatid = update.message.chat.id
    messageid = update.message.message_id
    passwordfromuser=str(update.message.text)
    LL.link_read()
    pwl.pw_read()
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        if(addlinkplatoon == pltname):
            if(passwordfromuser == pltpassword):
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Password Verified!")
                update.message.reply_text("Please enter a Friendly Name for the Link.",
                                          reply_markup=ForceReply(selective=True))
                return ADDLINKNAME
            else:
                update.message.reply_text("Wrong Password! Try Again!")
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Please Enter Password for " + addlinkplatoon + " :",
                                          reply_markup=ForceReply(selective=True))
                return ADDLINKSVALIDATION

def addinglinktext(update,context):
    global userlinkname
    userlinkname = str(update.message.text)
    update.message.reply_text("Please Enter/Paste the Link you would like to store.",reply_markup=ForceReply(selective=True))
    return ADDLINKTEXT

def addlinkdata(update,context):
    userlinktext = str(update.message.text)
    LL.linkname = userlinkname
    LL.pltname = addlinkplatoon
    LL.linktext = userlinktext
    LL.link_read()
    LL.link_update(LL.Inputs)
    replylist = []
    for linkname, pltname, linktext in sorted(
            [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
        nameplt = str(pltname)
        namelink = str(linkname)
        textlink = str(linktext)
        if (addlinkplatoon == nameplt):
            stringreply = "Name: " + namelink + "\nLink: " + textlink + "\n\n"  # crafting string
            replylist.append(stringreply)

    replydata = "Link Added! \nHere are the updated links for " + addlinkplatoon + "!\n\n" + "".join(replylist)
    update.message.reply_text(replydata)
    return ConversationHandler.END

'---------- DELETE LINKS -------------'

def delete_links(update,context):
    pwl.pw_read()
    namelist = []
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        platoonName = str(pltname)
        namelist.append(platoonName)
    stringreply = "Please Select which Platoon you would like to DELETE links for."
    # reply_keyboard = [['A1', 'A2'], ['B1', 'B2']]
    # n =0
    # for name in namelist:
    # namelistfirstitem = namelist[n]
    # namelistnext = namelist[n+1]
    reply_keyboard = [[name] for name in namelist]
    update.message.reply_text(stringreply,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return DELETELINKS

def deletelinkvalidation(update,context):
    global deletelinkplatoon
    deletelinkplatoon = str(update.message.text)
    update.message.reply_text("Please Enter Password for " + deletelinkplatoon + " :",
                              reply_markup=ForceReply(selective=True))

    return DELETELINKVALIDATION

def deletelinkconfirm(update,context):
    userchatid = update.message.chat.id
    messageid = update.message.message_id
    passwordfromuser=str(update.message.text)
    LL.link_read()
    pwl.pw_read()
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        if(deletelinkplatoon == pltname):
            if(passwordfromuser == pltpassword):
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Password Verified!")
                linklist = []
                for linkname, pltname, linktext in sorted(
                        [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
                    if(deletelinkplatoon == pltname):
                        linklist.append(linkname)
                if not linklist:
                    update.message.reply_text("Apologies, Your Platoon currently does not have any links set.")
                    return ConversationHandler.END

                else:
                    reply_keyboard = [[link] for link in linklist]
                    update.message.reply_text("Please select which link you would like to DELETE",
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))
                    return DELETELINKCONFIRM

            else:
                update.message.reply_text("Wrong Password! Try Again!")
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Please Enter Password for " + deletelinkplatoon + " :",
                                          reply_markup=ForceReply(selective=True))
                return DELETELINKVALIDATION

def deletelinkdb(update,context):
    linkfromuser = str(update.message.text)
    LL.link_read()
    LL.linkname_r = linkfromuser
    LL.link_del(LL.Inputs)
    replylist = []
    for linkname, pltname, linktext in sorted(
            [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
        nameplt = str(pltname)
        namelink = str(linkname)
        textlink = str(linktext)
        if (deletelinkplatoon == nameplt):
            stringreply = "Name: " + namelink + "\nLink: " + textlink + "\n\n"  # crafting string
            replylist.append(stringreply)

    if not replylist:
        update.message.reply_text("Your Reminder has been deleted and you currently do not have any Reminders.")
    else:
        replydata = "Link Deleted! \nHere are the updated links for " + deletelinkplatoon + "!\n\n" + "".join(replylist)
        update.message.reply_text(replydata)
    return ConversationHandler.END

'---------- EDIT LINKS -------------'

def edit_links(update,context):
    pwl.pw_read()
    namelist = []
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        platoonName = str(pltname)
        namelist.append(platoonName)
    stringreply = "Please Select which Platoon you would like to EDIT links for."
    # reply_keyboard = [['A1', 'A2'], ['B1', 'B2']]
    # n =0
    # for name in namelist:
    # namelistfirstitem = namelist[n]
    # namelistnext = namelist[n+1]
    reply_keyboard = [[name] for name in namelist]
    update.message.reply_text(stringreply,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return EDITLINKS

def editlinkvalidation(update,context):
    global editlinkplatoon
    editlinkplatoon = str(update.message.text)
    update.message.reply_text("Please Enter Password for " + editlinkplatoon + " :",
                              reply_markup=ForceReply(selective=True))

    return EDITLINKSVALIDATION

def editlinkconfirm(update,context):
    userchatid = update.message.chat.id
    messageid = update.message.message_id
    passwordfromuser = str(update.message.text)
    LL.link_read()
    pwl.pw_read()
    for pltname, pltpassword in sorted(
            [(d['PltName'], d['Password']) for d in pwl.Inputs], key=lambda t: t[1]):
        if (editlinkplatoon == pltname):
            if (passwordfromuser == pltpassword):
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Password Verified!")
                linklist = []
                for linkname, pltname, linktext in sorted(
                        [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
                    if (editlinkplatoon == pltname):
                        linklist.append(linkname)
                if not linklist:
                    update.message.reply_text("Apologies, Your Platoon currently does not have any links set.")
                    return ConversationHandler.END

                else:
                    reply_keyboard = [[link] for link in linklist]
                    update.message.reply_text("Please select which link you would like to EDIT",
                                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                               selective=True))
                    return EDITLINKSCONFIRM

            else:
                update.message.reply_text("Wrong Password! Try Again!")
                tb.deleteMessage(userchatid, messageid)
                update.message.reply_text("Please Enter Password for " + editlinkplatoon + " :",
                                          reply_markup=ForceReply(selective=True))
                return EDITLINKSVALIDATION

def editlinktype(update,context):
    global userselectlinkname
    userselectlinkname = str(update.message.text)
    reply_keyboard = [["Link Name"], ["Link Text"]]
    update.message.reply_text("Please Select which Field would you like to EDIT.",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))
    return EDITLINKSTYPE


def editlinkdetails(update,context):
    global editlinktype
    editlinktype = str(update.message.text)
    update.message.reply_text("Please Enter the new details for: " + editlinktype + ".",
                              reply_markup=ForceReply(selective=True))
    return EDITLINKSDETAILS

def editlinkdb(update,context):
    linkdetails = str(update.message.text)
    LL.link_read()
    if(editlinktype == "Link Name"):
        LL.link_read()
        LL.linkname_r = userselectlinkname
        LL.usereditlinkname = linkdetails
        LL.link_edit_Name(LL.Inputs)
        replylist = []
        for linkname, pltname, linktext in sorted(
                [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
            nameplt = str(pltname)
            namelink = str(linkname)
            textlink = str(linktext)
            if (editlinkplatoon == nameplt):
                stringreply = "Name: " + namelink + "\nLink: " + textlink + "\n\n"  # crafting string
                replylist.append(stringreply)

        if not replylist:
            update.message.reply_text("Your Platoon has no Links.")
        else:
            replydata = "Link Edited! \nHere are the updated links for " + editlinkplatoon + "!\n\n" + "".join(
                replylist)
            update.message.reply_text(replydata)

            return ConversationHandler.END

    if(editlinktype == "Link Text"):
        LL.link_read()
        LL.linkname_r= userselectlinkname
        LL.linktext_r = linkdetails
        LL.link_edit_Link(LL.Inputs)

        replylist = []
        for linkname, pltname, linktext in sorted(
                [(d['LinkName'], d['PltName'], d['LinkText']) for d in LL.Inputs], key=lambda t: t[1]):
            nameplt = str(pltname)
            namelink = str(linkname)
            textlink = str(linktext)
            if (editlinkplatoon == nameplt):
                stringreply = "Name: " + namelink + "\nLink: " + textlink + "\n\n"  # crafting string
                replylist.append(stringreply)

        if not replylist:
            update.message.reply_text("Your Platoon has no Links.")
        else:
            replydata = "Link Edited! \nHere are the updated links for " + editlinkplatoon + "!\n\n" + "".join(replylist)
            update.message.reply_text(replydata)

    return ConversationHandler.END

def Inlinelinks_command(update, context):
    keyboard =[
        [InlineKeyboardButton("A1", callback_data=LINKHANDLER),InlineKeyboardButton("A2", callback_data=str(LINKHANDLER))],
               [InlineKeyboardButton("B1", callback_data=str(LINKHANDLER)),InlineKeyboardButton("B2", callback_data=str(LINKHANDLER))]]
    reply_button = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please Select Which links you would like to view.", reply_markup=reply_button)
    #return LINKHANDLER

def inlinelinkhandler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    #query.edit_message_text(text=f"Selected option: {query.data}")
    #query.edit_message_reply_markup(reply_markup=ForceReply(selective=True) )
    return PASSWORDPROMPT

#def inlinelinkpassword(update: Update, context: CallbackContext) -> None:




def register_command(update, context):
    global duplicatevalue
    duplicatevalue = False
    global wlverification
    wlverification = False
    global userchatidingroup
    userchatidingroup = update.message.message_id
    groupname = str(update.message.chat.title)
    groupchatid = update.message.chat.id
    #groupchatid2 = str(update.message.chat.id)
    groupusername = str(update.message.from_user.username)
    Gid.dict_read()
    wlu.wl_read()  # reads whitelist update db
    # update.message.reply_text(groupchatid)
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in wlu.Inputs], key=lambda t: t[1]):
        if groupchatid == chatid:
            wlverification = True
            update.message.reply_text("This is a Whitelisted Group! Verifying Authorisation...")

    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in wlu.Inputs], key=lambda t: t[1]):
        if wlverification == True and groupchatid == chatid and groupusername in username:
            Gid.grpchatid = groupchatid
            Gid.grpusername = groupusername
            if (groupname == "None"):
                Gid.grpchatname = "PM Chat"
            else:
                Gid.grpchatname = groupname
            for chatid, grpname, username in sorted(
                    [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                if (groupchatid == chatid) and (groupusername in username):
                    duplicatevalue = True

            if duplicatevalue == False:
                Gid.dict_update(Gid.Inputs)
                update.message.reply_text("You Are an Authorised User, Your details are now Registered!")
                userpmid = update.message.from_user.id
                context.bot.send_message(chat_id=userpmid,
                                         text="You are now a Registered Member in  Whitelisted Group: " + groupname + ", Feel free to set Reminders!")

            else:
                update.message.reply_text("You Are Already Registered! Feel Free to set a Reminder")

        elif wlverification == True and groupusername not in username:
            update.message.reply_text("Apologies, You are not an Authorised Member in this group.")


    if wlverification == False:
        print("Group is not whitelisted")
        print(groupchatid)
        print(wlu.Inputs)
        Gid.grpchatid = groupchatid
        Gid.grpusername = groupusername
        if (groupname == "None"):
            Gid.grpchatname = "PM Chat"
        else:
            Gid.grpchatname = groupname

        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if groupchatid == chatid and groupusername in username:
                duplicatevalue = True

        if duplicatevalue == False:
            Gid.dict_update(Gid.Inputs)
            update.message.reply_text("This Group is not Whitelisted, Registration Completed!")
            userpmid = update.message.from_user.id
            context.bot.send_message(chat_id=userpmid,
                                     text="You are now a Registered Member in " + Gid.grpchatname + " Feel free to set Reminders!")

        else:
            update.message.reply_text("You Are Already Registered! Feel Free to set a Reminder")




def help_command(update, context):
    update.message.reply_text(
        "This bot enables you to create, delete, and edit reminders. Please follow the commands stated below to get started! \U0001f60A \n\n"
        "/register to register as a user to set reminders in that chat!\n"
        "/schedule to set a new reminder\n"
        "/list shows you a list of reminders that you have set\n"
        "/delete allows for you to delete reminders based on the Reminder Names\n"
        "/edit allows for you to edit existing reminders")


def list_command(update, context):
    # update.message.reply_text("hello! here are your set reminders : (work in progress)")
    # print(update.message.chat.idj)
    usernameofuser = str(update.message.from_user.username)
    Gid.dict_read()
    replylist = []
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser in username):
            dbchatid = chatid
            global userchatidingroup
            userchatidingroup = update.message.message_id
            Loc.dict_lock_read()  # read DB
            # global userchatid
            # userchatid = update.message.chat.id
            # for IDitem, DAY, Time, Text in Loc.Inputs:
            for ReminderName, IDitem, DAY, Time, Text, dbusername in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                    key=lambda t: t[1]):
                if (IDitem == dbchatid):  # check userchatid against db id
                    if (usernameofuser == dbusername):
                        dbRemName = str(ReminderName)
                        dbday = str(DAY)
                        dbtime = str(Time)
                        dbmsg = str(Text)
                        dbgrpname = grpname
                        stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                        replylist.append(stringreply)  # append into the list\

    if not replylist:
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:  # checking if list is empty
        print(replylist)
        replydata = "\U0001F4D1Here are your List of Reminders: \n\n" + "".join(replylist)
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")
            update.message.reply_text(msg,
                                      reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs,
                                      reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup)  # sentence + joining the list


"------------------DELETING COMMANDS ------------------------"


def del_command(update, context):
    global dbchatid
    Gid.dict_read()
    namelist = []
    replylist = []
    global dbreminderchatid
    usernameofuser = update.message.from_user.username
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser in username):
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
        reply_keyboard = [[name] for name in namelist]  # get each item in namelist and put in custom keyboard
        #print(reply_keyboard)
        replydata = "\u274C DELETE \u274C\n\n" "Here are your List of Reminders: \n\n\n" + "".join(
            replylist) + "\n\u274C DELETE \u274C\nPlease Select the Reminder you would like to delete according to ReminderName"
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")

            update.message.reply_text(msg, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                            selective=True), )  # sentence + joining the list + custom keyboard
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                                 selective=True), )  # sentence + joining the list + custom keyboard

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                                 selective=True),)  # sentence + joining the list

        return DELETE


def deletefromdb(update: Update, context: CallbackContext) -> int:
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
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if usernameofuser in username:
            dbchatid = chatid
            dbgrpname = grpname

            for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d["User"]) for d in Loc.Inputs],
                    key=lambda t: t[1]):
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

    else:
        replydata = "Your Reminder has been deleted, Here is your Updated List of Reminders: \n\n" + "".join(replylist)
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")
            update.message.reply_text(msg,
                                      reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs,
                                      reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup)  # sentence + joining the list
            userchatidingroup = str(update.message.from_user.id)

    return ConversationHandler.END


"------------------EDITING COMMANDS ------------------------"


def edit_command(update, context):
    global usernameofuser
    usernameofuser = update.message.from_user.username
    Gid.dict_read()
    namelist = []
    replylist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
    Loc.dict_lock_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id
    # for IDitem, DAY, Time, Text in Loc.Inputs:
    for ReminderName, IDitem, DAY, Time, Text, username in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        if (usernameofuser in username):
            for chatid, grpname, username in sorted([(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs],
                                                    key=lambda t: t[1]):
                if (IDitem == chatid):
                    dbchatid = chatid
                    global dbgrpname
                    dbgrpname = grpname
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
        replydata = "\U0001F4DD EDITING \U0001F4DD \n\n" "Here are your List of Reminders: \n\n" + "".join(replylist) + \
                    "\n\n" + "\U0001F4DD EDIT \U0001F4DD\nPlease Select the Reminder you would like to Edit"
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")
            update.message.reply_text(msg,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # sentence + joining the list
            # userchatidingroup = str(update.message.from_user.id)

        return EDIT


def editfromuser(update: Update, context: CallbackContext) -> int:
    Gid.dict_read()
    replylist = []
    print("Hi")
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editnameuser
    editnameuser = str(update.message.text)
    Loc.dict_lock_read()  # read DB
    for ReminderName, IDitem, DAY, Time, Text, usernamedb in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):

            if usernamedb in username and IDitem == chatid:
                dbchatid = chatid
                global dbgrpname
                dbgrpname = grpname
        if (ReminderName == editnameuser):
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime = str(Time)
            dbmsg = str(Text)
            global reminderchatid
            reminderchatid = IDitem
            stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
            replylist.append(stringreply)  # append into the list
            reply_keyboard = [["Reminder Name"], ["Day"], ["Time"],
                              ["Message"]]  # get each item in namelist and put in custom keyboard
            replydata = "Here are the details for this Reminder: \n\n" + "".join(
                replylist) + "\nPlease Select which field you would like to edit."

            update.message.reply_text(replydata,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # sentence + joining the list
            # userchatidingroup = str(update.message.from_user.id)
            return EDITCHOICE


def useredits(update: Update, context: CallbackContext) -> int:
    global usernameofuser
    usernameofuser = str(update.message.from_user.username)
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editchoiceuser
    editchoiceuser = str(update.message.text)
    if (editchoiceuser == "Time"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser + " (Format: HH:MM, e.g: 17:30)",
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if (editchoiceuser == "Day"):
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday'], ['Saturday'], ['Sunday'],
                          ['Everyday']]
        update.message.reply_text("Please select the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   selective=True))
    if (editchoiceuser == "Reminder Name"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if (editchoiceuser == "Message"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    return EDITINDB


def editindb(update: Update, context: CallbackContext) -> str:
    global usersconfirmationedit
    global usernameofuser
    global dbgrpname
    global usernameofuser
    global dbchatid

    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser in username):
            dbchatid = chatid
            global dbgrpname
            dbgrpname = grpname

    usersconfirmationedit = str(update.message.text)
    if (editchoiceuser == "Time"):

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
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                           selective=True))
        except:
            return "Sorry, Your Date Time format is wrong. Please Follow Example: 17:30"

    if (editchoiceuser == "Day"):
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
                reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                update.message.reply_text(
                    "Would you like to continue Editing? Please select the option you would like to proceed with."
                    , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    if (editchoiceuser == "Reminder Name"):
        usernameofuser = update.message.from_user.username
        if len(usersconfirmationedit) > constants.MAX_MESSAGE_LENGTH - 2500:
            update.message.reply_text(
                "Error! Reminder Name is too long. Please reduce the length of the reminder name and send again.",
                reply_to_message_id=userchatidingroup)
            return ConversationHandler.END
        else:
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
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    if (editchoiceuser == "Message"):

        usernameofuser = update.message.from_user.username
        if len(usersconfirmationedit) > constants.MAX_MESSAGE_LENGTH - 500:
            update.message.reply_text(
                "Error! Scheduled Message is too long. Please reduce the length of the reminder message and send again.",
                reply_to_message_id=userchatidingroup)
            return ConversationHandler.END

        else:
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
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return EDITCON


def editcontinue(update: Update, context: CallbackContext) -> int:
    Gid.dict_read()
    usereditcon = str(update.message.text)
    if (usereditcon == "Continue Editing"):
        return edit_command(update, context)
    if (usereditcon == "Finish Editing"):
        Loc.dict_lock_read()
        replylist = []
        for ReminderName, IDitem, DAY, Time, Text, usernamedb in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                key=lambda t: t[1]):  
            for chatid, grpname, username in sorted(
                    [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                if usernamedb in username and IDitem == chatid:
                    global dbgrpname
                    dbgrpname = grpname
            if (editchoiceuser != "Reminder Name"):
                if (ReminderName == editnameuser):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    update.message.reply_text("Here are the details for the new Reminder: \n\n" + "".join(replylist))
            elif (editchoiceuser == "Reminder Name"):
                if (ReminderName == usersconfirmationedit):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    replydata = "Here are the new details for the Reminder: \n\n" + "".join(replylist)
                    msg = replydata
                    sub_msgs = ""
                    if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
                        while len(msg):
                            split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                                '\n')  # Finding point within Bytes Limit(4096) to split message
                            if split_point != -1:
                                sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                                msg = msg[:split_point]  # Initial Message Section
                                break  # Ending the while Loop

                            else:
                                print("Message Error!")
                        update.message.reply_text(msg,
                                                  reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
                        # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
                        update.message.reply_text(sub_msgs,
                                                  reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

                    else:
                        update.message.reply_text(replydata,
                                                  reply_to_message_id=userchatidingroup)  # sentence + joining the list
                        # userchatidingroup = str(update.message.from_user.id)

        return ConversationHandler.END


"------------------SCHEDULING COMMANDS ------------------------"


def schedule_command(update, context):
    global userchatidingroup
    userchatidingroup = update.message.message_id
    reply_keyboard = [['Monday', 'Tuesday'], ['Wednesday', 'Thursday'], ['Friday', 'Saturday'], ['Sunday', 'Everyday']]
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
    update.message.reply_text("At  what time do you want to set the reminder? (Format: HH:MM, e.g: 17:30)",
                              reply_to_message_id=userchatidingroup,
                              reply_markup=ForceReply(selective=True))  # first reply

    return TIME


def timefromuser(update: Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global timeusertext
    timeusertext = str(update.message.text)
    # update.message.reply_text(timeusertext)
    global timeresponse
    timeresponse = R.time_response(timeusertext)  # process time given under responses.py
    update.message.reply_text("What would you like the Reminder Message to be?", reply_to_message_id=userchatidingroup,
                              reply_markup=ForceReply(selective=True), )
    # update.message.reply_text(timeresponse)  # first reply
    # scheduletest(update, context)

    return MESSAGE


def messagefromuser(update: Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global userchatid
    userchatid = update.message.chat.id
    global messagefromuser
    messagefromuser = str(update.message.text)
    if len(messagefromuser) > constants.MAX_MESSAGE_LENGTH-500:
        update.message.reply_text("Error! Scheduled Message is too long. Please reduce the length of the reminder message and send again.", reply_to_message_id=userchatidingroup)
        return ConversationHandler.END

    else:
        global usernamefromuser
        usernamefromuser = str(update.message.from_user.username)
        # process time given under responses.py
        update.message.reply_text("What would you like to name this Reminder?", reply_markup=ForceReply(selective=True),
                                  reply_to_message_id=userchatidingroup)
        return NAME
        # update.message.reply_text(timeresponse + "\n\nYour Reminder Message: " + messagefromuser)
        # scheduletest(update, context)
        # successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
        # context.bot.send_message(chat_id=userchatid, text=successtext)

        # return ConversationHandler.END


def namefromuser(update: Update, context: CallbackContext) -> int:
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global userchatid
    userchatid = update.message.chat.id
    global nameusertext
    nameusertext = str(update.message.text)
    usernameofuser = update.message.from_user.username
    if len(nameusertext) > constants.MAX_MESSAGE_LENGTH - 2500:
        update.message.reply_text("Error! Reminder Name is too long. Please reduce the length of the reminder name and send again.", reply_to_message_id=userchatidingroup)
        return ConversationHandler.END

    else:
        global groupname
        groupname = str(update.message.chat.title)
        if (groupname == "None"):
            groupname = "PM Chat"
        Gid.dict_read()
        namelist = []
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if (usernameofuser in username):
                if (groupname == grpname):
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


def grpfromuser(update: Update, context: CallbackContext) -> int:
    global chatidforschedule
    global userchatid
    global dbchatname
    userchatid = update.message.chat.id
    # update.message.reply_text(nameusertext)
    thisuserchatid = update.message.chat.id
    grpusertext = str(update.message.text)
    usernameofuser = update.message.from_user.username

    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if grpusertext == grpname:
            dbchatname = str(grpname)
            chatidforschedule = chatid
        elif (grpusertext == "This Chat"):
            if (userchatid == chatid):
                dbchatname = groupname
                chatidforschedule = userchatid
    scheduletest(update, context)
    update.message.reply_text(
        "\u2705Your Reminder has been scheduled! Here are the details: \n\n" + "Group: " + dbchatname + "\n\nReminder Name: " + nameusertext + "\n\n" + timeresponse + "\n\nYour Reminder Message: " + messagefromuser,
        reply_to_message_id=userchatidingroup)
    successtext = 'Feel free to type /schedule again if you want to set another reminder.\nAlternatively, you could type /list to view all your set reminders'
    context.bot.send_message(chat_id=thisuserchatid, text=successtext)

    return ConversationHandler.END


"------------------PASSIVE/RUNNING COMMANDS------------------------"


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
    # global userchatid
    # userchatid2 = str(userchatid)
    bot = context.bot
    global dbchatid
    context.bot.send_message(chat_id=dbchatid, text=remindertext)
    # update.message.reply_text(text=remindertext)
    # print(userchatid2)


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Set reminder cancelled. Hope to talk to you again. Bye!', reply_markup=ReplyKeyboardRemove(),
        reply_to_message_id=userchatidingroup
    )

    return ConversationHandler.END


def handle_message(update, context):
    # global text
    text = str(update.message.text)  # .lower() #receive text from user


def schedulecheck(context: CallbackContext):
    Loc.dict_lock_read()  # read DB
    print("DB Reading....")
    for IDitem, DAY, Time, Text in sorted([(d['IDitem'], d['DAY'], d['Time'], d['Text']) for d in Loc.Inputs],
                                          key=lambda t: t[1]):
        now = datetime.now()
        today = now.strftime("%A")  # return today's day
        tdytime = now.strftime("%H:%M")
        if (today == DAY):
            if (tdytime == Time):
                global dbchatid
                dbchatid = str(IDitem)
                global dbremindermsg
                dbremindermsg = str(Text)
                Send_Reminder_Message(update, context)
                print("success")
        elif (DAY == 'Everyday'):
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


'-------------------- MASTER COMMANDS ----------------------------'


def masterlist_command(update, context):
    global userchatidingroup
    userchatidingroup = update.message.message_id
    Loc.dict_lock_read()  # read DB
    global userchatid
    global chatname
    userchatid = update.message.chat.id
    print("Test1")
    replylist = []
    Gid.dict_read()

    for ReminderName, IDitem, DAY, Time, Text, User in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        dbRemName = str(ReminderName)
        dbday = str(DAY)
        dbtime = str(Time)
        dbmsg = str(Text)
        grpname = update.message.chat.title  # get group name
        dbuser = str(User)
        # Gid.dict_read()
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if dbuser in username and IDitem == chatid:
                chatname = grpname

        stringreply = "Group/ID: " + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "User: " + dbuser + "\n\nMessage: " + dbmsg + "\n\n\n\n"  # crafting string

        replylist.append(stringreply)  # append into the list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        replydata = "\U0001F4D1Here are your List of Reminders: \n\n" + "".join(replylist)
        msg = replydata
        # sub_msgs = ""
        # sub_msgs_s = ""
        # sub_msgs_con = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message exceeds Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section

                    # Sending Initial Section (Before Telegram Message Limit)
                    update.message.reply_text(msg,
                                              reply_to_message_id=userchatidingroup)

                    # Checking if Subsequent Section(s) are longer than Telegram Message Limit
                    while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:
                        split_point = sub_msgs[:constants.MAX_MESSAGE_LENGTH].rfind(
                            '\n')  # Finding point within Bytes Limit(4096) to split message
                        if split_point != -1:
                            sub_msgs_con = (sub_msgs[split_point:])  # Subsequent Message Section(s)
                            sub_msgs_s = sub_msgs[:split_point]

                            # Sending Second Message Section
                            update.message.reply_text(sub_msgs_s,
                                                      reply_to_message_id=userchatidingroup)

                            if len(sub_msgs_con) > constants.MAX_MESSAGE_LENGTH:
                                sub_msgs = sub_msgs_con

                            else:
                                # Sending Subsequent Message Section(s)
                                # print("HIYO")
                                update.message.reply_text(sub_msgs_con,
                                                          reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)
                                break  # Ending the while Loop
                        else:
                            print("Message Error!")
                    break  # Ending the while Loop
                else:
                    print("Message Error!")

            # update.message.reply_text(msg,
            # reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            # update.message.reply_text(sub_msgs,
            # reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup)  # sentence + joining the list


def masterdel_command(update, context):
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
            if dbuser in username and IDitem == chatid:
                print(username)
                print(grpname)
                chatname = grpname

        stringreply = "Group/ID: " + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "User: " + dbuser + "\n\nMessage: " + dbmsg + "\n\n\n\n"  # crafting string

        replylist.append(stringreply)
        namelist.append(dbRemName)  # append into the list

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist]  # get each item in namelist and put in custom keyboard
        replydata = "\u274C DELETE \u274C\n\n" "Here are your List of Reminders: \n\n\n" + "".join(
            replylist) + "\n\u274C DELETE \u274C\nPlease Select the Reminder you would like to delete according to ReminderName"
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")
            update.message.reply_text(msg, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                            selective=True), )  # sentence + joining the list + custom keyboard
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                            selective=True), )  # sentence + joining the list + custom keyboard

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                                 selective=True),)  # sentence + joining the list

        # .join(replylist)
        return MASTERDELETE


def masterdel_fromdb(update, context):
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
    # dbchatid = chatid
    # dbgrpname = grpname
    # update.message.reply_text(dbchatid)

    for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d["User"]) for d in Loc.Inputs],
            key=lambda t: t[1]):
        # if (IDitem == dbchatid):  # check userchatid against db id
        dbRemName = str(ReminderName)
        dbday = str(DAY)
        dbtime = str(Time)
        dbmsg = str(Text)
        usernamedb = dbUser
        for chatid, grpname, username in sorted(
                [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
            if usernamedb in username and IDitem == chatid:
                chatname = grpname
        stringreply = "Group: " + chatname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n\n\n"  # crafting string
        replylist.append(stringreply)  # append into the list

    if not replylist:
        update.message.reply_text("Your Reminder has been deleted and you currently do not have any Reminders.")

    else:
        replydata = "Your Reminder has been deleted, Here is your Updated List of Reminders: \n\n" + "".join(replylist)
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    break  # Ending the while Loop

                else:
                    print("Message Error!")
            update.message.reply_text(msg,
                                      reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs,
                                      reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup)  # sentence + joining the list
            #userchatidingroup = str(update.message.from_user.id)

    return ConversationHandler.END


def masteredit_command(update, context):
    global usernameofuser
    usernameofuser = update.message.from_user.username
    Gid.dict_read()
    namelist = []
    replylist = []
    print(Gid.Inputs)

    global userchatidingroup
    userchatidingroup = update.message.message_id
    Loc.dict_lock_read()  # read DB
    global userchatid
    userchatid = update.message.chat.id

    for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        # if (IDitem == chatid):  # check userchatid against db id
        dbRemName = str(ReminderName)
        dbday = str(DAY)
        dbtime = str(Time)
        dbmsg = str(Text)
        usernamedb = dbUser
        print(usernamedb)
        for chatid, grpname, username in sorted([(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs],
                                                key=lambda t: t[1]):
            if usernamedb in username and IDitem == chatid:
                global dbgrpname
                dbgrpname = grpname
                print(dbgrpname)
                stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                replylist.append(stringreply)  # append into the list
                namelist.append(dbRemName)  # append all names relating to this chatid into local list
                #print(dbRemName)

    if not replylist:  # checking if list is empty
        update.message.reply_text("Sorry, you do not appear to have set any Reminders")
    else:
        reply_keyboard = [[name] for name in namelist]  # get each item in namelist and put in custom keyboard
        print(reply_keyboard)
        replydata = "\U0001F4DD EDITING \U0001F4DD \n\n" "Here are your List of Reminders: \n\n" + "".join(replylist) + \
                        "\n\n" + "\U0001F4DD EDIT \U0001F4DD\nPlease Select the Reminder you would like to Edit"
        msg = replydata
        sub_msgs = ""
        if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
            while len(msg):
                split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                    '\n')  # Finding point within Bytes Limit(4096) to split message
                if split_point != -1:
                    sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                    msg = msg[:split_point]  # Initial Message Section
                    #break  # Ending the while Loop

                else:
                    print("Message Error!")

            update.message.reply_text(msg,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # Sending Initial Section (Before Telegram Message Limit)
            # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
            update.message.reply_text(sub_msgs,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )   # Sending Subsequent Message Section(s)

        else:
            update.message.reply_text(replydata, reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # sentence + joining the list
            #userchatidingroup = str(update.message.from_user.id)

        return MASTEREDIT


def mastereditfromuser(update: Update, context: CallbackContext) -> int:
    Gid.dict_read()
    replylist = []
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editnameuser
    editnameuser = str(update.message.text)
    Loc.dict_lock_read()  # read DB
    for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
            [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
            key=lambda t: t[1]):
        for chatid, grpname, username in sorted([(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs],
                                                key=lambda t: t[1]):
            if dbUser in username and IDitem == chatid:
                #dbchatid = chatid
                global dbgrpname
                dbgrpname = grpname


        if (ReminderName == editnameuser):
            dbRemName = str(ReminderName)
            dbday = str(DAY)
            dbtime = str(Time)
            dbmsg = str(Text)
            global reminderchatid
            reminderchatid = IDitem
            stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
            replylist.append(stringreply)  # append into the list
            reply_keyboard = [["Reminder Name"], ["Day"], ["Time"],
                              ["Message"]]  # get each item in namelist and put in custom keyboard
            replydata = "Here are the details for this Reminder: \n\n" + "".join(
                replylist) + "\nPlease Select which field you would like to edit."
            update.message.reply_text(replydata,
                                      reply_to_message_id=userchatidingroup,
                                      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                       selective=True), )  # sentence + joining the list
            # userchatidingroup = str(update.message.from_user.id)


            return MASTEREDITCHOICE


def masteruseredits(update: Update, context: CallbackContext) -> int:
    global usernameofuser
    usernameofuser = str(update.message.from_user.username)
    global userchatidingroup
    userchatidingroup = update.message.message_id
    global editchoiceuser
    editchoiceuser = str(update.message.text)
    if (editchoiceuser == "Time"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser + " (Format: HH:MM, e.g: 17:30)",
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if (editchoiceuser == "Day"):
        reply_keyboard = [['Monday'], ['Tuesday'], ['Wednesday'], ['Thursday'], ['Friday'], ['Saturday'], ['Sunday'],
                          ['Everyday']]
        update.message.reply_text("Please select the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup,
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                   selective=True))
    if (editchoiceuser == "Reminder Name"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    if (editchoiceuser == "Message"):
        update.message.reply_text("Please Enter the new details for " + editchoiceuser,
                                  reply_to_message_id=userchatidingroup, reply_markup=ForceReply(selective=True))
    return MASTEREDITINDB


def mastereditindb(update: Update, context: CallbackContext) -> str:
    global usersconfirmationedit
    global usernameofuser
    global dbgrpname
    global usernameofuser
    global dbchatid

    Gid.dict_read()
    for chatid, grpname, username in sorted(
            [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
        if (usernameofuser in username):
            dbchatid = chatid
            global dbgrpname
            dbgrpname = grpname

    usersconfirmationedit = str(update.message.text)
    if (editchoiceuser == "Time"):

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
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                           selective=True))
        except:
            return "Sorry, Your Date Time format is wrong. Please Follow Example: 17:30"

    if (editchoiceuser == "Day"):
        usernameofuser = update.message.from_user.username
        Loc.dict_lock_read()
        Loc.day_r = usersconfirmationedit
        Loc.usercid_r = reminderchatid
        Loc.name_r = editnameuser
        Loc.lock_edit_Day(Loc.Inputs)
        replylist = []
        print("hi")
        for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                key=lambda t: t[1]):
            if (ReminderName == editnameuser):
                dbRemName = str(ReminderName)
                dbday = str(DAY)
                dbtime = str(Time)
                dbmsg = str(Text)
                stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                replylist.append(stringreply)  # append into the list
                print(stringreply)
                reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                update.message.reply_text(
                    "Would you like to continue Editing? Please select the option you would like to proceed with."
                    , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    if (editchoiceuser == "Reminder Name"):
        usernameofuser = update.message.from_user.username
        if len(usersconfirmationedit) > constants.MAX_MESSAGE_LENGTH - 2500:
            update.message.reply_text(
                "Error! Scheduled Reminder Name is too long. Please reduce the length of the reminder name and send again.",
                reply_to_message_id=userchatidingroup)
            return ConversationHandler.END

        else:
            Loc.dict_lock_read()
            Loc.usercid_r = reminderchatid
            Loc.name_r = editnameuser
            Loc.useredit_r = usersconfirmationedit
            Loc.lock_edit_Name(Loc.Inputs)
            replylist = []

            for ReminderName, IDitem, DAY, Time, Text, username in sorted(
                    [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                    key=lambda t: t[1]):
                if (ReminderName == usersconfirmationedit):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    if (editchoiceuser == "Message"):
        usernameofuser = update.message.from_user.username
        if len(usersconfirmationedit) > constants.MAX_MESSAGE_LENGTH - 500:
            update.message.reply_text(
                "Error! Scheduled Message is too long. Please reduce the length of the reminder message and send again.",
                reply_to_message_id=userchatidingroup)
            return ConversationHandler.END

        else:
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
                    reply_keyboard = [["Continue Editing"], ["Finish Editing"]]
                    update.message.reply_text(
                        "Would you like to continue Editing? Please select the option you would like to proceed with."
                        , reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, selective=True))

    return MASTEREDITCON


def mastereditcontinue(update: Update, context: CallbackContext) -> int:
    Gid.dict_read()
    usereditcon = str(update.message.text)
    if (usereditcon == "Continue Editing"):
        return masteredit_command(update, context)
    if (usereditcon == "Finish Editing"):
        Loc.dict_lock_read()
        replylist = []
        print("Hi")
        for ReminderName, IDitem, DAY, Time, Text, dbUser in sorted(
                [(d['ReminderName'], d['IDitem'], d['DAY'], d['Time'], d['Text'], d['User']) for d in Loc.Inputs],
                key=lambda t: t[1]):
            for chatid, grpname, username in sorted(
                    [(d['CHATID'], d['GRPNAME'], d['USER']) for d in Gid.Inputs], key=lambda t: t[1]):
                if dbUser in username and IDitem == chatid:
                    global dbgrpname
                    dbgrpname = grpname
            if (editchoiceuser != "Reminder Name"):
                if (ReminderName == editnameuser):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)
                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    update.message.reply_text("Here are the details for the new Reminder: \n\n" + "".join(replylist))
            elif (editchoiceuser == "Reminder Name"):
                if (ReminderName == usersconfirmationedit):
                    dbRemName = str(ReminderName)
                    dbday = str(DAY)
                    dbtime = str(Time)
                    dbmsg = str(Text)

                    stringreply = "Group: " + dbgrpname + "\nReminder Name: " + dbRemName + "\nDay: " + dbday + "\n" + "Time: " + dbtime + "\n" + "Message: " + dbmsg + "\n\n"  # crafting string
                    replylist.append(stringreply)  # append into the list
                    replydata = "Here are the new details for the Reminder: \n\n" + "".join(replylist)
                    msg = replydata
                    sub_msgs = ""
                    if len(replydata) > constants.MAX_MESSAGE_LENGTH:  # Checking whether Message excedes Telegram's Bytes Limit(4096)
                        while len(msg):
                            split_point = msg[:constants.MAX_MESSAGE_LENGTH].rfind(
                                '\n')  # Finding point within Bytes Limit(4096) to split message
                            if split_point != -1:
                                sub_msgs = (msg[split_point:])  # Subsequent Message Section(s)
                                msg = msg[:split_point]  # Initial Message Section
                                break  # Ending the while Loop

                            else:
                                print("Message Error!")
                        update.message.reply_text(msg,
                                                  reply_to_message_id=userchatidingroup)  # Sending Initial Section (Before Telegram Message Limit)
                        # Do "while len(sub_msgs) > constants.MAX_MESSAGE_LENGTH:" check here for repeating loops of msg
                        update.message.reply_text(sub_msgs,
                                                  reply_to_message_id=userchatidingroup)  # Sending Subsequent Message Section(s)

                    else:
                        update.message.reply_text(replydata, reply_to_message_id=userchatidingroup)  # sentence + joining the list
                        # userchatidingroup = str(update.message.from_user.id)


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



def main():
    updater = Updater(keys.API_J, use_context=True)
    dp = updater.dispatcher

    j = updater.job_queue
    job_minute = j.run_repeating(schedulecheck, interval=55, first=0)
    print("checking on DB started")


    scheduleconv_handler = (ConversationHandler(
        entry_points=[CommandHandler('schedule', schedule_command)],
        states={
            NAME: [MessageHandler(Filters.all, namefromuser)],
            DAY: [MessageHandler(Filters.regex('^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Everyday)$'),
                                 dayfromuser)],
            TIME: [MessageHandler(Filters.regex('^([01]\d|2[0-3]):([0-5]\d)$'), timefromuser)],
            MESSAGE: [MessageHandler(Filters.all, messagefromuser)],
            GRP: [MessageHandler(Filters.all, grpfromuser)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    deleteconvhandler = (ConversationHandler(
        entry_points=[CommandHandler('delete', del_command)],
        states={DELETE: [MessageHandler(Filters.all, deletefromdb)], },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    editconvhandler = (ConversationHandler(
        entry_points=[CommandHandler('edit', edit_command)],
        states={EDIT: [MessageHandler(Filters.all, editfromuser)],
                EDITCHOICE: [MessageHandler(Filters.all, useredits)],
                EDITINDB: [MessageHandler(Filters.all, editindb)],
                EDITCON: [MessageHandler(Filters.all, editcontinue)], },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    masterdeleteconvhandler = (ConversationHandler(
        entry_points=[CommandHandler('masterdelete', masterdel_command)],
        states={MASTERDELETE: [MessageHandler(Filters.all, masterdel_fromdb)], },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    mastereditconvhandler = (ConversationHandler(
        entry_points=[CommandHandler('masteredit', masteredit_command)],
        states={MASTEREDIT: [MessageHandler(Filters.all, mastereditfromuser)],
                MASTEREDITCHOICE: [MessageHandler(Filters.all, masteruseredits)],
                MASTEREDITINDB: [MessageHandler(Filters.all, mastereditindb)],
                MASTEREDITCON: [MessageHandler(Filters.all, mastereditcontinue)], },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    linkshandler = (ConversationHandler(
        entry_points=[CommandHandler('links', links_command)],
        states={PASSWORDPROMPT: [MessageHandler(Filters.all, linkpassword)],
                PASSWORDVALIDATION:[MessageHandler(Filters.all, passwordvalidation)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    addlinkhandler = (ConversationHandler(
        entry_points=[CommandHandler('addlinks', add_links)],
        states={ADDLINKS: [MessageHandler(Filters.all, addlinkpassword)],
                ADDLINKSVALIDATION:[MessageHandler(Filters.all, addinglinkname)],
                ADDLINKNAME:[MessageHandler(Filters.all, addinglinktext)],
                ADDLINKTEXT:[MessageHandler(Filters.all, addlinkdata)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    ))
    deletelinkhandler = (ConversationHandler(
        entry_points=[CommandHandler('deletelinks', delete_links)],
        states={DELETELINKS: [MessageHandler(Filters.all, deletelinkvalidation)],
                DELETELINKVALIDATION: [MessageHandler(Filters.all, deletelinkconfirm)],
                DELETELINKCONFIRM: [MessageHandler(Filters.all, deletelinkdb)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    ))
    editlinkhandler = (ConversationHandler(
        entry_points=[CommandHandler('editlinks', edit_links)],
        states={EDITLINKS: [MessageHandler(Filters.all, editlinkvalidation)],
                EDITLINKSVALIDATION: [MessageHandler(Filters.all, editlinkconfirm)],
                EDITLINKSCONFIRM: [MessageHandler(Filters.all, editlinktype)],
                EDITLINKSTYPE:[MessageHandler(Filters.all, editlinkdetails)],
                EDITLINKSDETAILS: [MessageHandler(Filters.all, editlinkdb)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    # dp.add_handler(CommandHandler("schedule", schedule_command))
    dp.add_handler(scheduleconv_handler)
    dp.add_handler(deleteconvhandler)
    dp.add_handler(editconvhandler)
    dp.add_handler(masterdeleteconvhandler)
    dp.add_handler(mastereditconvhandler)
    dp.add_handler(linkshandler)
    dp.add_handler(addlinkhandler)
    dp.add_handler(deletelinkhandler)
    dp.add_handler(editlinkhandler)
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(CommandHandler("apple", scheduletest))
    dp.add_handler(CommandHandler("masterlist", masterlist_command))
    dp.add_handler(CommandHandler("register", register_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(0)  # seconds on how often bot check for input
    updater.idle()


'add comment to push'

main()
