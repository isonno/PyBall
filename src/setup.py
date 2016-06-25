#!/usr/bin/python

# Setup the PyBall environment for time-lapse photography
#
# J. Peterson, Aug-2015
#

#
# This script does installs the various components for basic
# PyBall operation.  It must be run via sudo:
#
#  sudo ./setup.py
#
# NOTE: This script, and the scripts therin, have not be extensively
# vetted for security issues.  They assume the Raspberry PI is dedicated
# to the task of running the PyBall scripts, and running on a local
# network where it is not subject to attack from the Internet at large.
#
#
import os, pwd, shutil, subprocess, stat, glob

# Grab the username from the owner of this script, since
# we'll be running as root and don't want to use that as "thisUser"
thisUser = pwd.getpwuid( os.stat(__file__).st_uid ).pw_name

# Run a shell command & return output, trimming off the newline
def shellCmd(cmdLine):
	return subprocess.Popen( cmdLine, shell=True, stdout=subprocess.PIPE).stdout.read()[:-1]

def isDir(path):
    return os.path.exists( path ) and os.path.isdir(path)

def chown( path, user, group ):
    os.chown( path, pwd.getpwnam(user).pw_uid, pwd.getpwnam(group).pw_gid )

def setupDir(path, user, group ):
    if (not isDir(path)):
        os.makedirs( path )
    os.chmod( path, 0755 ); # Set user/group to root
    chown( path, user, group )

def copyFile( src, dest, user=None, group=None, mode=None ):
    shutil.copy( src, dest )

    if (user and group and mode):
        if (os.path.isdir(dest)):
            dest += os.sep + os.path.basename(src)
        os.chmod( dest, mode )
        chown( dest, user, group )

# Set up apache / camera access
shellCmd( "usermod -G video www-data" ) # So www-data can access the camera
shellCmd( "chmod a+rx /var/log/apache2" ) # Make the log files visible
shellCmd( "chmod a+r /var/log/apache2/*" )

# set up www folder
setupDir( "/var/www/lapse", thisUser, "root" )
setupDir( "/var/www/camimg", "www-data", "root" )

# Copy in CGI scripts
for f in (glob.glob("cgi-bin/*.py")):
    copyFile( f, "/usr/lib/cgi-bin/" + os.path.basename(f).split('.')[0],
			  "root", "root", 0755 )

# Copy web site
for f in (glob.glob("www/*")):
	copyFile( f, "/var/www/" + os.path.basename(f), "root", "root", 0644 )

# Set up the crontab jobs
cronPath = os.path.abspath(os.path.dirname(__file__)) + "/cronjobs/"

# Make sure crontab scripts are executable
for f in (glob.glob(cronPath + "*.py")):
	os.chmod( f, 0751 )
	
# Create the chrontab file and install it
if False:
	cronFilePath = cronPath + "crontab.tmp"
	cronTabFile = file( cronFilePath, 'w' )
	cronTabFile.write( "# Crontab for pyball\n" )
	cronTabFile.write( "@reboot %stimelapse.py\n" % cronPath )
	cronTabFile.write( "00 23 * * * %supload_files.py\n" % cronPath )
	cronTabFile.close()

	shellCmd( "crontab -u %s %s" % (thisUser, cronFilePath) )

