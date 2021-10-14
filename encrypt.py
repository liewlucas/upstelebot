admin_pass = ""
whitelistpass = ""

def dict_check(Fname=wl_db):
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

def wl_register(datadel):
    for i in range(len(datadel)):
        if datadel[i]['IDitem'] == xx:
            if datadel[i]['ReminderName'] == yy:
                with open(stats, 'w') as frc:
                    del datadel[i]
                    json.dump(datadel, frc, indent=2)
                    print(datadel)





