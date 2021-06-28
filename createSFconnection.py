import json
import os
import boto3
import requests
session = boto3.session.Session()
client = session.client('appflow')
def lambda_handler(event, context):
	accessToken = token_gen()
	print(accessToken)
	response = client.create_connector_profile(connectorProfileName='SF_API_Connection',connectorType='Salesforce',connectionMode='Public',connectorProfileConfig={'connectorProfileProperties': {'Salesforce': {'instanceUrl': os.environ['instanceUrl'],'isSandboxEnvironment': False}},'connectorProfileCredentials': {'Salesforce': {'accessToken': accessToken,'refreshToken': 'DummyrefreshToken'}}})
	return {'response': response}
def token_gen():
	clientId = os.environ['client_Id']
	clientSecret = os.environ['client_Secret']
	clientUserName = os.environ['client_UserName']
	ClientPassword = os.environ['Client_Password']
	ClientToken = os.environ['Client_Token']
	access_token_url = 'https://login.salesforce.com/services/oauth2/token'
	dataAT = {'grant_type': 'password','client_id' : clientId,'client_secret' : clientSecret,'username': clientUserName,'password': ClientPassword+ClientToken}
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	reqAT = requests.post(access_token_url, data=dataAT, headers=headers)
	responseAT = reqAT.json()
	accessToken = responseAT['access_token']
	return accessToken