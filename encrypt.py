import json
import zipfile
import random
import hashlib, uuid, base64


# db_name = "C:/Users/Antho/Desktop/TEst TExt2"
zip_name = "C:/Users/Antho/Desktop/TEst TExt2.zip"

#Base64 Encoding
Pword = (base64.b64decode("Z3JlYXRndWFyZDEyMw==").decode("utf-8"))
print(base64.b64decode("Z3JlYXRndWFyZDEyMw==").decode("utf-8"))
RemName = "Name"
IDchat = "ID"
day_r = "Date"
time_r = "Hoe"
text_r = "IT Tech Support"

usercid_r = -45992903294
name_r = 'Nami'

#Hashing not viable
#Pword = str.encode('greatguard123')
#salt = str.encode(uuid.uuid4().hex)
#hashed_Pword = hashlib.sha512(Pword + salt).hexdigest()
#print(hashed_Pword)


#def rng_pword():
    #chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    #length = 16
    #global Pout
    #Pout = ''
    #for c in range(length):
        #Pout += random.choice(chars)
    #print(Pout)

def read_zipdb():
    with zipfile.ZipFile(zip_name) as zfile:
        try:
            zfile.open(name=zfile.namelist()[-1], mode='r', pwd=str.encode(Pword))
            # ZipFile.getinfo(path = filepath) returns the information about a member of Zip file.
            print(zfile.getinfo(zfile.namelist()[-1]))

        # Checking for Empty Zipfile
        except IndexError:
            print('Zipfile Empty! Please add Text Document into zipfile')

        # Checking for corrupted Zip files
        except zipfile.BadZipFile:
            print("Error: Zip file is corrupted")


def open_read_text():
    with zipfile.ZipFile(zip_name) as zfile:
        zipreadList = zfile.read(name="TEst TExt2.txt", pwd=str.encode(Pword))
        global readlist
        readlist = json.loads(zipreadList.decode('utf-8'))

        # Checking if file database empty, creating list to input data
        if bool(readlist):
            return readlist
        else:
            return []



def dict_lock_update(newdata):
    try:
        newdata.append({'ReminderName': RemName, 'IDitem': IDchat, 'DAY': day_r, 'Time': time_r, 'Text': text_r})
        dict_append = json.dumps(newdata, indent=2).encode('utf-8')
        with zipfile.ZipFile(zip_name, 'w') as zwfile:
            zwfile.writestr("TEst TExt2.txt", dict_append)
            zwfile.close()
            print(dict_append.decode('utf-8'))

    #Checking for invalid/Non-dictionary DB
    except AttributeError:
        print('Invalid DB! Please add Valid DB to Zipfile')


def dict_del(datadel):
    for i in range(len(datadel)):
        if datadel[i]['IDitem'] == usercid_r:
            if datadel[i]['ReminderName'] == name_r:
                del datadel[i]
                bdata = json.dumps(datadel, indent=2).encode('utf-8')
                print(bdata)
                break

    with zipfile.ZipFile(zip_name, 'w') as zwfile:
        zwfile.writestr("TEst TExt2.txt", bdata)
        zwfile.close()
        print(datadel)


#Edit Functions
def lock_edit_Time(dataed):
    with zipfile.ZipFile(zip_name) as zefile:
        for ed in range(len(dataed)):
            if dataed[ed]['IDitem'] == usercid_r:
                if dataed[ed]['ReminderName'] == name_r:
                        #Fill list[dictionary] with user input parameters
                        dataed[ed]['Time'] = time_r  #usereditTime
                        global bedits
                        bedits = json.dumps(dataed, indent=2).encode('utf-8')
                        break

        with zipfile.ZipFile(zip_name, 'w') as zwfile:
            zwfile.writestr(zefile.namelist()[-1], bedits)
            zwfile.close()
            print(dataed)

read_zipdb()
open_read_text()
#dict_lock_update(readlist)
#dict_del(readlist)
lock_edit_Time(readlist)






