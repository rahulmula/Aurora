import subprocess
import sys

def lambda_handler(event, context):
    try:
        print(f'function loaded')
        if len(sys.argv) < 2:
            errormessage = "Error: Missing argument. Provide the script name"
            print(errormessage)
            return {
                    'statusCode': 400,
                    'body': errormessage
                    }
            
        script_name = sys.argv[1]
        process = subprocess.Popen(['/bin/bash', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        returncode = process.returncode

        if returncode == 0:
            successmessage = "f'Script executed successfully. Output: '" + stdout.decode('utf-8')
            print(successmessage)
            return {
                'statusCode': 200,
                'body': successmessage
            }
        else:
            errormessage = "f'Script execution failed. Error:'," + stderr.decode('utf-8')
            print(errormessage)
            return {
                'statusCode': 500,
                'body': errormessage
            }
    except Exception as e:
        exceptionmessage = "f'An error occurred: {str(e)}, Exception: '," + stderr.decode('utf-8')
        print(exceptionmessage)
        return {
            'statusCode': 500,
            'body': exceptionmessage
        }
