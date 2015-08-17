#!/usr/bin/python

# Upload the day's harvest of JPG files to attic
# for safe keeping and rapid access

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
SendFiles( "attic", "eyeball", "seemenow", photoList, remFolder )
