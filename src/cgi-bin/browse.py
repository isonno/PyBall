#!/usr/bin/python
#
# Script to check on today's progress of the images
#
import os, datetime, socket, glob, urlparse, json, sys

# Mobile devices in the house can't resolve the hostname
# Use IP Address instead.
##hostname = socket.gethostname()
hostname = socket.getaddrinfo(socket.gethostname(),
							  80, socket.AF_INET)[0][4][0]
webdir = "/var/www/lapse"

os.chdir(webdir)
allPhotos = glob.glob("*.jpg")
allPhotos.sort()

# urlparse.parse_qs("date-start=16-03-19;date-end=16-03-20")
# datetime.datetime.strptime("16-05-22", "%y-%m-%d")
queryDict = urlparse.parse_qs( os.getenv("QUERY_STRING") )
# By default, the query dict allows multiple values per key.  Flatten this
for k in queryDict.keys():
    if (len(queryDict[k]) == 1):
        queryDict[k] = queryDict[k][0]

def photoDate(s):
    return datetime.datetime.strptime(s, "%y-%m-%d_%H-%M-%S.jpg")

def strDate(s):
    return datetime.datetime.strptime(s[:8], "%y-%m-%d")

def dumpWithinDates():
    startDate = strDate(queryDict['date-start'] if queryDict.has_key('date-start') else allPhotos[0] )
    endDate = strDate(queryDict['date-end'] if queryDict.has_key('date-end') else allPhotos[-1:]) 
    endDate = endDate + datetime.timedelta(1) # Include last day

    def insideDate(s):
        picDate = photoDate(s)
        return picDate >= startDate and picDate < endDate

    return json.dumps([s for s in allPhotos if insideDate(s)])

if (queryDict.has_key('date-start') or queryDict.has_key('date-end')):
    print "Content-Type: text/json"
    print
    print dumpWithinDates()
