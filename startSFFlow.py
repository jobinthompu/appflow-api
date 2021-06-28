import json
import boto3
import stsAssumeRole
session = boto3.session.Session()
client = session.client('appflow')

def lambda_handler(event, context):
    response = client.start_flow(flowName='Salesforce2s3')
    return {
        'Flow ARN': response['flowArn'],
        "Flow Status": response['flowStatus']
         }