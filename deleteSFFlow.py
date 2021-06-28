import json
import boto3

import stsAssumeRole
session = boto3.session.Session()
client = session.client('appflow')

def lambda_handler(event, context):
    response = client.delete_flow(flowName='Salesforce2s3',forceDelete=False)
    return {
        'Flow ARN': response,
         }