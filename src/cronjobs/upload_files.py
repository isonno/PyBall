#!/usr/bin/python

# Upload the day's harvest of JPG files to a remote host
# for safe keeping and rapid access.  Requires shell definitions
# for the host, username and password to upload the files to.
# UPLOADHOST, UPLOADUSERNAME and UPLOADPASSWORD, respectively.

import ftplib, os, glob, datetime, sys

localFiles = "/var/www/lapse/"
remFolder = "/s2/eyeball"

def SendFiles( host, user, key, sendfiles, remoteFolder ):
	ftp = ftplib.FTP(host)
	ftp.login( user, key )
	ftp.cwd( remoteFolder )

	for f in sendfiles:
		print "Sending %s..." % f
		ftp.storbinary("STOR " + f, file(f, 'rb'))
		ftp.sendcmd("chmod 644 %s" % f)

	ftp.quit()

todayStr = datetime.datetime.now().strftime("%y-%m-%d")
if (len(sys.argv) == 2):
    todayStr = sys.argv[1]

os.chdir(localFiles)
photoList = glob.glob(localFiles + todayStr + *.jpg)
SendFiles( os.getenv("UPLOADHOST"), 
           os.getenv("UPLOADUSERNAME"), 
           os.getenv("UPLOADPASSWORD"), photoList, remFolder )
