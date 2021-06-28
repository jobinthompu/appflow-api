import json
import boto3
import time
import stsAssumeRole
session = boto3.session.Session()
client = session.client('appflow')

def lambda_handler(event, context):
    epoch_time = int(time.time()*1000)
    response = client.create_flow(
    flowName='Salesforce2s3',
    description='Pull Data From Salesforce to Amazon s3',
    triggerConfig={'triggerType': 'OnDemand'},
    sourceFlowConfig={
        'connectorType': 'Salesforce',
        'connectorProfileName': 'JobinSF',
        'sourceConnectorProperties': {'Salesforce': {'object': 'Contact'}}
    },
    destinationFlowConfigList=[
        {
            'connectorType': 'S3',
            'connectorProfileName': 'S3',
            'destinationConnectorProperties': {
                'S3': {
                    'bucketName': 'appflow-testy',
                    's3OutputFormatConfig': {'fileType':'JSON'}
                    }}}],
    tasks=[
        {
            'sourceFields': ['Id','Name','CreatedDate'],
            "taskProperties": {"DATA_TYPE":"string"},
            'destinationField': 'Id',
            'connectorOperator':{'Salesforce': 'PROJECTION'},
            'taskType': 'Filter',
        },
        {
            'sourceFields': ['CreatedDate'],
            'destinationField': 'CreatedDate',
            'connectorOperator':{'Salesforce': 'BETWEEN'},
            'taskType': 'Filter',
            "taskProperties": {"DATA_TYPE": "datetime","LOWER_BOUND": "0000000000000","UPPER_BOUND": str(epoch_time)}
        },{
            'sourceFields': ['Id'],
            'destinationField': 'Id',
            "taskProperties": {"DATA_TYPE":"string"},
            'taskType': 'Map'
        },{
            'sourceFields': ['Name'],
            'destinationField': 'Name',
            "taskProperties": {"DATA_TYPE":"string"},
            'taskType': 'Map'
        },{
            'sourceFields': ['CreatedDate'],
            'destinationField': 'CreatedDate',
            "taskProperties": {"DATA_TYPE":"datetime"},
            'taskType': 'Map'
        }
        
        ]
    )
    return {
        'Flow ARN': response['flowArn'],
        "Flow Status": response['flowStatus']
         }