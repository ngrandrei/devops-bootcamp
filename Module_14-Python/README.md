# Automation with Python

Module 13 was pretty easy, I'll skip it.

I'm using pyenv to manage multiple versions of python and dependencies between different project with virtualenv.

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

--- 

## Project 3

****

