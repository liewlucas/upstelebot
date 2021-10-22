import json
import os

#variables filled in from main
xx = ""
yy = ""
zz = ""

admin_user = ""
admin_ID = ""
grpchatname = ""
whitelistpass = ""
changed_adminpw = ""
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
    wl_read()
    for i in range(len(wInputs)):
        if wInputs[i]['USER'] == xx:
            if wInputs[i]['CHATID'] == yy:
                with open(wl_db, 'w') as fr:
                    wInputs.append({'CHATID': admin_ID, 'GRPNAME': grpchatname, 'USER': admin_user, 'PASSWORD': whitelistpass})
                    # indent=2 is not needed but makes the file human-readable
                    json.dump(wInputs, fr, indent=2)
                    print(wInputs)


def wl_revoke(datadel):
    for i in range(len(datadel)):
        if datadel[i]['GRPNAME'] == xx and datadel[i]['USER'] == yy and datadel[i]['PASSWORD'] == zz:
            with open(wl_db, 'w') as frc:
                del datadel[i]
                json.dump(datadel, frc, indent=2)
                print(datadel)


def wl_edit(editpw):
    for i in range(len(editpw)):
        if editpw[i]['GRPNAME'] == xx and editpw[i]['USER'] == yy and editpw[i]['PASSWORD'] == zz:
            with open(wl_db, 'w') as fe:
                editpw[i]['PASSWORD'] = changed_adminpw
                json.dump(editpw, fe, indent=2)
                print(editpw)