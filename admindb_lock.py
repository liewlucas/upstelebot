import json
import os
import zipfile
import hashlib, uuid, base64

admname = "" #Username of Administrator
passd = "" #Administrator verification
admtype = "" #Clasification of Administrator


# For Edits/Deletes
admname_r = ""
passd_r = ""
admtype_r = ""



Inputs = []
zip_db = "admin.zip"
zip = (base64.b64decode('QWxwaGExMjM=').decode("utf-8"))
salt = str.encode(uuid.uuid4().hex)
Pass = hashlib.sha512(zip.encode('utf-8') + salt).hexdigest()



def adm_check(Fname=zip_db):
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


def adm_read():
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


def adm_update(newdata):
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            newdata.append({"AdminName": admname, "Password": passd, "AdminType": admtype})
            dict_append = json.dumps(newdata, indent=2).encode('utf-8')
            with zipfile.ZipFile(zip_db, 'w') as zwfile:
                zwfile.writestr(zfile.namelist()[-1], dict_append)
                zwfile.close()
                print(dict_append.decode('utf-8'))


        #Checking for invalid/Non-dictionary DB
        except AttributeError:
            print('Invalid DB! Please add Valid DB Text File to Zipfile to enable Update!')



def adm_del(datadel):
    with zipfile.ZipFile(zip_db) as zfile:
        for i in range(len(datadel)):
            if datadel[i]['AdminName'] == admname_r:
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


def adm_edit(dataed):
    with zipfile.ZipFile(zip_db) as zefile:
        global bedits_D
        global updateflag
        updateflag = False
        for ed in range(len(dataed)):
            if dataed[ed]['AdminName'] == admname_r:
                # Fill list[dictionary] with user input parameters
                updateflag = True
                dataed[ed]['Password'] = passd_r  #Change of admin pw
                dataed[ed]['AdminType'] = admtype_r #hardcoded to be administrator by default
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



#adm_check()
#adm_read()
#adm_update(Inputs)
#adm_del(Inputs)
#adm_edit(Inputs)


