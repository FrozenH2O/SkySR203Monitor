# SkySR203Monitor
Python script to monitor the internet connection and reboot the Hub if it is has been down for so long

For some unknown reason every few weeks my Sky Hub loses internet connection, 
unplugging the network cable between the ONT and the hub, then reconnecting is the fastest way to get up and running.
The cable disconect / reconnect makes sky dhcpc client (v0.0.1) start again.
But if I'm not in the house then the internet will stay down, so this script will check the connection and call the Hub reboot function.

Decides if the internet is down because it can't access http://www.google.com, so if Google ever shuts up shop you'll need to change to another reliable domain

I run this on a Raspberry Pi, called from the crontab every 6 minutes
cronttab example:
*/6 * * * * python /home/myuser/networkmonitor/networkmonitor.py

In networkmonitor.py change these:
# username of the skyhub
user = 'admin'
# password of the skyhub - change this
pwd = 'notmypassword'
# ip address of the skyhub - change this
host = '192.168.1.1'

#  shorten it to 10 minutes if you want 3/4 hour suits me because Blink will tell me after 30 minutes and I can unplug the cable and plug back in if I'm home
iRestartAfterxMins = 45

Please note this could reboot your hub everytime it runs, the hub can take 5 minutes to reboot so if you time it badly it could get stuck rebooting.
