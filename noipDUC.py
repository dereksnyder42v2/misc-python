#!/usr/bin/python

'''
When I installed the NoIP dynamic update client (DUC), (Ubuntu 16 LTS)
I experienced some problems--mainly that the DUC would not run automagically.
So anytime the server IP changed I had to run,
$ ./noip2 -c CONFIG -i <my new ip>
...which is, well not very dynamic is it

so this script hackishly obtains current IP and runs a manual update!
then a cron job executes every 5 minutes:
	$ crontab -e #this might need to be sudo if noip requires su permissions.  don't remember
	then add (*/X * * * *     /path/to/script.sh) to file
more notes about cron jobs: if you want this script to keep a log of updates, 
	you should '$ chown <user> FADlog.txt' so it doesn't belong to root
(oh, and it's called FADlog.txt because the original script was named fuc-a-duc.py... LOL)

Dependencies:
	- curl
	- noip2

For a walkthru on using noip tool, refer to https://www.togaware.com/linux/survivor/No_IP_Manual.html 

Derek Snyder
2/7/2018
'''

import os
import datetime

os.chdir('/home/derek/Desktop/scripts') # replace w /path/to/script

dateStamp = '%d-%d %d:%d %d\n' % (datetime.date.today().month, datetime.date.today().day, datetime.datetime.now().time().hour, datetime.datetime.now().time().minute, datetime.date.today().year)
log_file=open('FADlog.txt','w') 
log_file.write(dateStamp)
log_file.close()

os.system('rm myIp.txt') # delete existing record: only want recent
#it's hard to communicate b/w python and a shell. I use text files...
cmdStr = 'curl http://icanhazip.com/ 2>/dev/null > myIp.txt' 
os.system(cmdStr)

ip_file = open('myIp.txt', 'r')
for line in ip_file:
	myip = line
	myip = myip.rstrip('\r\n')
	break #it's the first line. avoid that newline business

ip_file.close()
#print myip

os.chdir('/home/derek/Desktop/noip-2.1.9-1') # replace w /path/to/noip-binary
cmdStr = './noip2 -c CONFIG -i %s' % (myip)
os.system(cmdStr)
