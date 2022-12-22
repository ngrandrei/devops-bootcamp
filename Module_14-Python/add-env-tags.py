import boto3

ec2_client_ireland = boto3.client('ec2', region_name="eu-west-1")
ec2_resource_ireland = boto3.resource('ec2', region_name="eu-west-1")

ec2_client_frankfurt = boto3.client('ec2', region_name="eu-central-1")
ec2_resource_frankfurt = boto3.resource('ec2', region_name="eu-central-1")

instance_ids_ireland = [] # all the instance ids from ireland
instance_ids_frankfurt = [] # all the instance ids from frankfurt

reservations_ireland = ec2_client_ireland.describe_instances()['Reservations']
for res in reservations_ireland:
    instances = res['Instances']
    for ins in instances:
        instance_ids_ireland.append(ins['InstanceId'])


response = ec2_resource_ireland.create_tags(
    Resources=instance_ids_ireland,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

reservations_frankfurt = ec2_client_frankfurt.describe_instances()['Reservations']
for res in reservations_frankfurt:
    instances = res['Instances']
    for ins in instances:
        instance_ids_frankfurt.append(ins['InstanceId'])


response = ec2_resource_frankfurt.create_tags(
    Resources=instance_ids_frankfurt,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)