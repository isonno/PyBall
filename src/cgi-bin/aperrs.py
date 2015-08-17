#!/bin/bash
echo -e "Content-type: text/html\n\n"
echo "<h1>Apache Error Log</h1>"
echo "<pre>"
tail -50 /var/log/apache2/error.log
echo "</pre>"
echo "<h2>Recent access</h2>"
echo "<pre>"
tail -10 /var/log/apache2/access.log
echo "</pre>"
