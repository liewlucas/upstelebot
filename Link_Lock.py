import json
import os
import zipfile
import hashlib, uuid, base64

linkname = "" #Purpose of Link (Name)
pltname = "" #Name of Platoon
pltid = "" #Platoon ID
linktext = "" #Link

# For Edits
linkname_r = ""
usereditlinkname = ""
pltname_r = ""
pltid_r = ""
linktext_r = ""

Inputs = []
zip_db = "link_info.zip"
zip = (base64.b64decode("Z3JlYXRndWFyZDEyMw==").decode("utf-8"))
salt = str.encode(uuid.uuid4().hex)
Pass = hashlib.sha512(zip.encode('utf-8') + salt).hexdigest()


def link_check(Fname=zip_db):
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


def link_read():
    #dict_lock_check(zip_db)
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            zip_inputs = zfile.read(name=zfile.namelist()[-1], pwd=str.encode(zip))
            global Inputs
            Inputs = json.loads(zip_inputs.decode('utf-8)'))
            #print(Inputs)

            # Checking if file database empty, creating list to input data
            if bool(Inputs):
                return Inputs
            else:
                return []

        # Checking for Empty Zipfile
        except IndexError:
            print('Zipfile Empty!')


def link_update(newdata):
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            newdata.append({"LinkName": linkname, "PltName": pltname, "PltID": pltid, "LinkText": linktext})
            dict_append = json.dumps(newdata, indent=2).encode('utf-8')
            with zipfile.ZipFile(zip_db, 'w') as zwfile:
                zwfile.writestr(zfile.namelist()[-1], dict_append)
                zwfile.close()
                print(dict_append.decode('utf-8'))


        #Checking for invalid/Non-dictionary DB
        except AttributeError:
            print('Invalid DB! Please add Valid DB Text File to Zipfile to enable Update!')



def link_del(datadel):
    with zipfile.ZipFile(zip_db) as zfile:
        for i in range(len(datadel)):
            if datadel[i]['LinkName'] == linkname_r:
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
def link_edit_Name(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_N
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['LinkName'] == linkname_r:
                #Fill list[dictionary] with user input parameters
                updateflag = True
                dataed[ed]['LinkName'] = usereditlinkname  #useredit Name
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

def link_edit_Link(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_T
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['LinkName'] == linkname_r:
                updateflag = True
                #Fill list[dictionary] with user input parameters
                dataed[ed]['LinkText'] = linktext_r  #useredit Time
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

def link_edit_Plt(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_D
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['LinkName'] == linkname_r:
                # Fill list[dictionary] with user input parameters
                updateflag = True
                dataed[ed]['PltName'] = pltname_r  # user edit for platoon name
                dataed[ed]['PltID'] = pltid_r  # platoon name coorelates to relevant group chat id
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



#def lock_edit_Text(dataed):
    #with zipfile.ZipFile(zip_db) as zefile:
        #global bedits_x
        #global updateflag
        #updateflag = False
        #for ed in range(len(dataed)):
            #if dataed[ed]['ReminderName'] == name_r:
                #updateflag = True
                # Fill list[dictionary] with user input parameters
                #dataed[ed]['Text'] = text_r  # useredit Time
                #bedits_x = json.dumps(dataed, indent=2).encode('utf-8')

                #try:
                    #with zipfile.ZipFile(zip_db, 'w') as zwfile:
                        #zwfile.writestr(zefile.namelist()[-1], bedits_x)
                        #zwfile.close()
                        #print("Data Edited")
                        #print(dataed)


                # Checking for invalid/Non-dictionary DB
                #except AttributeError:
                    #print("AE!")

                #except IndexError:
                    #print("IE!")

                #except NameError:
                    #print("NE!")

    #if updateflag == False:
        #print("No matching Reminder!")



link_check(zip_db)
#link_read()
#link_update(Inputs)
#link_del(Inputs)

#link_edit_Link(Inputs)
#link_edit_Plt(Inputs)
#link_edit_Name(Inputs)