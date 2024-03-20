

"""
Created on Fri Sep 29 13:31:25 2023

@author: abdera

Ref:  https://www.youtube.com/watch?v=J0BMM-B3WW4&t=256s
Ref2: https://docs.informatica.com/integration-cloud/b2b-gateway/current-version/rest-api-reference/platform-rest-api-version-3-resources.html

"""
######################################### Log in 
import requests
import json

url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": "xxxxxxxxxxxx",
  "password": "xxxxxxxxxxxx"
})
headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic Og=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

#print(response.text)
User_Profile_df = json.loads(response.text)

###################################### securityLog            ### V# ### baseAPIURL

import requests
import json

url = "https://{region}.dm-na.informaticacloud.com/saas/public/core/v3/securityLog"

#For Data Integration, use one of the following codes: v2/task?type=MTT
# DMASK. Masking task.
# DRS. Replication task.
# DSS. Synchronization task.
# MTT. Mapping task.
# PCS. PowerCenter task.

payload = {}
headers = {
  'INFA-SESSION-ID': 'xxxxxxxxxx',### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)


securityLog = json.loads(response.text)


jsonString = json.dumps(securityLog)
with open('C:/Users/................./securityLog', 'w') as f:
    json.dump(jsonString, f)



