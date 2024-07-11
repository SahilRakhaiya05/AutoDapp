#!/usr/bin/python3

import cgi
import subprocess

# Get CGI form data
form = cgi.FieldStorage()

# Retrieve the command from the CGI parameters
cmd = form.getvalue('cmd')

# Set content type to HTML
print("Content-type: text/html")
print()

# Execute the Docker command with sudo
finalCommand = "sudo " + cmd
output = subprocess.getoutput(finalCommand)

# Print HTML response
print("<html>")
print("<head><title>Docker Command Execution</title></head>")
print("<body>")
print("<h1>Output of Docker Command:</h1>")
print("<pre>{}</pre>".format(output))
print("</body>")
print("</html>")
