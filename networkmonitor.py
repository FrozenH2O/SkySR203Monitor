# run on crontab - e.g every 5 minutes
# be aware that the hub can take 4 minutes to get going again, so if you time it badly you might get stuck 

from datetime import datetime
import time
import re
import requests
from requests.auth import HTTPDigestAuth

# username of the skyhub
user = 'admin'
# password of the skyhub - change this
pwd = 'notmypassword'
# ip address of the skyhub - change this
host = '192.168.1.1'

#  shorten it to 10 minutes if you want 3/4 hour suits me because Blink will tell me after 30 minutes and I can unplug the cable and plug back in if I'm home
iRestartAfterxMins = 45

bLogOn = True
fmt = "%Y-%m-%d %H:%M:%S"

def checknetwork():
    iconnected = 3

    try:
        # change from google to gobbledeegoop to test what happens when the internet is down
        requests.get('http://www.google.com', timeout=5)
        iconnected = 1
        print("Connected to the Internet")
    except requests.exceptions.RequestException as err:
        iconnected = 0
        print("No internet connection.")
    
    return iconnected

def restartrouter():

    url = 'http://' + host + '/sky_rebootCPE.html'
    urlreboot = 'http://' + host + '/sky_rebootCPE.cgi?todo=reboot&sessionKey='

    try:
        response = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=10)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        logthis("Hub unaccessible - Http error.")
        return
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        logthis("Hub unaccessible - Connection.")
        return
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        logthis("Hub unaccessible - Timeout.")
        return
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        logthis("Hub unaccessible - Request error.")
        return

    if response.status_code != requests.codes.ok:
      logthis(url + " " + str(response.reason))
      return

    htmlbody = str(response.text)

    # we want the sessionKey, its in a line that looks like - $.ajax({url:"sky_rebootCPE.cgi?todo=reboot&sessionKey=1117778432",
    for line in htmlbody.splitlines():
        if 'sessionKey=' in line:
            sessionKey = line.split("sessionKey=")[1]
            sessionKey = re.sub('[^A-Za-z0-9]+', '', sessionKey)

    # complete the reboot url with the current sessionkey
    urlreboot = urlreboot + sessionKey
    print (urlreboot)
    logthis("Calling reboot...")
    response = requests.get(urlreboot, auth=HTTPDigestAuth(user, pwd))

    # we've tried, lets stop now and see what happens
    print ("fingers crossed")

def networkisdown():
    

    # get last status
    f = open("./networkstatus.txt", "r")
    laststatus = f.readline().strip("\n")
    f.close()
    
    # check the laststatus if not a date say it was up, because it is blank perhaps
    try:
        d1 = datetime.strptime(laststatus, fmt)
    except ValueError:
        laststatus = "UP"
    
    print(laststatus)
    downsince = 0
    if laststatus != "UP":
        # Its been down at least once before
        d1 = datetime.strptime(laststatus, fmt)
        d2 = datetime.now()

        # how many minutes has it been down for
        downsince = (d2 - d1).total_seconds() / 60.0
        print (downsince)

        if downsince < iRestartAfterxMins:
            # log that the network is down
            logthis("Network is down - Waiting for " + str(int(iRestartAfterxMins - downsince)) + " Minutes")

    if laststatus == "UP":
        print ("network was UP - record the time")
        # if network down for the 1st time, record the time
        f = open("./networkstatus.txt", "w")
        f.write(datetime.now().strftime(fmt))
        f.close()
        logthis("Network is down - Waiting for " + str(iRestartAfterxMins) + " Minutes")

    elif downsince > iRestartAfterxMins:
        # if network down for > 45 minutes 
        print ("network has been down for " + str(iRestartAfterxMins) + " minutes - restart router")
        restartrouter()


def logthis(stringtolog):
    if bLogOn == True:
        fl = open("./networkstatus.log","a")
        fl.writelines(datetime.now().strftime(fmt) + " : " + stringtolog + "\n")
        fl.close()


# 1. check network
networkstatus = checknetwork()
if networkstatus == 0:
    # 2. Network is down
    print ("network is DOWN")
    networkisdown()
elif networkstatus == 1:
    print ("network is UP")
    # get last status
    f = open("./networkstatus.txt", "r")
    laststatus = f.readline().strip("\n")
    f.close()
    if laststatus != "UP" and laststatus != "":
        # log that the network is back up
       logthis("Network is back up")

    f = open("./networkstatus.txt", "w")
    f.write("UP")
    f.close()

      

