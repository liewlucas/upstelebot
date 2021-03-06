import json
import os


# Use '/root/File_DB/db.txt' when migrated to windows remote desktop
from typing import TextIO

db_name = "db_ID"
ID_List = []
Inputs = []

# Function to check if file database available
def check_db(Fname=db_name):
    # Checking if file exist, then creating if it does not
    if not os.path.isfile(Fname):
        print('File does not exist\nCreating New File')
        udb = open(db_name, 'w')
        print(Fname)
        udb.close()


# Function to read file database
def read_db():
    try:
        udb = open(db_name, "r")
    except:
        check_db()
        read_db()

    # Loading json format list from file database
    try:
        with open(db_name, 'r') as f:
            readList = json.load(f)
            print(readList)

            # Checking if file database empty, creating list to input data
            if len(readList) == 0:
                return []
            else:
                return readList
    except:
        return []


# Updating file database with non-duplicate ID
def update_db(newdata):
    with open(db_name, 'w') as f:
        # indent=2 is not needed but makes the file human-readable
        json.dump(newdata, f, indent=2)


# Defining repetition checking function
x: object
def repcheck(ID, ID_List):
    for x in ID_List:
        if ID_List.count(ID) > 0:
            return True
        return False



#data = {'another_dict': {'a': 0, 'b': 1}, 'a_list': [0, 1, 2, 3]}
#Dictfile = "db"
#with open(Dictfile, 'w') as f:
    #json.dump(data, f)

#with open(Dictfile, 'r') as f:
   #data = json.load(f)
   #print(data)

dict_grp = "db_grpID"
dict_db = "db_info"
RemName = ""
IDchat = ""
day_r = ""
time_r = ""
text_r = ""
usercid_r = ""
name_r = ""
useredit_r = ""
username_r = ""

#Inputs.append({'ID': namex, 'DAY': dayresponse, 'Time': timeresponse, 'Text': textresponse})
#print(Inputs)




# Function to check if file database available
def dict_check(Fname=dict_db):
    # Checking if file exist, then creating if it does not
    if not os.path.isfile(Fname):
        print('File does not exist\nCreating New File')
        udb = open(dict_db, 'w')
        print(Fname)
        udb.close()


# Function to read file database
def dict_read():
    try:
        udb = open(dict_db, "r")
    except:
        dict_check()
        dict_read()

    # Loading json format list from file database
    try:
        with open(dict_db, 'r') as fr:
            global Inputs
            Inputs = json.load(fr)
            print(Inputs)

            # Checking if file database empty, creating list to input data
            if len(Inputs) == 0:
                return []
            else:
                return Inputs
    except:
        return []

def dict_update(newdata):
    with open(dict_db, 'w') as fr:
        Inputs.append({'ReminderName': RemName, 'IDitem': IDchat, 'DAY': day_r, 'Time': time_r, 'Text': text_r, 'User': username_r})
        # indent=2 is not needed but makes the file human-readable
        json.dump(newdata, fr, indent=2)
        print(Inputs)


def dict_Ex():
    dict_read()
    for RemName, IDitem, DAY, Time in sorted([(d['IDitem'], d['DAY'], d['Time']) for d in Inputs], key=lambda t: t[1]):
        print('{}: {}: {}'.format(IDitem, DAY, Time))
        print(IDitem)
        print(DAY)
        print(Time)


def dict_del(datadel):
    with open(dict_db, 'w') as frc:
        for i in range(len(datadel)):
            if datadel[i]['IDitem'] == usercid_r:
                if datadel[i]['ReminderName'] == name_r:
                    del datadel[i]
                    json.dump(datadel, frc, indent=2)
                    print(datadel)
                    break


#Edit Functions
def dict_edit_Time(dataed):
    with open(dict_db, 'w') as fre:
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r:
                if dataed[ed]['ReminderName'] == name_r:
                        #Fill list[dictionary] with user input parameters
                        dataed[ed]['Time'] = time_r  #usereditTime
                        json.dump(dataed, fre, indent=2)
                        print(dataed)
                        break

def dict_edit_Name(dataed):
    with open(dict_db, 'w') as fre:
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r:
                if dataed[ed]['ReminderName'] == name_r:
                        #Fill list[dictionary] with user input parameters
                        dataed[ed]['ReminderName'] = RemName  #usereditReminderName
                        json.dump(dataed, fre, indent=2)
                        print(dataed)

def dict_edit_Day(dataed):
    with open(dict_db, 'w') as fre:
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r:
                if dataed[ed]['ReminderName'] == name_r:
                        #Fill list[dictionary] with user input parameters
                        dataed[ed]['DAY'] = day_r  #usereditDay
                        json.dump(dataed, fre, indent=2)
                        print(dataed)

def dict_edit_Text(dataed):
    with open(dict_db, 'w') as fre:
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r:
                if dataed[ed]['ReminderName'] == name_r:
                        #Fill list[dictionary] with user input parameters
                        dataed[ed]['Text'] = text_r  #usereditText
                        json.dump(dataed, fre, indent=2)
                        print(dataed)



