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
