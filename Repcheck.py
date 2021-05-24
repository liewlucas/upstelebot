import json
import os

db_name = 'C:/Users/Antho/Desktop/DBfile/db.txt'
IDList = []
ID = 47


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

def repcheck(ID, IDList):
    for x in IDList:
        if IDList.count(ID) > 0:
            return True
        return False


# Using Repetition checking function
# To prepopulate the IDlist from a file
IDList = read_db()
print("afterlist")
print(IDList)
if repcheck(ID, IDList):
    print("There are duplicates.")
else:
    print("No duplicates.")
    # Later to add multi-schedule function

    # Adding new ID to IDList
    IDList.append(ID)
    print("after append")
    update_db(IDList)
    print(IDList)
    # Add Original Schedule Function



# Adapted for Main*
# Use '/root/File_DB/db.txt' when migrated to windows remote desktop
db_name = 'C:/Users/Antho/Desktop/DBfile/db.txt'
ID_List = []


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

def repcheck(userchatid2, ID_List):
    for x in ID_List:
        if ID_List.count(userchatid2) > 0:
            return True
        return False

    # Using Repetition checking function
    # To prepopulate the IDlist from a file
    ID_List = read_db()
    print("afterlist")
    print(ID_List)
    if repcheck(userchatid2, ID_List):
        print("There are duplicates.")
    else:
        print("No duplicates.")
        # Later to add multi-schedule function

        # Adding new ID to IDList
        ID_List.append(userchatid2)
        print("after append")
        update_db(ID_List)
        print(ID_List)
        # Add Original Schedule Function