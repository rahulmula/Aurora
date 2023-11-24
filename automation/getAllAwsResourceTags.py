import boto3
import openpyxl


region = 'us-east-2'

def get_all_tags():
    tags_data = []

    resource_types = ['ec2', 's3', 'rds', 'lambda', 'eb', 'ecs']
    client = boto3.client('resourcegroupstaggingapi', region_name=region)

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    sheet.append(['Resource Type', 'Resource ID', 'Tag Key', 'Tag Value'])

    for resource_type in resource_types:
        resources = client.list_resources(ResourceTypeFilters=[resource_type])

        for resource in resources.get('ResourceTagMappingList', []):
            resource_arn = resource['ResourceARN']

            tags = client.list_tags_for_resource(ResourceARN=resource_arn).get('Tags', [])

            for tag in tags:
                sheet.append([resource_type, resource_id, tag['Key'], tag['Value']])
    workbook.save('all_tags_output.xlsx')


def main():
    try:

        get_all_tags()

    except Exception as error:
        print(f'exception in main() {str(error)}')

if __name__ == "__main__":
    main()
