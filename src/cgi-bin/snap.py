#!/usr/bin/python
#
# CGI script to snap a photo on the raspi and return a web page with
# the result.
#
import subprocess, datetime, socket

hostname = socket.gethostname()
webdir = "/var/www/"
imgpath = webdir + "now.jpg"

webphotocmd = "raspistill -w 1024 -h 768 -t 1 -o %s" % imgpath

subprocess.call( webphotocmd.split(" ") )

datestr = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

resultPage = """<head><title>Current photo</title></head>
<body>
<H1>Current photo</H1>
<p>
%s
<p>
<img src="http://%s/now.jpg">
<p>
</body>""" % (datestr, hostname)

print "Content-Type: text/html"
print
print resultPage
