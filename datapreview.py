# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:29:32 2023

@author: abdera
"""

"""
Ref:  https://docs.informatica.com/cloud-common-services/administrator/current-version/rest-api-reference/data-integration-rest-api/datapreview.html
Ref2: https://docs.informatica.com/integration-cloud/b2b-gateway/current-version/rest-api-reference/platform-rest-api-version-2-resources/auditlog.html

Postman Reference: https://martian-meteor-681122.postman.co/workspace/New-Team-Workspace~5ca85789-8e10-466e-ba03-442b2dbdcc00/request/28403454-b112a4cb-d841-48ad-a3de-193e15ab9733?ctx=code
"""
######################################### Log in 
import requests
import json

url = "https://dm-na.informaticacloud.com/identity-service/api/v1/Login"

payload = json.dumps({
  "username": username,
  "password": password
})
headers = {
  'content-type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic Og=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

#print(response.text)
User_Profile_df = json.loads(response.text)

import pandas as pd
df = pd.json_normalize(User_Profile_df)
sessionId = df['sessionId'].iloc[0]


############################################################################################################# 

#                                       Search/Query
 
##############################################################################################################



############# connections/ Connectors


import requests
import json

url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/connection"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': sessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

df = json.loads(response.text)

import pandas as pd
connection = pd.json_normalize(df)




################ connections (sources & targets)



import requests
import json

### get source connectionid

urls = "https://nac1.dm-na.informaticacloud.com/saas/api/v2/connection/source/" + connection.id

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': sessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


url_list = urls.tolist()

results = []

for url in urls:
    response = requests.request("GET", url, headers=headers,timeout=None, verify=False)# only 200
    df = json.loads(response.text)
    test = pd.json_normalize(json.loads(response.text))
    if test.empty != True:
        results.append(test)
    else:
        pass
    
sources = pd.concat(results, axis=0, ignore_index=True)


################ datapreview - if permitted 

#DeltaConnectionID = '010Sxxxxxxxxxxxxxxx00008'# DEV - DataBricks Delta -  
#DeltaConnectionID = '010Sxxxxxxxxxxxxxxx0000D'# DEV - DataBricks Delta - 

import requests
import json

### get source data 

url = "https://{region}.dm-na.informaticacloud.com/saas/api/v2/connection/source/{sourceID}/datapreview/{file/source}.csv"

#parameters can be used with activitylog: "entry id, task id, run id, offset, rowlimit
#maximum number to return is 1000

payload = {}
headers = {
  'icSessionId': sessionId,### changes based on First Step Runs -- every 30 min
  'Content-Type': 'application/json'}


response = requests.request("GET", url, headers=headers, verify=False)

print(response.text)























