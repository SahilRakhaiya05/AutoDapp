#!/usr/bin/env python3
import cgi
import os
import boto3

# CGI headers
print("Content-Type: text/html")
print()

# Parse form data
form = cgi.FieldStorage()

# Extract topic name from form data
topic_name = form.getvalue('name')

# Retrieve AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = 'your_aws_region'  # Replace with your AWS region

# Check if credentials are set
if not aws_access_key_id or not aws_secret_access_key:
    print("<p>AWS credentials not configured properly.</p>")
    exit()

# AWS SNS client setup
try:
    sns = boto3.client('sns', region_name=aws_region,
                       aws_access_key_id=aws_access_key_id,
                       aws_secret_access_key=aws_secret_access_key)

    # Create SNS topic
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    print(f"<p>Successfully created SNS topic with ARN: {topic_arn}</p>")
except Exception as e:
    print(f"<p>Error creating SNS topic: {e}</p>")
