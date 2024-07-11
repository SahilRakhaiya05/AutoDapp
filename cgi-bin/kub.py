#!/usr/bin/env python3

import cgi
import cgitb
import subprocess

# Enable debugging
cgitb.enable()

# Function to print HTML content type header
def print_content_type():
    print("Content-type: text/plain\n")

# Function to execute kubectl commands and return output or error message
def execute_kubectl_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return str(e.output.decode("utf-8"))

# Function to list pods
def list_pods():
    print_content_type()
    command = ["kubectl", "get", "pods", "--no-headers"]
    print(execute_kubectl_command(command))

# Function to launch a pod
def launch_pod(pod_name):
    print_content_type()
    if not pod_name:
        print("Error: Pod name is required.")
        return
    command = ["kubectl", "run", pod_name, "--image=nginx", "--restart=Never"]
    print(execute_kubectl_command(command))

# Function to delete a pod
def delete_pod(pod_name):
    print_content_type()
    if not pod_name:
        print("Error: Pod name is required.")
        return
    command = ["kubectl", "delete", "pod", pod_name]
    print(execute_kubectl_command(command))

# Function to scale replicas
def scale_replica(pod_name, replica_count):
    print_content_type()
    if not pod_name or not replica_count.isdigit():
        print("Error: Pod name and valid replica count are required.")
        return
    command = ["kubectl", "scale", "--replicas="+replica_count, "deployment/"+pod_name]
    print(execute_kubectl_command(command))

# Function to describe a pod
def describe_pod(pod_name):
    print_content_type()
    if not pod_name:
        print("Error: Pod name is required.")
        return
    command = ["kubectl", "describe", "pod", pod_name]
    print(execute_kubectl_command(command))

# Function to get logs of a pod
def get_logs(pod_name):
    print_content_type()
    if not pod_name:
        print("Error: Pod name is required.")
        return
    command = ["kubectl", "logs", pod_name]
    print(execute_kubectl_command(command))

# Main CGI logic
def main():
    form = cgi.FieldStorage()

    operation = form.getvalue("operation")
    pod_name = form.getvalue("name")
    replica_count = form.getvalue("replica")

    if operation == "listPods":
        list_pods()
    elif operation == "launchPod":
        launch_pod(pod_name)
    elif operation == "deletePod":
        delete_pod(pod_name)
    elif operation == "scaleReplica":
        scale_replica(pod_name, replica_count)
    elif operation == "describePod":
        describe_pod(pod_name)
    elif operation == "getLogs":
        get_logs(pod_name)
    else:
        print_content_type()
        print("Invalid operation.")

if __name__ == "__main__":
    main()
