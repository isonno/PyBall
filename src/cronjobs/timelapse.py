#!/usr/bin/python
import os, time, datetime, sys, subprocess
from astral import Astral

where = "/var/www/lapse/"

# options: dawn, sunrise, noon, sunset, dusk
astral = Astral()
here = astral['San_Francisco']
def getSunTime( key ):
    sun = here.sun(date=datetime.datetime.now(), local=True)
    return sun[key]

def logMsg(msg):
	"""Update a log file"""
	f = file( where + "photoLog.html", "a" )
	f.write( msg + "\n" )
	f.close()

def snapPhoto(imgpath):
    webphotocmd = "raspistill -w 1024 -h 768 -t 1 -o %s" % imgpath
    subprocess.call( webphotocmd.split(" ") )
##    cropcmd = "/home/jp/src/momcrop.py %s" % imgpath
##    subprocess.call( cropcmd.split(" ") )


dawn = getSunTime('dawn')
dusk = getSunTime('dusk')

startTimeStr = datetime.datetime.now(tz=dawn.tzinfo).strftime("%y-%m-%d_%H-%M")
logMsg("<H1>Started at " + startTimeStr + "</H1>")

while (1):
    now = datetime.datetime.now(tz=dawn.tzinfo)
    if (now > dawn) and (now < dusk):
        nowStr = now.strftime("%y-%m-%d_%H-%M")
        snapPhoto( where + nowStr + ".jpg" )
        logMsg('<a href="/lapse/%s">%s</a><br>' % (nowStr, nowStr) )
    time.sleep( 60 * 10 )
    # Should just find these once per day
    dawn = getSunTime('dawn')
    dusk = getSunTime('dusk')
