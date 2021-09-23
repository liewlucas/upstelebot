import json
import os
import zipfile
import hashlib, uuid, base64

RemName = "Error Testing"
IDchat = -558414218
day_r = "Sunday"
time_r = "12:35"
text_r = "I love Coding"
usercid_r = -558414218
name_r = "Error Testing"
useredit_r = "" #ReminderName Edits
username_r = "xnegate"
ID_List = []
Inputs = []
zip_db = "db_info.zip"
zip = (base64.b64decode("Z3JlYXRndWFyZDEyMw==").decode("utf-8"))
salt = str.encode(uuid.uuid4().hex)
Pass = hashlib.sha512(zip.encode('utf-8') + salt).hexdigest()


def dict_lock_check(Fname=zip_db):
    # Checking if Zipfile exist
    if not os.path.isfile(Fname):
        print('File does not exist\n Required to create New Zip File')

    with zipfile.ZipFile(zip_db) as zfile:
        try:
            zfile.open(name=zfile.namelist()[-1], mode='r', pwd=str.encode(zip))
            # ZipFile.getinfo(path = filepath) returns the information about a member of Zip file.
            print(zfile.getinfo(zfile.namelist()[-1]))

        # Checking for Empty Zipfile
        except IndexError:
            print('Zipfile Empty! Please add Text Document into zipfile')
        # Checking for corrupted Zip files
        except zipfile.BadZipFile:
            print("Error: Zip file is corrupted")


def dict_lock_read():
    #dict_lock_check(zip_db)
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            zip_inputs = zfile.read(name=zfile.namelist()[-1], pwd=str.encode(zip))
            global Inputs
            Inputs = json.loads(zip_inputs.decode('utf-8)'))
            print(Inputs)

            # Checking if file database empty, creating list to input data
            if bool(Inputs):
                return Inputs
            else:
                return []

        # Checking for Empty Zipfile
        except IndexError:
            print('Zipfile Empty!')


def dict_lock_update(newdata):
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            newdata.append({"ReminderName": RemName, "IDitem": IDchat, "DAY": day_r, "Time": time_r, "Text": text_r, "User": username_r})
            dict_append = json.dumps(newdata, indent=2).encode('utf-8')
            with zipfile.ZipFile(zip_db, 'w') as zwfile:
                zwfile.writestr(zfile.namelist()[-1], dict_append)
                zwfile.close()
                print(dict_append.decode('utf-8'))


        #Checking for invalid/Non-dictionary DB
        except AttributeError:
            print('Invalid DB! Please add Valid DB to Zipfile to enable Update!')



def dict_del(datadel):
    with zipfile.ZipFile(zip_db) as zfile:
        datasave = datadel
        print(datadel)
        for i in range(len(datadel)):
            if datadel[i]['IDitem'] == usercid_r:
                if datadel[i]['ReminderName'] == name_r:
                    del datadel[i]
                    print("DELETED")
                    bdata = json.dumps(datadel, indent=2).encode('utf-8')
                    try:
                        with zipfile.ZipFile(zip_db, 'w') as zwfile:
                            zwfile.writestr(zfile.namelist()[-1], bdata)
                            zwfile.close()
                            print(datadel)

                    # Checking for invalid/Non-dictionary DB
                    except AttributeError:
                        print("AE!")

                    except IndexError:
                        print("IE!")

                    except NameError:
                        print("NE!")
                    break


#Edit Functions
def lock_edit_Name(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_N
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r and dataed[ed]['ReminderName'] == name_r :
                #Fill list[dictionary] with user input parameters
                updateflag = True
                dataed[ed]['ReminderName'] = useredit_r  #useredit Name
                bedits_N = json.dumps(dataed, indent=2).encode('utf-8')

                try:
                    with zipfile.ZipFile(zip_db, 'w') as zwfile:
                        zwfile.writestr(zefile.namelist()[-1], bedits_N)
                        zwfile.close()
                        print("Data Edited")
                        print(dataed)

                # Checking for invalid/Non-dictionary DB
                except AttributeError:
                    print("AE!")

                except IndexError:
                    print("IE!")

                except NameError:
                    print("NE!")

    if updateflag == False:
        print("No matching Reminder!")

def lock_edit_Time(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_T
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r and dataed[ed]['ReminderName'] == name_r:
                updateflag = True
                #Fill list[dictionary] with user input parameters
                dataed[ed]['Time'] = time_r   #useredit Time
                bedits_T = json.dumps(dataed, indent=2).encode('utf-8')

                try:
                    with zipfile.ZipFile(zip_db, 'w') as zwfile:
                        zwfile.writestr(zefile.namelist()[-1], bedits_T)
                        zwfile.close()
                        print("Data Edited")
                        print(dataed)

                # Checking for invalid/Non-dictionary DB
                except AttributeError:
                    print("AE!")

                except IndexError:
                    print("IE!")

                except NameError:
                    print("NE!")

    if updateflag == False:
        print("No matching Reminder!")

def lock_edit_Day(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_D
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r and dataed[ed]['ReminderName'] == name_r:
                # Fill list[dictionary] with user input parameters
                updateflag = True
                dataed[ed]['DAY'] = day_r  #usereditDay
                bedits_D = json.dumps(dataed, indent=2).encode('utf-8')

                try:
                    with zipfile.ZipFile(zip_db, 'w') as zwfile:
                        zwfile.writestr(zefile.namelist()[-1], bedits_D)
                        zwfile.close()
                        print("Data Edited")
                        print(dataed)


                # Checking for invalid/Non-dictionary DB
                except AttributeError:
                    print("AE!")

                except IndexError:
                    print("IE!")

                except NameError:
                    print("NE!")

    if updateflag == False:
        print("No matching Reminder!")



def lock_edit_Text(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_x
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r and dataed[ed]['ReminderName'] == name_r:
                updateflag = True
                # Fill list[dictionary] with user input parameters
                dataed[ed]['Text'] = text_r  # useredit Time
                bedits_x = json.dumps(dataed, indent=2).encode('utf-8')

                try:
                    with zipfile.ZipFile(zip_db, 'w') as zwfile:
                        zwfile.writestr(zefile.namelist()[-1], bedits_x)
                        zwfile.close()
                        print("Data Edited")
                        print(dataed)


                # Checking for invalid/Non-dictionary DB
                except AttributeError:
                    print("AE!")

                except IndexError:
                    print("IE!")

                except NameError:
                    print("NE!")

    if updateflag == False:
        print("No matching Reminder!")




#dict_lock_check(zip_db)
dict_lock_read()
#dict_lock_update(Inputs)
#dict_del(Inputs)
lock_edit_Day(Inputs)
lock_edit_Time(Inputs)
lock_edit_Text(Inputs)
lock_edit_Name(Inputs)


