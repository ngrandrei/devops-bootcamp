# Automation with Python

Module 13 was pretty easy, I'll skip it.

While Terraform is best used to provision infrastructure, Python can be used to automate some repetitive tasks regarding already created infrastructure. You can do regular back-ups, regular clean-ups, health-checks & monitoring, etc.\

TF knows the state of the infrastructure, Python does not track that. TF is also idempotent, while Python not.\

I'm using pyenv to manage multiple versions of python and dependencies between different project with virtualenv.\

- Install pyenv
- Create a virtualenv with the python versions you want. For example: `pyenv virtualenv 3.9.4 devops-work` - will create devops-work virtulenv using version 3.9.4 of python
- `pyenv activate devops-work` - activate the virtual env. All the dependencies installed with pip will be added into this virtual env.

## Project 1

**EC2 Status check**

1. Create an EC2 instance with Terraform or using console

2. Write a Python script that checks the EC2 Status checks based on a schedule 

`pip install schedule` and `pip install boto3` - install boto3 and scheduler

Use the boto3 documentation to see diffrent functions and the JSON returned.

Script name: `ec2-status-check.py`

---

## Project 2

**Python script that adds environment tags to all EC2 instances**

1. Iterrate over all instances in all reservations and collect the ids in a list for each reagion. 

2. You can use only one call to AWS to update all the instances tag by providing the list with ids to the `Resources` key parameter.

Script name: `add-env-tags.py`

--- 

## Project 3

**Python script that displays info about EKS clusters**

1. Use Terraform to deploy EKS clusters 

2. Fetch Status, Endpoint and Versions of the K8s

Script name: `eks-info.py`

---

## Project 4

**Data backup & restore**

1. Create Python script that automates creating backup for EC2 Volumes 

Script name: `volume-backup.py`

2. Create Python script that cleans up old snapshots

Script name: `cleanup-snapshots.py`

3. Create Python script that resores Volumes from Snapshots

Script name: `restore-volumes.py`

---

## Project 5

**Nginx server monitoring and recovery**

1. Create a server on any cloud platform

2. Install docker and run a nginx docker container

3. Create functions to restart the reboot the server first and then restart the docker container

To restart the server you can use boto3 and for the docker container you first need to SSH into the server using `paramiko`. 

4. Create function that sends an email notification

5. Create function that monitors the nginx server at 5 minutes interval using `requests` module. 

Script name: `monitor-nginx.py`

