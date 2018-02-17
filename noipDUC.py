#!/usr/bin/python

'''
When I installed the NoIP dynamic update client (DUC), (Ubuntu 16 LTS)
I experienced some problems--mainly that the DUC would not run automagically.
So anytime the server IP changed I had to run,
$ ./noip2 -c CONFIG -i <my new ip>
...which is, well not very dynamic is it

so this script hackishly obtains current IP and runs a manual update!
then a cron job executes every 15 minutes:
	$ crontab -e #this might need to be sudo if noip requires su permissions.  don't remember
	then add (*/15 * * * *     /path/to/script.sh) to file

Dependencies:
	- noip2

For a walkthru on using noip tool, refer to https://www.togaware.com/linux/survivor/No_IP_Manual.html 

Derek Snyder
2/7/2018
last revision:
2/17/2018 - replaced hackish dependencies on curl with httplib request, less platform dependent now
'''

import os
import datetime
import httplib

os.chdir('/home/derek/Desktop/scripts') # replace w /path/to/script

# get new global IPv4 address
conn=httplib.HTTPConnection('icanhazip.com')
conn.request('GET', '/')
res=conn.getresponse()

if res.status == 200: # don't want to update if attempt to get IP failed
	myip=res.read().rstrip('\r\n')
	os.chdir('/home/derek/Desktop/noip-2.1.9-1') # replace w /path/to/noip-binary
	cmdStr = './noip2 -c CONFIG -i %s' % (myip)
	os.system(cmdStr)

os.chdir('/home/derek/Desktop/scripts') # replace w /path/to/noip-updater-script
if not os.path.isfile('./noip_log.txt'):
	logFile=file('noip_log.txt', 'w') # opening a non-existent file in append mode doesn't do anything
else:
	logFile=file('noip_log.txt', 'a')

dateStamp = '%d-%d %d:%d %d,' % (
	datetime.date.today().month, 
	datetime.date.today().day, 
	datetime.datetime.now().time().hour, 
	datetime.datetime.now().time().minute, 
	datetime.date.today().year
	)

logFile.write(dateStamp + str(res.status) + ',\n')
logFile.close()