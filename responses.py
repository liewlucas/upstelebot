import time
from datetime import datetime

from telegram import bot

now = datetime.now()
current_time= now.strftime("%H:%M:%S")
def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hi ups bot", "hi bot"):
        return "Hey, this is the UpdateParadeState Bot"

    try:
        time.strptime(user_message, '%H:%M')
        userinput = user_message
        replymessage = "Reminder is set at"
        arrayofreply = [replymessage, userinput]
        fullreply = " " #empty string
        return(fullreply.join(arrayofreply))

    except ValueError:
        return "Sorry Your Date Time format is wrong. Please Follow Example: 17:30 "


    print(userinput)
    your_str = userinput.text

    return "Sorry i dont understand"