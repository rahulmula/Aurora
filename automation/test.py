import boto3

region = 'ap-east-1'
cw_tags_lst = []

def get_cloudwatch_alarms(region):
    try:
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        response = cloudwatch.describe_alarms()
        alarms = response['MetricAlarms']
        return alarms
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')

def get_alarm_tags(alarm_name, region):
    try:
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        response = cloudwatch.list_tags_for_resource(ResourceARN=alarm_name)
        tags = response['Tags']
        return tags
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')

def get_eb_environment_details(environment_id, region):
    try:
        eb = boto3.client('elasticbeanstalk', region_name=region)
        response = eb.describe_environments(EnvironmentIds=[environment_id])
        return response
    except Exception as error:
        print(f'Exception in get_eb_environment_details() {str(error)}')

def get_eb_environment_tags(environment_id, region):
    try:
        eb = boto3.client('elasticbeanstalk', region_name=region)
        response = eb.describe_environments(EnvironmentIds=[environment_id])
        environment_arn = response['Environments'][0]['EnvironmentArn']
        response = eb.list_tags_for_resource(ResourceArn=environment_arn)
        tags = response.get('ResourceTags', [])
        return tags
    except Exception as error:
        print(f'Exception in get_eb_environment_tags() {str(error)}')

def add_cloudwatch_alarm_tags(alarm_arn, tags, region):
    try:
        cloudwatch = boto3.client('cloudwatch', region_name=region)
        cloudwatch.tag_resource(ResourceARN=alarm_arn, Tags=tags)
    except Exception as error:
        print(f'Exception in add_cloudwatch_alarm_tags() {str(error)}')

def main():
    try:
        alarms = get_cloudwatch_alarms(region)
        count = 0
        for alarm in alarms:
            alarm_arn = alarm['AlarmArn']
            #print(f'Alarm Name: {alarm_name}')
            #if alarm_name == 'arn:aws:cloudwatch:eu-west-3:933919336272:alarm:TargetTracking-table/Configuration-ProvisionedCapacityHigh-145db75a-7896-4beb-a629-2306c09df5d9':
                #print('111')
                #tags = get_alarm_tags(alarm_name, region)
                #print(tags)
            print(alarm_arn)
            alarm_name = alarm_arn.split(':')[-1]
            print(alarm_name)
            if len(alarm_name.split('-')) == 6 and count < 1:
                count += 1
                alarmStr = alarm_name.split('-')[2]
                print(alarmStr)
                environment_id = 'e-' + alarmStr
                print(environment_id)
                print(get_eb_environment_tags(environment_id, region))
                environment_tags = get_eb_environment_tags(environment_id, region)
                for tag in environment_tags:
                    print(f"{tag['Key']}: {tag['Value']}")
                    if 'sce:app:name:' in tag['Key']:
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
                add_cloudwatch_alarm_tags(alarm_arn, cw_tags_lst, region)
                cw_tags_lst.clear()
                print('Success!!!')
                print(f'count: {count}')
            tags = get_alarm_tags(alarm_arn, region)
            print(tags)
            if tags:
                print("Tags:")
                for tag in tags:
                    print(f"{tag['Key']}: {tag['Value']}")

                    #if tag['key'] == 'sce:app:name':

                #if 'sce:app:name' in tags:
                    #print('sce tags already exist')
                    #count += 1

                #else:
                    #print('sce tags does not exist')
                #break
                    #for tag in tags:
                        #print(f'{tag['Key']}: {tag['Value']}')
                        #if ''
            #else:
                #print("No tags found for this alarm")

        print(count)
    except Exception as error:
        print(f'Exception in get_cloudwatch_alarms() {str(error)}')

main()
