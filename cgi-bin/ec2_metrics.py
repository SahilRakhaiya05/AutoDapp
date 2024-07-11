#!/usr/bin/env python3
import cgi
import boto3
from botocore.exceptions import ClientError
import json

# Required headers for CGI response
print("Content-Type: text/plain")
print()  # Blank line required by CGI protocol

# Parse incoming form data
form = cgi.FieldStorage()

# Retrieve values from form fields
instance_id = form.getvalue('instanceId', '').strip()
aws_access_key = form.getvalue('awsAccessKey', '').strip()
aws_secret_key = form.getvalue('awsSecretKey', '').strip()
region_name = form.getvalue('regionName', '').strip()

# Initialize Boto3 session with explicit credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

# Initialize EC2 client with the session
ec2_client = session.client('ec2')

# Placeholder for metrics data
metrics_data = {}

try:
    # Describe instance status to fetch metrics
    response = ec2_client.describe_instance_status(
        InstanceIds=[instance_id],
        IncludeAllInstances=True
    )

    # Extract relevant metrics data
    instance_statuses = response.get('InstanceStatuses', [])
    if instance_statuses:
        instance_status = instance_statuses[0]
        metrics_data = {
            "InstanceId": instance_status['InstanceId'],
            "InstanceState": instance_status['InstanceState']['Name'],
            "InstanceStatus": instance_status['InstanceStatus']['Status'],
            "SystemStatus": instance_status['SystemStatus']['Status']
        }
    else:
        metrics_data = {
            "error": "Instance not found or metrics not available."
        }

except ClientError as e:
    error_message = e.response['Error']['Message']
    metrics_data = {
        "error": f"AWS Error: {error_message}"
    }

# Output JSON response
print(json.dumps(metrics_data))
