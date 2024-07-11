#!/usr/bin/env python3

import cgi
import json
import boto3
from botocore.exceptions import ClientError

# Required headers for CGI response
print("Content-Type: application/json")
print()  # Blank line required by CGI protocol

# Parse incoming form data
form = cgi.FieldStorage()

# Retrieve values from form fields
name = form.getvalue('name', '').strip()
action = form.getvalue('action', '').strip()

# AWS credentials (Access Key ID and Secret Access Key)
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'
region_name = 'your_region'  # Specify the AWS region

# Initialize Boto3 session with explicit credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Initialize IAM client with the session
iam = session.client('iam')

# Placeholder for response data
response_data = {}

try:
    if action == 'create':
        # Create IAM user
        iam.create_user(UserName=name)
        response_data = {
            "status": "success",
            "message": f"User '{name}' created successfully."
        }
    elif action == 'delete':
        # Delete IAM user
        iam.delete_user(UserName=name)
        response_data = {
            "status": "success",
            "message": f"User '{name}' deleted successfully."
        }
    else:
        response_data = {
            "status": "error",
            "message": "Invalid action specified."
        }
except ClientError as e:
    error_message = e.response['Error']['Message']
    response_data = {
        "status": "error",
        "message": f"AWS Error: {error_message}"
    }

# Output JSON response
print(json.dumps(response_data))
