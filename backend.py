import os, smtplib
IPLIST = r'ipsheet.txt'
EMAIL_ADDRESS = 'cryptoSyr428@gmail.com'
EMAIL_PASSWORD = 'Applesauce34'


database = open(IPLIST,"r")

#P = database.readline()     #P is the host's IP
PASSWORD_LEN = 32
guestPasswords = []       #will remember guests passwords, ordered as a tuple of (pos, email, pass)   or (int, str, str)
currGuest = 0


def sendEmail(email):
    #sends email to their email (entered in parameter)
    global currGuest
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = "Zoom-Copy password"

        cc = os.urandom(PASSWORD_LEN)
        guestPasswords.append((currGuest, email,cc))
        currGuest+=1

        body = cc
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, email, msg)
    return cc

def createRoom():
    #creates a room w/ random pass for host
    return os.urandom(PASSWORD_LEN)


def validateUserIP(ip):
    #checks if user is valid to enter (ie if IP is valid to come in from)
    if ip in open(IPLIST).read():
        return True
    return False

"""
idk it doesnt work like i wanted
def inBlockList(ip):
    blockSheet = open("blockedUsers.txt","r")
    cc = (ip in blockSheet)
    blockSheet.close()
    return not cc
"""

def putPassNextIP(password, ip):
    global database
    database.close()
    if not validateUserIP(ip):
        return False

    with open(IPLIST,'r') as f:
        lines = f.readlines()

    with open(IPLIST, "w") as fh:
        for line in lines:
            if line.startswith(ip):
                fh.write(ip + "\t" + password + '\n')
            else:
                fh.write(line)
    database = open(IPLIST,"r")
    

def addToRoom(key):
    pass

def blockUser(ip):
    #backtracks from key to IP in database
    blockSheet = open("blockedUsers.txt","w")
    blockSheet.write(ip)
    val = removeIP(ip)
    blockSheet.close()
    return val

def addIP(ip):
    #adds IP to DB
    global database
    database.close()
    if validateUserIP(ip):
        #if it already exists in the db
        return False

    with open(IPLIST,"r+") as fh:
        for line in fh:
            if line.startswith(ip):     #if ip is found in list
                return False
        fh.write(ip + "\n")
    database = open(IPLIST, "r")
    return True


def removeIP(ip):
    global database
    database.close()
    val = False
    with open(IPLIST, "r") as f:
        lines = f.readlines()
    with open(IPLIST, "w") as f:
        for line in lines:
            if line.strip("\n") != ip:
                f.write(line)
            else:
                val = True
    database = open(IPLIST,"r")
    return val


def sendUserPass(email, ip): 
    #emails guests their respective password
    if(validateUserIP(ip)):
        guest_pass = sendEmail(email)
        putPassNextIP(guest_pass, ip)
        return True
    else:
        blockUser(ip)
        return False

#print(inBlockList('162.111.93.999'))
#print(validateUserIP('162.111.93.999'))
#addIP('162.111.93.999')

#print(validateUserIP('166.221.158.209'))
#print(putPassNextIP('gg','224.82.25.210'))
#print(putPassNextIP('gg','166.221.158.209'))
#print(sendUserPass('gg','162.111.93.999'))


database.close()
