#!/usr/bin/python
#
# Watch the camera, saving interesting delta images
#

import os, time, datetime, sys, subprocess
from PIL import Image
from PIL import ImageChops
from PIL import ImageStat
import numpy					# For mean()

where = "/var/www/watch/"
delay = 1                       # Seconds
rmsThreshold = 9

# options: dawn, sunrise, noon, sunset, dusk

def logMsg(msg):
	"""Update a log file"""
	f = file( where + "photoLog.html", "a" )
	f.write( msg + "\n" )
	f.close()

def snapPhoto(imgpath):
    webphotocmd = "raspistill -vf -w 1024 -h 768 -t 1 -o %s" % imgpath
    subprocess.call( webphotocmd.split(" ") )

def getNowDateStr():
    return datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")

def getNowPhotoPath():
    return where + getNowDateStr() + ".jpg"

def openShrunkImg( path ):
    img = Image.open( path )
    img = img.resize( (img.size[0] >> 2, img.size[1] >> 2) )
    return img

logMsg("<H1>Started at " + getNowDateStr() + "</H1>")

basePhoto = getNowPhotoPath()
snapPhoto( basePhoto )

while (1):
    time.sleep( delay )
    newPhoto = getNowPhotoPath()
    snapPhoto( newPhoto )

    baseImg = openShrunkImg( basePhoto )
    newImg = openShrunkImg( newPhoto )

    deltaImg = ImageChops.difference( baseImg, newImg )
    deltaImg.save( where + "delta.jpg" )
    deltaStats = ImageStat.Stat( deltaImg )
    rmsValue = numpy.mean( deltaStats.rms )
#    print "Threshold: " + str(rmsValue)
    if (rmsValue < rmsThreshold):
	os.remove( newPhoto )
    else:
        logMsg('Image <a href="http://myball/watch/%s">%s</a>, thresh %s<br>' %
	       (os.path.basename(newPhoto), os.path.basename(newPhoto),
		str(rmsValue)))
#	print "Keeping(str%s): " % str(rmsValue) + basePhoto	
	basePhoto = newPhoto

