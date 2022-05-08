import json
import os
import zipfile
import hashlib, uuid, base64

pltname = "" #Name of Platoon
passw = "" #respective platoon pw


# For Deletes
pltname_r = ""
passw_r = ""


Inputs = []
zip_db = "pw_link.zip"
zip = (base64.b64decode("Z3JlYXRndWFyZDEyMw==").decode("utf-8"))
salt = str.encode(uuid.uuid4().hex)
Pass = hashlib.sha512(zip.encode('utf-8') + salt).hexdigest()


def pw_check(Fname=zip_db):
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


def pw_read():
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


def pw_update(newdata):
    with zipfile.ZipFile(zip_db) as zfile:
        try:
            newdata.append({"PltName": pltname, "Password": passw})
            dict_append = json.dumps(newdata, indent=2).encode('utf-8')
            with zipfile.ZipFile(zip_db, 'w') as zwfile:
                zwfile.writestr(zfile.namelist()[-1], dict_append)
                zwfile.close()
                print(dict_append.decode('utf-8'))


        #Checking for invalid/Non-dictionary DB
        except AttributeError:
            print('Invalid DB! Please add Valid DB Text File to Zipfile to enable Update!')



def pw_del(datadel):
    with zipfile.ZipFile(zip_db) as zfile:
        for i in range(len(datadel)):
            if datadel[i]['PltName'] == pltname_r:
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



#pw_check()
#pw_read()
#pw_update(Inputs)
#pw_del(Inputs)

