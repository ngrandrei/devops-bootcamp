import boto3
import schedule

ec2_client = boto3.client("ec2", region_name="eu-west-1") # if region is not specified, it will take the default region in .aws directory
ec2_resource = boto3.resource("ec2", region_name="eu-west-1")


def check_instance_status():
    statuses = ec2_client.describe_instance_status(IncludeAllInstances=True) # include terminated instances also
    for status in statuses["InstanceStatuses"]:
        ins_status = status["InstanceStatus"]["Status"]
        sys_status = status["SystemStatus"]["Status"]
        state = status["InstanceState"]["Name"]
        print(
            f"Instance {status['InstanceId']} is {state} with instance status {ins_status} and system status {sys_status}"
        )
    print("#############################\n")


schedule.every(10).minutes.do(check_instance_status)

while True:
    schedule.run_pending() 

# this program will run forever but the function that checks the instance status will be called only at 10 minutes interval
