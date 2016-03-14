#!/usr/bin/python
#
# CGI Script to display files uploaded by the DLink DCS-942L camera
#
# The DLink DCS-942L can be set up to automatically FTP a video clip
# every time it detects motion.  The uploaded video clips also
# include a snapshot JPEG image as well.  This script catalogs all of
# the uploaded clips, and builds a thumbnail catalog web page of the
# most recent clips.
#
# John Peterson, March 2016
#

import os, datetime, socket, glob, urlparse, json, sys

# This host's IP address is a string in the form 'xxx.xxx.xxx.xxx'
thisIP = socket.getaddrinfo(socket.gethostname(), 80, socket.AF_INET)[0][4][0]

# Where the files are sent by the camera.  This directory should be accessible
# by the apache web server.
webdir = "/var/www/window"

# This selects how many thumbnails are presented.
maxEvents = 120


os.chdir(webdir)

# Stupid camera makes folders for date AND hour.
allfiles = glob.glob("*/*/*")

# Filenames are of the form:
# YYYYMMDD/HH/v_YYYYMMDD_HHMMSS.mp4  (video)
# YYYYMMDD/HH/v_YYYYMMDD_HHMMSSD.mp4 (video)  ('D' indicates daylight savings)
# YYYYMMDD/HH/i_YYYYMMDD_HHMMSS.jpg  (image)
# YYYYMMDD/HH/i_YYYYMMDD_HHMMSSD.jpg  (image)

# Start and end string postions of the time stamp
ts0 = 14
ts1 = 29

def sortfun(a,b):
    return 1 if a[ts0:ts1] < b[ts0:ts1] else -1

allfiles.sort(sortfun)  # Most recent first

resultPage = "<body>\n"

dateFormat = '<div class="date">---{datestring}---</div>\n'

eventFormat = '<a href="http://{thisAddr}/{video}"><div class="thumbox"> <img src="http://{thisAddr}/{image}" width="200" height="150"><br>{timestring}</div></a>\n'

curdate = datetime.date.today()
resultPage += dateFormat.format(datestring="Today")
lastImage = ""

for f in allfiles[:maxEvents]:
    fileType = {'mp4':"Video", 'jpg':"Image"}[f[-3:]]
    timestamp = datetime.datetime.strptime(f[ts0:ts1], "%Y%m%d_%H%M%S")

    # New day, insert a date header
    if (timestamp.date() != curdate):
        datestr = timestamp.strftime("%d-%b")
        resultPage += dateFormat.format(datestring=datestr)
        curdate = timestamp.date()

    # The last image before the video corresponds to the video
    if (fileType == "Image"):
        lastImage = f
        continue

    timestr = timestamp.strftime("%I:%M:%S %p")
    eventLine = eventFormat.format(timestring=timestr, thisAddr=thisIP, video="window/"+f,
                                   image="window/"+lastImage)
    resultPage += eventLine

print "Content-Type: text/html"
print
print "<head>"
print '  <link href="../eventfmt.css" rel="stylesheet" type="text/css">'
print '  <title>Recorded camera events</title>'
print '</head>'
print resultPage
print "</body>"
