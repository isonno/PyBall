#!/usr/bin/python

# CGI to shrink an image

import os, sys, cgi, urlparse

from PIL import Image

queryDict = urlparse.parse_qs( os.getenv("QUERY_STRING") )
# By default, the query dict allows multiple values per key.  Flatten this
for k in queryDict.keys():
    if (len(queryDict[k]) == 1):
        queryDict[k] = queryDict[k][0]

webDir = "/var/www/lapse/"
bottomCrop = 250

img = Image.open(webDir + queryDict['imageName'])
img = img.resize( (img.size[0] >> 1, img.size[1] >> 1) )


print "Content-Type: image/jpeg"
print
img.save(sys.stdout, quality=80)
