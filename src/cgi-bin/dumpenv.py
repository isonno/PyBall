#!/bin/bash
echo -e "Content-type: text/html\n\n"
echo "<h1>Environment</h1>"
echo "<pre>"
printenv
echo "</pre>"
echo "<h2>And I am...</h2>"
echo "<pre>"
whoami
echo "</pre>"
