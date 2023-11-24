import sys
def handler(event, context):
        return 'Running Bash In Docker AWS Lambda' + sys.version + '!'