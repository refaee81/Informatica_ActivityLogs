
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 11:41:05 2023

@author: abdera

"""

import requests
import json
import pandas as pd


######################################### Log in 

url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": "xxxxxxxxx",
  "password": "xxxxxxxxE"
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

runId = str(ActivityLogs_Sample_df['runId'])



###################################### runId V2


url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/activity/activityLog?runId=1149"
payload = {}
headers = {
  'icSessionId': icSessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)
runId_Sample = json.loads(response.text)

###################################### runId Loop

runId_list = pd.DataFrame(range(10000))
runId_list[0] = runId_list[0].astype(str)



url_list = "https://nac1.dm-na.informaticacloud.com/saas/api/v2/activity/activityLog?runId="+runId_list[0]

results = []

for url in url_list:
    headers = {
      'icSessionId': icSessionId,### changes based on First Step Runs -- every 30 min
      'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers, verify=False)# only 200
    df = json.loads(response.text)
    test = pd.json_normalize(json.loads(response.text))
    if test.empty != True:
        results.append(test)
    else:
        pass


DEV_RunId_Logs = pd.concat(results)

writer = pd.ExcelWriter(r'C:\Users\abdera\Documents\EDC\MDM\Python API\Informatica API\runIds Log\DEV_RunId_Logs.xlsx', engine='xlsxwriter')
DEV_RunId_Logs.to_excel(writer, sheet_name='DEV_RunId_Logs', index=False)
writer.close() 


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









