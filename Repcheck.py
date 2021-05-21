# Checking if ID is a duplicate in list
IDList = [1, 3, 5, 8, 9]
ID = 45

x: object
def repcheck(ID, IDList):
    for x in IDList:
        if IDList.count(ID) > 0:
            return False
        return True


repcheck(ID, IDList)
if repcheck(ID, IDList):
    print("No duplicates.")
    IDList.append(ID)
    print(IDList)
else:
    print("There are duplicates.")


import json, os
db_name = 'ID'

def check_db(name = db_name):
    if not os.path.isfile(name):
        print('Adding New ID')
        udb = open(db_name,'w')
        udb.close()

def read_db():
    try:
        udb = open(db_name, "r")
    except:
        check_db()
        read_db()
    try:
        dicT = json.load(udb)
        udb.close()
        return dicT
    except:
        return {}

def update_db(newdata):
    data = read_db()
    wdb = dict(data.items() + newdata.items())
    udb = open(db_name, 'w')
    json.dump(wdb, udb)
    udb.close()




