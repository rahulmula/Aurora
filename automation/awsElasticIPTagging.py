import boto3

region = 'us-east-2'



def get_elastic_ips():
    try:

        # Create an Elastic IP client
        ec2 = boto3.client('ec2', region_name=region)

        # Describe the Elastic IP addresses
        elastic_ips = ec2.describe_addresses()['Addresses']

        return elastic_ips
    
    except Exception as error:
        print(f'Exception in get_elastic_ips() {str(error)}')


def get_elastic_ip_tags(allocation_id):
    try:
        # Create an Elastic IP client
        ec2 = boto3.client('ec2', region_name=region)

        tags = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [allocation_id]}])['Tags']
        
        return tags
        
    except Exception as error:
        print(f'Exception in get_elastic_ip_tags() {str(error)}')


def set_region(region):
    if region == 'us-east-2':
        return "na"
    elif region == 'ap-east-1':
        return "asia"
    elif region == 'eu-west-3':
        return "emea"


def main():
    try:
        tags = []
        cw_tags_lst = []

        elastic_ips = get_elastic_ips()

        # Loop through each Elastic IP and print its tags
        for elastic_ip in elastic_ips:
            allocation_id = elastic_ip['AllocationId']        
            
            tags = get_elastic_ip_tags(allocation_id)

            #print(tags)
            
            #if 'sce:service:name' in tags:
                #print('tags exists')
            #else:
                #print('tags not exists')
            
            key_found = False

            # Check if key exists in any dictionary in the list
            for tag in tags:
                print(f"{tag['Key']}: {tag['Value']}")
                if 'Application' in tag['Key']:                    
                    new_tag = {'Key': 'sce:app:name', 'Value' : tag['Value'].lower()}
                    cw_tags_lst.append(new_tag)
                elif 'Environment' in tag['Key']:                
                    new_tag = {'Key': 'sce:app:environment', 'Value' : tag['Value'].lower()}
                    cw_tags_lst.append(new_tag)
                    #region = set_region(region)
                    new_tag = {'Key': 'sce:app:region', 'Value' : set_region(region)}
                    cw_tags_lst.append(new_tag)
                elif 'Name' in tag['Key']:
                    service_name = "eip-" + tag['Value']
                    new_tag = {'Key': 'sce:service:name', 'Value' : service_name}
                    cw_tags_lst.append(new_tag)
                elif 'CostCenter' in tag['Key']:
                    costcenter = tag['Value']
                    new_tag = {'Key': 'sce:app:costcenter', 'Value' : costcenter}
                    cw_tags_lst.append(new_tag)                    
                    

                if 'sce:service:name' in tag['Key']:
                    print('tag exists')
                    key_found = True
                    break
                else:
                    new_tag = {'Key': 'sce:app:name', 'Value' : tag['Value']}
                #print(f"{tag['Key']}: {tag['Value']}")
            if not key_found:
                print('tag not exists')


    except Exception as error:
        print(f'Exception in main() {str(error)}')

main()

