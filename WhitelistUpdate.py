import json
import os


wl_db = "db_whitelist"
Masterexecutive = ("liewlucass", "xnegate")
grpchatid = ""
grpchatname = ""
grpusername = ""
Inputs = []


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

def whitelist_reg(newdata):
    with open(wl_db, 'w') as fr:
        Inputs.append({'CHATID': grpchatid , 'GRPNAME': grpchatname, 'USER': grpusername })
        # indent=2 is not needed but makes the file human-readable
        json.dump(newdata, fr, indent=2)
        print(Inputs)
