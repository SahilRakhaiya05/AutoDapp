#!/usr/bin/env python3
import cgi
import boto3
from botocore.exceptions import ClientError
import json

# Required headers for CGI response
print("Content-Type: application/json")
print()  # Blank line required by CGI protocol

# Parse incoming query parameters
params = cgi.FieldStorage()
log_group_name = params.getvalue('logGroupName', '').strip()
log_stream_name = params.getvalue('logStreamName', '').strip()
region_name = params.getvalue('regionName', '').strip()
aws_access_key_id = params.getvalue('awsAccessKey', '').strip()
aws_secret_access_key = params.getvalue('awsSecretKey', '').strip()

# Initialize Boto3 client for CloudWatch Logs with explicit credentials
logs_client = boto3.client('logs', region_name=region_name,
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key)

# Placeholder for logs data
logs_data = []

try:
    # Fetch logs from CloudWatch Logs
    response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        limit=20,  # Adjust as needed
        startFromHead=True
    )

    # Process response to extract log events
    events = response.get('events', [])
    for event in events:
        log_entry = {
            'timestamp': event['timestamp'],
            'message': event['message']
        }
        logs_data.append(log_entry)

except ClientError as e:
    error_message = f"AWS Error: {e}"
    logs_data = [{
        'error': error_message
    }]

# Output JSON response
print(json.dumps(logs_data))
