import json
import os


dict_db = "db_grpID"
grpchatid = ""
grpchatname = ""
grpusername = ""
Inputs = []
userlist = []
Repcheck = True

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
        userlist.append(grpusername)
        if not newdata:
            newdata.append({'CHATID': grpchatid, 'GRPNAME': grpchatname, 'USER': userlist})
        else:
            for chatid, groupname, username in sorted([(d['CHATID'], d['GRPNAME'], d['USER']) for d in newdata]):
                if(chatid == grpchatid and grpusername in username):
                    print("Already Registered")
                    break

                else:
                    if (chatid == grpchatid and grpusername not in username):
                        username.append(grpusername)
                        Repcheck = True
                        break
                    else:
                        Repcheck = False


            if(Repcheck == False):
                Inputs.append({'CHATID': grpchatid, 'GRPNAME': grpchatname, 'USER': userlist})



        # indent=2 is not needed but makes the file human-readable
        json.dump(newdata, fr, indent=2)
        print(Inputs)
