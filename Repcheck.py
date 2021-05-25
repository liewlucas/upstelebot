import json
import os

# Use '/root/File_DB/db.txt' when migrated to windows remote desktop
db_name = "db"
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
def repcheck(ID, ID_List):
    for x in ID_List:
        if ID_List.count(ID) > 0:
            return True
        return False

