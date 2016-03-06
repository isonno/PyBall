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

maxEvents = 90
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

dateFormat = '<b>---{datestring}---</b><br>\n'
## eventFormat = ' <a href="http://{thisAddr}/{path}">{type}: {timestring}</a><br>\n'
eventFormat = ' {timestring}: <a href="http://{thisAddr}/{video}">Video</a> <a href="http://{thisAddr}/{image}">Image</a></br>\n'

curdate = datetime.date.today()
resultPage += "<b>---Today---</b><br>\n"

for f in allfiles[:maxEvents]:
    fileType = {'mp4':"Video", 'jpg':"Image"}[f[-3:]]
    timestamp = datetime.datetime.strptime(f[14:-4], "%Y%m%d_%H%M%S")

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
print resultPage
print "</body>"
