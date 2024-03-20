# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:31:25 2023

@author: abdera

Ref:  https://www.youtube.com/watch?v=J0BMM-B3WW4&t=256s
Ref2: https://docs.informatica.com/integration-cloud/b2b-gateway/current-version/rest-api-reference/platform-rest-api-version-2-resources/activitylog.html

"""

######################################### Log in 
import requests
import json

url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": "xxxxxxxx",
  "password": "xxxxx"
})
headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic Og=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

#print(response.text)
User_Profile_df = json.loads(response.text)

icSessionId = User_Profile_df['sessionId']

###################################### Activitylog V2

import requests
import json
import pandas as pd

url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/activity/activityLog"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000
#can also be applied to sessionlog and errorlog

payload = {}
headers = {
  'icSessionId': icSessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


ActivityLogs_Sample = json.loads(response.text)
ActivityLogs_Sample_df = pd.json_normalize(ActivityLogs_Sample)

runId = ActivityLogs_Sample_df['runId']



###################################### Activitylog Query
"""
import requests
import json

url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/activity/activityLog?startTime=" + "2023-09-28T16:30:25.000Z"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000
#can also be applied to sessionlog and errorlog: /api/v2/activity/activityLog/<id>/sessionLog

payload = {}
headers = {
  'icSessionId': icSessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


ActivityLogs_Sample = json.loads(response.text)


jsonString = json.dumps(ActivityLogs_Sample)
with open('C:/Users/......./ActivityLogs_Sample', 'w') as f:
    json.dump(jsonString, f)



"""



################################ Sessions Log

import requests
import json

url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/activity/activityLog/{log#}"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000
#can also be applied to sessionlog and errorlog: /api/v2/activity/activityLog/<id>/sessionLog

payload = {}
headers = {
  'icSessionId': icSessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


ActivityLogs_session = json.loads(response.text)










