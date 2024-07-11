#!/usr/bin/env python3

import cgi
import cgitb
import json
from twilio.rest import Client

# Enable CGI error reporting
cgitb.enable()

# Get form data
form = cgi.FieldStorage()

# Twilio credentials and message details
account_sid = ''
auth_token = ''
twilio_whatsapp_number = ''

recipient_number = form.getvalue('recipient_number')
message_body = form.getvalue('message_body')

# Set the content type to application/json
print("Content-Type: application/json\n")

response = {}

# Validate required fields
if not all([account_sid, auth_token, twilio_whatsapp_number, recipient_number, message_body]):
    response['error'] = 'All fields are required.'
else:
    try:
        # Initialize the Twilio client
        client = Client(account_sid, auth_token)

        # Send WhatsApp message
        message = client.messages.create(
            body=message_body,
            from_=f'whatsapp:{twilio_whatsapp_number}',
            to=f'whatsapp:{recipient_number}'
        )

        # Success response
        response['message'] = 'Message sent successfully!'
        response['sid'] = message.sid

    except Exception as e:
        # Error handling
        response['error'] = str(e)

# Output the result as JSON
print(json.dumps(response))
