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

user = 'admin'

pwd = 'notmypassword'

host = '192.168.1.1'

iRestartAfterxMins = 45

Logs into networkstatus.log, and uses networkstatus.txt to store last status

Please note this could reboot your hub everytime it runs, the hub can take 5 minutes to reboot so if you time it badly it could get stuck rebooting.
