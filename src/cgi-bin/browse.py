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

def queryDate(s):
    return datetime.datetime.strptime(s, "%y-%m-%d")

startDate = queryDate(queryDict['date-start'])
endDate = queryDate(queryDict['date-end']) + datetime.timedelta(1) # Include last day

def insideDate(s):
    picDate = photoDate(s)
    return picDate >= startDate and picDate < endDate

selPhotos = [s for s in allPhotos if insideDate(s)]

def sendSimplePage(photoIndex):
	prevPhoto = max(photoIndex-1, 0)
	nextPhoto = min(photoIndex+1, len(allPhotos)-1)
	skipPhoto = min(photoIndex+6, len(allPhotos)-1)

	datestr = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

	resultPage = """<head><title>Preview photos</title></head>
	<body>
	<H1>Preview</H1>
	<p>
	<img src="http://{host}/cgi-bin/shrink?imageName={curImg}">
	<p>
	{curImg}
	<p>
	<a href="http://{host}/cgi-bin/check?photoIndex={cur}&stepDay=-1">Prev Day</a> &nbsp;
	<a href="http://{host}/cgi-bin/check?photoIndex={prev}">Previous</a> &nbsp;
	<a href="http://{host}/cgi-bin/check?photoIndex={next}">Next</a> &nbsp;
	<a href="http://{host}/cgi-bin/check?photoIndex={skip}">Next Hour</a> &nbsp;
	<a href="http://{host}/cgi-bin/check?photoIndex={cur}&stepDay=1">Next Day</a>
	</body>""".format(host=hostname, curImg=allPhotos[photoIndex],
					  prev=prevPhoto, next=nextPhoto, skip=skipPhoto,
					  cur=photoIndex)

	print "Content-Type: text/html"
	print
	print resultPage

def stepDay(photoIndex, dayStep):
	def sign(n):
		if (n < 0):
			return -1
		if (n > 0):
			return 1
		return 0

	curDayHr = datetime.datetime.strptime( allPhotos[photoIndex],
											"%y-%m-%d_%H-%M.jpg")
	backDay = curDayHr + datetime.timedelta(dayStep) # back up a day
	backDayStr = backDay.strftime( "%y-%m-%d_%H")
	while ((photoIndex > 0)
			and (allPhotos[photoIndex][:len(backDayStr)] != backDayStr)):
		photoIndex += sign(dayStep)
	return photoIndex

def getDateIndex(dateStr):
	for i in range(len(allPhotos)):
		if allPhotos[i][0:len(dateStr)] == dateStr:
			return i

currentPhoto = 0

if (queryDict.has_key('photoIndex')):
	currentPhoto=int(queryDict['photoIndex'])
	if (queryDict.has_key('stepDay')):
		currentPhoto = stepDay( currentPhoto, int(queryDict['stepDay']) )

elif (queryDict.has_key('photoList')):
	photoIndex = getDateIndex(queryDict['photoList'])
	print "Content-type: text/json"
	print
	print json.dumps(allPhotos[photoIndex:])
	sys.exit(1)

else:
	# Find today's file in the list
	todayStr = (datetime.datetime.now()-datetime.timedelta(1)).strftime("%y-%m-%d")
	currentPhoto = getDateIndex(todayStr)

sendSimplePage(currentPhoto)
