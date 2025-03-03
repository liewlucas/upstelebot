import time
from datetime import datetime
from telegram import bot


now = datetime.now()
current_time= now.strftime("%H:%M:%S")
def time_response(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi ups bot", "hi bot"):
        return "Hey, this is the UpdateParadeState Bot"

    try:
        time.strptime(user_message, '%H:%M')
        global userinputtime
        userinputtime = user_message
        replymessage = "Reminder has been set on: "
        arrayofreply = [replymessage,userday, "at" ,userinputtime]
        fullreply = " " #empty string
        reply = (fullreply.join(arrayofreply))
        return reply

    except :
        return "Sorry, Your Date Time format is wrong. Please Follow Example: 17:30 "


    print(userinput)
    your_str = userinput.text

    return "Sorry i dont understand"

def day_response(input_day):
    user_day = str(input_day)

    try:
        #time.strptime(user_day, '%A')
        global userday
        userday = user_day
        replymessage = "Reminder is set on"
        arrayofreply= [replymessage, userday, userinputtime]
        fullreply = " "
        reply = (fullreply.join(arrayofreply))
        return reply

    except :
        return "Sorry, Your Day format is wrong. Please Follow Example: Monday "


    '------------------ INDENT RATION BOT ------------------------------------'

    def username_response(input_text):
        global usernameinput
        usernameinput = str(input_text)

        try:
            replymessage = "Your username is"
            arrayofreply = [replymessage, usernameinput]
            fullreply = ' '
            reply = (fullreply.join(arrayofreply))
            return reply
        except:
            return "Sorry your input was invalid"

    def password_response(input_text):
        global passwordinput
        passwordinput = str(input_text)

        try:
            replymessage = "Your password is"
            arrayofreply = [replymessage, passwordinput]
            fullreply = ' '
            reply = (fullreply.join(arrayofreply))
            return reply
        except:
            return "Sorry your input was invalid"

    def pin_response(input_text):
        global pininput
        pininput = str(input_text)
        if len(pininput) == 4:
            try:
                pin_input = int(input_text)
                replymessage = "Your pin is"
                arrayofreply = [replymessage, str(pininput),
                                'use /indent to indent your rations. For more information on how to use this bot, use /help']
                fullreply = ' '
                reply = (fullreply.join(arrayofreply))
                return reply
            except:
                return 'Sorry your input was invalid, please input another pin'
        else:
            return 'Sorry your input was invalid, please input another pin'

    def ration_response(input_text):
        global rationinput
        rationinput = str(input_text)

        try:
            replymessage = "Your option is"
            arrayofreply = [replymessage, rationinput]
            fullreply = ' '
            reply = (fullreply.join(arrayofreply))
            return reply

        except:
            return "Sorry your input was invalid"
