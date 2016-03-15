D-Link DCS-942L Server
======================

This is a web server for displaying the images captured by the D-Link DCS-942L (also sold as the "Cloud Camera 1200").

The DCS-942L automatically uploads a video clip every time it detects motion (see Setup > Video Clip on the camera's
server to set this up).  You can also have it upload a snapshot for every motion clip captured (Setup > Snapshot).  By setting up both of these uploads, it's straightforward to get a thumbnailed catalog of video clips.  The script in the `cgi-bin` folder creates a web page for this. (Camera setup details TBD...)

If you install the files in this folder set using:
```
sudo ./setup.py
```
the web server's home page displays the camera's live video.  If you click on the "Events" link, you're shown a set of thumbnails
of the last hundred or so video clips the camera captured, cataloged and timestamps.  Clicking on a thumbnail plays the corresponding 
video clip.

### Issues.  So many issues.

* You'll need to edit `index.html` to reflect the account, password and IP address of your camera.
  * You can add accounts and passwords to your camera under Maintenance > Admin.  I recommend you set up another account for accessing the live video, so your admin password isn't broadcast on the web page.
  * Unless you have DNS configured on your local network, use the numeric IP address, not a hostname.  Phones and tables won't have a hosts file.
* The live video feed often comes up blank.  Click "Fix" and then back, and it's fine.  I suspect this is a browser caching issue that can be fixed with some JavaScript...
* __DO NOT RUN THIS ON THE OPEN INTERNET__
  * Everything about these scripts assumes running behind a firewall.  If you put this code on the open internet, your camera goes live on YouTube and the haxors steal your Bitcoins.
* This is running on Raspbian on a Raspberry Pi-2B.  I haven't tested it on other Apache/Linux configureations.
  * Raspberry Pi's work great when you need to leave a computer on as a web server or whatever.  For $50, they make great lightweight servers.
