# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 15:42:29 2023

@author: abdera
"""


"""
Created on Fri Sep 29 13:31:25 2023

@author: abdera

Ref:  https://www.youtube.com/watch?v=J0BMM-B3WW4&t=256s
Ref2: https://docs.informatica.com/integration-cloud/b2b-gateway/current-version/rest-api-reference/platform-rest-api-version-2-resources/auditlog.html

Postman Reference: https://martian-meteor-681122.postman.co/workspace/New-Team-Workspace~5ca85789-8e10-466e-ba03-442b2dbdcc00/request/28403454-b112a4cb-d841-48ad-a3de-193e15ab9733?ctx=code
"""
######################################### Log in 
import requests
import json

url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": "xxxxxxxx",
  "password": "xxxxxxxx"
})
headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic Og=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

#print(response.text)
User_Profile_df = json.loads(response.text)

###################################### auditlog

import requests
import json

url = "https://nac1.dm-na.informaticacloud.com/saas/api/v2/auditlog?batchId=0&batchSize=1000"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': 'xxxxxxxxxxxxxxx',### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


auditlog_Sample = json.loads(response.text)


jsonString = json.dumps(auditlog_Sample)
with open('C:/Users/......................./Informatica API/auditlog_sample', 'w') as f:
    json.dump(jsonString, f)

###################################### runtime

import requests
import json

url = "https://nac1.dm-na.informaticacloud.com/saas/api/v2/runtimeEnvironment"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': 'xxxxxxxxxxxxxxxxxx',### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


runtime_Sample = json.loads(response.text)


jsonString = json.dumps(auditlog_Sample)
with open('C:/Users/................................/Informatica API/runtime_Sample', 'w') as f:
    json.dump(jsonString, f)


