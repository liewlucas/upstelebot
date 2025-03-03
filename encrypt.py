import json
import os

#variables filled in from main
adname = ""
adgrp = ""
adchatid = ""
adpass = ""

#true/false return value
Trigger = True     #Checking for Masterexecutive

#Other Variables
changed_adminpw = "ChangedPassword"
wl_db = "db_new_whitelist"
wInputs = []

def wl_check(Fname=wl_db):
    # Checking if file exist, then creating if it does not
    if not os.path.isfile(Fname):
        print('File does not exist\nCreating New File')
        udb = open(wl_db, 'w')
        print(Fname)
        udb.close()


# Function to read file database
def wl_read():
    try:
        udb = open(wl_db, "r")
    except:
        wl_check()
        wl_read()

    # Loading json format list from file database
    try:
        with open(wl_db, 'r') as fr:
            global wInputs
            wInputs = json.load(fr)
            print(wInputs)

            # Checking if file database empty, creating list to input data
            if len(wInputs) == 0:
                return []
            else:
                return wInputs
    except:
        return []


def wl_register():
    if Trigger is True:
        with open(wl_db, 'w') as fr:
            for i in range(len(wInputs)):
                wInputs.append({'CHATID': adchatid, 'GRPNAME': adgrp, 'USER': adname, 'PASSWORD': adpass})
                # indent=2 is not needed but makes the file human-readable
                json.dump(wInputs, fr, indent=2)
                print(wInputs)


def wl_revoke(datadel):    #For individual Users with individual passwords (Undecided)
    if Trigger is True:
        for i in range(len(datadel)):
            if datadel[i]['GRPNAME'] == adgrp and datadel[i]['USER'] == adname and datadel[i]['PASSWORD'] == adpass:
                with open(wl_db, 'w') as frc:
                    del datadel[i]
                    json.dump(datadel, frc, indent=2)
                    print(datadel)


def wl_reset(datar):     #For Grouped Users with Specific Passwords for Each Group (Undecided)
    if Trigger is True:
        for i in range(len(datar)):
            if datar[i]['GRPNAME'] == adgrp:
                with open(wl_db, 'w') as frc:
                    datar[i]['USER'] = []       #Reset all Admin Users assigned to the selected group
                    json.dump(datar, frc, indent=2)
                    print(datar)


def wl_resetpw(rpw):     #For Grouped Users with Specific Passwords for Each Group
    if Trigger is True:
        for i in range(len(rpw)):
            if rpw[i]['GRPNAME'] == adgrp and rpw[i]['PASSWORD'] == adpass:
                with open(wl_db, 'w') as fe:
                    rpw[i]['PASSWORD'] = changed_adminpw       #Reset Password for Group (For Grouped Users)
                    json.dump(rpw, fe, indent=2)
                    print(rpw)


def wl_edit(editpw):
    if Trigger is True:
        for i in range(len(editpw)):
            if editpw[i]['GRPNAME'] == adgrp and editpw[i]['USER'] == adname and editpw[i]['PASSWORD'] == adpass:
                with open(wl_db, 'w') as fe:
                    editpw[i]['PASSWORD'] = changed_adminpw
                    json.dump(editpw, fe, indent=2)
                    print(editpw)

wl_read()
#wl_revoke(wInputs)
wl_edit(wInputs)
#wl_reset(wInputs)
#wl_resetpw(wInputs)
