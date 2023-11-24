import boto3

region = 'us-east-2'
cw_tags_lst = []

def get_cloudwatch_alarms(region):
    try:
        # Create CloudWatch client
        cloudwatch = boto3.client('cloudwatch', region_name=region)        

        # Get all cloudwatch alarms
        response = cloudwatch.describe_alarms()    

        # Extract information from the response
        alarms = response['MetricAlarms']

        return alarms
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')


def get_alarm_tags(alarm_name, region):
    try:
        # Create CloudWatch client
        cloudwatch = boto3.client('cloudwatch', region_name=region)        

        # Get tags for a specific CloudWatch alarm
        response = cloudwatch.list_tags_for_resource(ResourceARN=alarm_name)
        
        # Extract tags from the response
        tags = response['Tags']

        return tags
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')


def get_eb_environment_details(environment_id, region):
    try:
        # Create an Elastic Beanstalk client
        eb = boto3.client('elasticbeanstalk', region_name=region) 

        # Get information about the environment
        response = eb.describe_environments(EnvironmentIds=[environment_id])

        return response
    except Exception as error:
        print(f'Exception in get_eb_environment_details() {str(error)}')


def get_eb_environment_tags(environment_id, region):
    try:
        # Create an Elastic Beanstalk client
        eb = boto3.client('elasticbeanstalk', region_name=region)

        # Get the ARN for the Elastic Beanstalk environment
        response = eb.describe_environments(EnvironmentIds=[environment_id])
        environment_arn = response['Environments'][0]['EnvironmentArn']

        # Get tags for the Elastic BeanStalk environment
        response = eb.list_tags_for_resource(ResourceArn=environment_arn)

        # Extract tags from the response
        tags = response.get('ResourceTags', [])

        return tags
    except Exception as error:
        print(f'Exception in get_eb_environment_tags() {str(error)}')


def add_cloudwatch_alarm_tags(alarm_arn, tags, region):
    try:
        # create a CloudWatch client
        cloudwatch = boto3.client('cloudwatch', region_name=region)                    

        # Get the ARN for the CloudWatch alarm
        cloudwatch.tag_resource(ResourceARN=alarm_arn, Tags=tags)

    except Exception as error:
        print(f'Exception in add_cloudwatch_alarm_tags() {str(error)}')


def main():
    try:
        alarms = get_cloudwatch_alarms(region)        

        # Get information about each alarm and its tags
        for alarm in alarms:
            alarm_arn = alarm['AlarmArn']            
            print(f'alarm_arn: {alarm_arn}')

            alarm_name = alarm_arn.split(':')[-1]            
            print(f'alarm_name: {alarm_name}')
            
            count = 0
            count_t = 0
            # Check whether alarm is Elastic Beanstalk
            if len(alarm_name.split('-')) == 6 and count < 1:
                count += 1
                alarmStr = alarm_name.split('-')[2]                
                environment_id = 'e-' + alarmStr
                print(environment_id)
                print(get_eb_environment_tags(environment_id, region))
                environment_tags = get_eb_environment_tags(environment_id, region)
                for tag in environment_tags:
                    print(f"{tag['Key']}: {tag['Value']}")
                    if 'sce:app:name' in tag['Key']:
                        new_tag = {'Key': 'sce:app:name', 'Value' : tag['Value']}
                        cw_tags_lst.append(new_tag)
                    elif 'sce:app:region' in tag['Key']:                                
                        new_tag = {'Key': 'sce:app:region', 'Value' : tag['Value']}
                        cw_tags_lst.append(new_tag)
                    elif 'sce:component:name' in tag['Key']:                        
                        new_tag = {'Key': 'sce:component:name', 'Value' : tag['Value']}
                        cw_tags_lst.append(new_tag)
                    elif 'sce:app:costcenter' in tag['Key']:                         
                        new_tag = {'Key': 'sce:app:costcenter', 'Value' : tag['Value']}
                        cw_tags_lst.append(new_tag)
                    elif 'sce:app:environment' in tag['Key']:                    
                        new_tag = {'Key': 'sce:app:environment', 'Value' : tag['Value']}
                        cw_tags_lst.append(new_tag)
                    elif 'sce:service:name' in tag['Key']:
                        service_name = tag['Value'].replace("ebs", "cloudwatch")
                        print(f'service_name: {service_name}')
                        new_tag = {'Key': 'sce:service:name', 'Value' : service_name }
                        cw_tags_lst.append(new_tag)
                print('cloud watch tags:')
                print(cw_tags_lst)                
                #add_cloudwatch_alarm_tags(alarm_arn, cw_tags_lst, region)
                cw_tags_lst.clear()
                print('Success!!!')                            
            elif 'TargetTracking-asg' in alarm_name and count_t < 1:
                count_t += 1
                environment = alarm_name.split('-')[2]
                cw_region = alarm_name.split('-')[3]
                app = 'ecat'
                #component_name = alarm_name.split('-')[2] + alarm_name.split('-')[3] + alarm_name.split('-')[4] + alarm_name.split('-')[5]
                component_name = alarm_name.split('-', 4)[2]
                print(component_name)
                service_name = 'cloudwatch-' + component_name
                tags_to_add = [                                    
                        {'Key': 'sce:app:name', 'Value': app },
                        {'Key': 'sce:app:region', 'Value': cw_region },
                        {'Key': 'sce:component:name', 'Value': component_name },
                        {'Key': 'sce:app:costcenter', 'Value': '104293' },
                        {'Key': 'sce:app:environment', 'Value': environment},
                        {'Key': 'sce:service:name', 'Value': service_name }
                        ]
                #add_cloudwatch_alarm_tags(alarm_arn, tags_to_add, region)           
                tags_to_add.clear()
                print(f'Tags successfully added to cloudwatch alarm')

            elif alarm_name.startswith('qa'):
                print('1111111111111111111111111111111111111')

            tags = get_alarm_tags(alarm_arn, region)
            print(tags)
            if tags:
                print("Tags:")
                for tag in tags:                
                    print(f"{tag['Key']}: {tag['Value']}")                
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')


main()
