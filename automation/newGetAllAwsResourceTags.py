import boto3

region = 'us-east-2'

def get_ec2_tags(region):
    try:
        ec2 = boto3.resource('ec2', region)
        instances = ec2.instances.all()

        for instance in instances:
            print(f"EC2 Instance ID: {instance.id}")
            for tag in instance.tags:
                print(f"{tag['Key']}: {tag['Value']}")
            print("\n")
    except Exception as error:
        print(f"error in get_ec2_instance_tags() {str(error)}")
        

get_ec2_instance_tags(region)



