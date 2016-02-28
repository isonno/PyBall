#!/usr/bin/python
#
# CGI Script to display files uploaded by the DLink DCS-942L camera
#

import os, datetime, socket, glob, urlparse, json, sys

# We need this and the the camera's IP address,
# because the phones & tablets won't have a local hostfile

windowCamIP = socket.getaddrinfo("windowcam", 80, socket.AF_INET)[0][4][0]
thisIP = socket.getaddrinfo(socket.gethostname(), 80, socket.AF_INET)[0][4][0]

# Where the files are sent by the camera:

webdir = "/var/www/window"

os.chdir(webdir)

# Stupid camera makes folders for date AND hour.
allfiles = glob.glob("*/*/*")

# Filenames are of the form:
# YYYYMMDD/HH/v_YYYYMMDD_HHMMSS.mp4  (video)
# YYYYMMDD/HH/i_YYYYMMDD_HHMMSS.jpg  (image)

def sortfun(a,b):
    return 1 if a[-19:] < b[-19:] else -1

allfiles.sort(sortfun)  # Most recent first

resultPage = """<head><title>Captured events</title></head>
<body>
<H1>Captured Events</H1>
"""

eventFormat = ' <a href="http://{thisAddr}/{path}">{type}: {day}-{month}, {hour}:{min}:{sec}</a><br>\n'

for f in allfiles[:60]:
    fileType = {'mp4':"Video", 'jpg':"Image"}[f[-3:]]
    monthNum = int(f[4:6])-1
    monthName = "JanFebMarAprMayJunJulAugSepOctNovDec"[monthNum*3:monthNum*3+3]
    eventLine = eventFormat.format(type=fileType, thisAddr=thisIP, path="window/"+f, day=f[6:8], 
                                  month=monthName, hour=f[23:25], min=f[25:27], sec=f[27:29] )
    resultPage += eventLine

print "Content-Type: text/html"
print
print resultPage
print "</body>"