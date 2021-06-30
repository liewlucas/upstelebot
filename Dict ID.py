import os
import json

# n = []
# list = [{'n': 'apple'}, {'n': 'banana'}, {'n': 'cow'}, {'n': 'donkey'},]
# def listy():

    # listo = [{n: 'apple'}, {n: 'banana'}, {n: 'cow'}, {n: 'donkey'}, {n: 'elephant'}]

    # for key in listo:
        # Number = n
        # n = n + 1
        # list.append({'Number': Number})
        # [(i,) + item for i, item in enumerate(dict.items(n), 1)]

# ID for items in dictionary
# [(i,) + item for i, item in enumerate(dict.items(), 1)]


#for key in list:
    #Rep.dict_read()
    # Rep.dict_update(Rep.Inputs)
    # Rep.reno = Rep.reno + 1


RemID = "RemIDcounter"
Listo = ["a", "b", "c", "d", "e"]
Listi = [{"apples": "oranges"}]
obj = object
stats = "db_ID"
xx = -558414218
yy = 'Test'

#-473469885
#dsfghjkl



# Function to check if Reminder ID file available
def check_db(Fname=RemID):
    # Checking if file exist, then creating if it does not
    if not os.path.isfile(Fname):
        print('File does not exist\nCreating New File')
        udb = open(RemID, 'w')
        print(Fname)
        udb.close()

def get_var_value(filename="RemIDcounter"):
    with open(filename, "a+") as f:
        f.seek(0)
        val = int(f.read() or 0) + 1
        f.seek(0)
        f.truncate()
        f.write(str(val))
        return val

def RemIDcheck(dictionary):
    for obj in dictionary:
        nu = str(get_var_value())
        Listi.append({"Reminder_ID": nu})
        print(Listi)
        print("This script has been run {} times.".format(nu))
        print("Reminder ID No. is {}.".format(nu))


def test_read():
    # Loading json format list from file database
    try:
        with open(stats, 'r') as frc:
            global Inputs_test
            Inputs_test = json.load(frc)
            print(Inputs_test)
    except:
        return []

def dict_del(datadel):
        for i in range(len(datadel)):
            if datadel[i]['IDitem'] == xx:
                if datadel[i]['ReminderName'] == yy:
                    with open(stats, 'w') as frc:
                        del datadel[i]
                        json.dump(datadel, frc, indent=2)
                        print(datadel)



test_read()
dict_del(Inputs_test)


# RemIDcheck(Listo)
# your_counter = get_var_value()
# print("This script has been run {} times.".format(your_counter))

# with is like your try .. finally block in this case
