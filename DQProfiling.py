# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:20:30 2023

@author: abdera
"""

#ref: https://docs.informatica.com/data-governance-and-quality-cloud/cloud-data-profiling/h2l/_getting-started-with-cloud-data-profiling-rest-api_cloud-data-profiling_h2l_ditamap/getting_started_with_cloud_data_profiling_rest_api/profiling-tutorial/prerequisites.html
#ref: https://github.com/vks9907/CDQ_Custom_Dashboard/blob/main/IICS_CDQ_Dashboard_Dataset.py


############################################################################################################# 

#                       # Function to get list of profiles with metadata information - START

 
##############################################################################################################

import requests
import json
import pandas as pd

POD_region = "na"
username = "xxxxxxxxx"
password = "xxxxx"

# Function to return session ID and Generate Profiling URLs
def get_session_id():
    login_api_url = "https://dm-" + POD_region + ".informaticacloud.com/ma/api/v2/user/login"
    credentials = {
        "username": username,
        "password": password
    }
    login_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    login_response = requests.request("POST", login_api_url, json=credentials, headers=login_headers, verify=False)
    print('Login API executed - ' + login_api_url)
    serverUrl = login_response.json()['serverUrl']
    get_session_id.profile_api_url = serverUrl.split('.')[0] + "-dqprofile.dm-" + POD_region + ".informaticacloud.com/profiling-service/api/v1/profile"
    get_session_id.profile_column_api_url = serverUrl.split('.')[0] + "-dqprofile.dm-" + POD_region + ".informaticacloud.com/metric-store/api/v1/odata/Profiles"
    get_session_id.frs_object_api_url = serverUrl.split('.')[0] + ".dm-" + POD_region + ".informaticacloud.com/frs/v1/Documents('"
    get_session_id.profile_execution_api_url = serverUrl.split('.')[0] + "-dqprofile.dm-" + POD_region + ".informaticacloud.com/profiling-service/api/v1/runDetail/"
    return login_response.json()['icSessionId']



# Get Session ID and Profiling URLs using above function
session_id = get_session_id()
profile_api_url = get_session_id.profile_api_url
profile_column_api_url = get_session_id.profile_column_api_url
frs_object_api_url = get_session_id.frs_object_api_url
profile_execution_api_url = get_session_id.profile_execution_api_url



###################################################################################################################################

#                                   1. Function to get list of profiles with metadata information 

####################################################################################################################################


def get_profile_list():
    profile_list_headers = {
        "Accept": "application/json",
        "IDS-SESSION-ID": session_id
    }
    profile_list_response = requests.request("GET", profile_api_url, headers=profile_list_headers, verify=False)
    print('API to get Profile list executed - ' + profile_api_url)
    return profile_list_response.json()


df = get_profile_list()
DQ_Profiles_Metadata = pd.json_normalize(df)


###################################################################################################################################

#                                   2. # get profile project and folder details

####################################################################################################################################


def get_frs_object_details(in_frs_id):
    url = frs_object_api_url + in_frs_id + "')?$expand=userInfo"
    headers = {
        "Accept": "application/json",
        "IDS-SESSION-ID": session_id
    }
    response = requests.request("GET", url, headers=headers, verify=False).json()
    print('API to get FRS object details executed - ' + url)
    array_dict = {
        "id": response["id"],
        "name": response["name"],
        "createdTime": response["createdTime"],
        "lastUpdatedTime": response["lastUpdatedTime"],
        "lastAccessedTime": response["lastAccessedTime"],
        "Object_Valid_Status": response["documentState"]
    }
    for loop_1 in response['parentInfo']:
        if loop_1['parentType'] == 'Project':
            array_dict.update({"Project_Name": loop_1['parentName']})
        elif loop_1['parentType'] == 'Folder':
            array_dict.update({"Folder_Name": loop_1['parentName']})
    try:
        for loop_2 in response['customAttributes']['stringAttrs']:
            if loop_2['name'] == 'DIMENSION':
                array_dict.update({"Rule_DIMENSION": loop_2['value']})
    except Exception as e:
        array_dict.update({"Rule_DIMENSION": ''})
    return array_dict



in_frs_id = DQ_Profiles_Metadata.frsId

results = []

for frsid in in_frs_id:
    x = get_frs_object_details(frsid)
    results.append(x)

DQ_Project_Folders = pd.json_normalize(results)



###################################################################################################################################

#                                   3. # fetch the profiles 

####################################################################################################################################


import requests
import json

urls = "https://nac1-dqprofile.dm-na.informaticacloud.com/profiling-service/api/v1/profile/" + DQ_Profiles_Metadata.id


headers = {
        "Accept": "application/json",
        "IDS-SESSION-ID": session_id
        }

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
    
DQ_profile_definitions = pd.concat(results, axis=0, ignore_index=True)

writer = pd.ExcelWriter('C:/Users/........................................................./DQ/profile_definitions_DEV.xlsx', engine='xlsxwriter')
DQ_profile_definitions.to_excel(writer, sheet_name='profile_definitions', index=False)
DQ_Project_Folders.to_excel(writer, sheet_name='DQ_Project_Folders', index=False)
DQ_Profiles_Metadata.to_excel(writer, sheet_name='DQ_Profiles_Metadata', index=False)
writer.save()














