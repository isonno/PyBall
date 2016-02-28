#!/usr/bin/python

# Check the filesystem to make sure there's available space.
# Emails you if space is running low.

# Call this from the crontab file with something like:
#   00 10 * * * ~jp/src/checkdiskspace.py somebody@example.com
# where the argument is whatever email address should get notified.

import os, sys, time, smtplib, re, socket

def SendEmail( toAddr, body ):
	fromAddr = 'eye@eyeball'
	subject = 'MESSAGE FROM THE EYEBALL'
	msg = "To: %s\r\nFrom: %s\r\nSubject: %s\r\n\r\n%s\n" % (toAddr, fromAddr, subject, body)

	try:
		# NOTE: You need to supply your actual SMTP server here.
		server = smtplib.SMTP('mail.example.com', 587)
		server.sendmail(fromAddr, toAddr, msg)
		server.quit()
	except (smtplib.SMTPException, socket.gaierror, socket.herror, socket.error, socket.timeout), serverErr:
		print 'email failed: ' + serverErr.__str__()

def EnoughDiskSpace(path):
    stat = os.statvfs(path)
    bytesAvail = stat.f_frsize * stat.f_bavail
    # 750K jpg * 17 hours per day * 6 photos/hour * 2 days
    bytesNeeded = 750000L * 17L * 6L * 2L

    return bytesAvail > bytesNeeded

# Note the RE to check the valid email address is not 100% RFC-822
# complient.  But it should serve as a useful sanity check for most.
if (len(sys.argv) < 2) or not (re.match("^[\w.-]+@\w+[.]\w+$", sys.argv[1])):
    print "Must supply an email address"
    sys.exit(1)

if not EnoughDiskSpace("/var/www/lapse"):
    SendEmail(sys.argv[1], "Eyeball is running out of disk space!")

