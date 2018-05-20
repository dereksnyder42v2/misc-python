#!/usr/bin/python

"""
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
 2/ 7/2018
 2/17/2018 - replaced hackish dependencies on curl with httplib request, less platform dependent now
 4/13/2018 - refactor
 4/14/2018 - refactor and modify for use on Ubuntu
"""

import datetime
import httplib
import os, subprocess

_NOIP_BIN_PATH_ROOT = "/home/derek/noip-2.1.9-1/" # TODO
_LOGFILE_PATH = "/home/derek/noip-pyduc/noip-update-log.txt" # TODO

def date_stamp():
    ds = "%s-%s-%s %s:%s" % (
	str(datetime.date.today().year).zfill(4),
        str(datetime.date.today().month).zfill(2), 
	str(datetime.date.today().day).zfill(2), 
	str(datetime.datetime.now().time().hour).zfill(2), 
	str(datetime.datetime.now().time().minute).zfill(2), 
    )
    return ds

if __name__ == "__main__":

    # get new global IPv4 address
    conn = httplib.HTTPConnection("icanhazip.com")
    conn.request("GET", "/")
    res = conn.getresponse()

    if res.status == 200: # don't want to update if attempt to get IP failed
        myip = res.read().rstrip('\r\n')
        os.chdir( _NOIP_BIN_PATH_ROOT) # replace w /path/to/noip-binary
        cmd_str = "./noip2 -c CONFIG -i %s" % (myip)
        try:
            subprocess.check_output(cmd_str.split() ) # TODO verify output
        except:
            pass 

    if not os.path.isfile( _LOGFILE_PATH):
        logfile = file( _LOGFILE_PATH, "w") # opening a non-existent file in append mode doesn't do anything
    else:
        logfile = file( _LOGFILE_PATH, "a")

    logfile.write(date_stamp() + "," + str(res.status) + ",\n")
    logfile.close()

