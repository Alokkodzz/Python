from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import configparser
import boto3
from botocore.exceptions import ClientError
import pytz
from log_utils import setup_logging, write_log, archive_log
import requests
import msal
import json

config = configparser.ConfigParser()
config.read("Config.ini")

utc_now = datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_now = utc_now.astimezone(ist_timezone)

datestamp = ist_now.strftime("%d-%m-%Y")
timestamp = ist_now.strftime("%Y-%m-%d_%H-%M-%S")
current_time = ist_now.strftime("%H")


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = "keys.json"
SPREADSHEET_ID = config.get("Sheet", "SPREADSHEET_ID")


ses_client = boto3.client('ses', region_name='us-east-1')
sender = "prabhakaranpv6@gmail.com"
recipient = "alok63579@gmail.com"
subjects = "Shift Report : {datestamp}"
subject = subjects.format(datestamp=datestamp)
date = "{datestamp}"
DATE = date.format(datestamp=datestamp)
Head = config.get("Sheet", "head")
current_date = datetime.now()

AU = config.get("shift", "AU")
EU = config.get("shift", "EU")
NA = config.get("shift", "NA")

#Graph API
client_id = '4c7a7472-b4bc-4e74-bff4-cab2a7588460'  #Azure AD application client ID
tenant_id = '699dd9b2-11db-4f3b-8979-518807fc5fb9'  #Azure AD tenant ID
client_secret = '54I8Q~7BF_Uo44ZygfpHDF2S20M3XT1EW~_D_cxf'  #Azure AD application client secret
scope = ['https://graph.microsoft.com/.default']  #Scope for Microsoft Graph API


setup_logging()

def shift():
  if current_time == AU:
    write_log("Starting AU shift report tool")
    RANGE_NAME = config.get("Sheet", "RANGE_NAME_AU")
    sft = "Shift Report : AU Shift"
    sheet_name = DATE
    range_address = RANGE_NAME
    Execute_ShiftReport(sheet_name, sft,range_address)
  elif current_time == EU:
    write_log("Starting EU shift report tool")
    RANGE_NAME = config.get("Sheet", "RANGE_NAME_EU")
    sft = "Shift Report : EU Shift"
    sheet_name = DATE
    range_address = RANGE_NAME
    Execute_ShiftReport(sheet_name, sft,range_address)
  elif current_time == NA:
    write_log("Starting NA shift report tool")
    RANGE_NAME = config.get("Sheet", "RANGE_NAME_NA")
    sft = "Shift Report : NA Shift"
    sheet_name = DATE
    range_address = RANGE_NAME
    Execute_ShiftReport(sheet_name, sft,range_address)

def deployment_p(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("WRC_P", "")
        #formatted = f"<br> {j}. " + ' '.join(line)
        formatted = f"<br> {j} . " + line
        matching_rows.append(formatted)
        j += 1
      #print(row)
    write_log("data fetched for deployment production")
    return ''.join(matching_rows)
    
    #print(values)

#deployments_p = deployment_p(values, "WRC_P")
#print(deployments_p)

def deployment_s(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("WRC_S", "")
        formatted = f"<br> {j} . " + line 
        matching_rows.append(formatted)
        j += 1 
    write_log("data fetched for deployment staging")
    return ''.join(matching_rows)

#deployments_s = deployment_s(values, "WRC_S")

def CP_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("CP_P", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1 
    write_log("data fetched for Cloud portal tasks")
    return ''.join(matching_rows)

#CP_P = CP_P(values, "CP_P")

def SM_S(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("SM_S", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1 
    write_log("data fetched for saas memo staging")
    return ''.join(matching_rows)

#SM_S = SM_S(values, "SM_S")

def SM_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("SM_P", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1 
    write_log("data fetched for saas memo production")
    return ''.join(matching_rows)

#SM_P = SM_P(values, "SM_P")


def SF_S(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("SF_S", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1 
    write_log("data fetched for sales force staging")
    return ''.join(matching_rows)

#SF_S = SF_S(values, "SF_S")

def SF_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("SF_P", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1
    write_log("data fetched for sales force production")
    return ''.join(matching_rows)

#SF_P = SF_P(values, "SF_P")


def OTHER_S(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("OTHER_S", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1
    write_log("data fetched for other updates on staging")
    return ''.join(matching_rows)

#OTHER_S = OTHER_S(values, "OTHER_S")

def OTHER_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("OTHER_P", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1
    write_log("data fetched for other updates on production")
    return ''.join(matching_rows)

#OTHER_P = OTHER_P(values, "OTHER_P")


def SEV_1(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("SEV_1", "")
        formatted = f"<br> {j} . " + line  
        matching_rows.append(formatted)
        j += 1
    write_log("data fetched for SEV 1 incident for today")
    return ''.join(matching_rows)

#SEV_1 = SEV_1(values, "SEV_1")

def CP_REPORT(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("CP_REPORT", "")
        #formatted = f"<br> {j} . " + line  
        matching_rows.append(line)
        j += 1
    write_log("data fetched for Daily cloud service report")
    return ''.join(matching_rows)

#CP_REPORT = CP_REPORT(values, "CP_REPORT")

def BASTION_S(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("BASTION_S", "")
        #formatted = f"<br> {j} . " + line  
        matching_rows.append(line)
        j += 1
    write_log("data fetched for Bastion rotation on staging")
    return ''.join(matching_rows)

#BASTION_S = BASTION_S(values, "BASTION_S")

def BASTION_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("BASTION_P", "")
        #formatted = f"<br> {j} . " + line  
        matching_rows.append(line)
        j += 1
    write_log("data fetched for Bastion rotation on staging")
    return ''.join(matching_rows)

#BASTION_S = BASTION_P(values, "BASTION_P")


def REDIS_S(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("REDIS_S", "")
        #formatted = f"<br> {j} . " + line  
        matching_rows.append(line)
        j += 1
    write_log("data fetched for redis memory on staging")
    return ''.join(matching_rows)

#REDIS_S = REDIS_S(values, "REDIS_S")

def REDIS_P(values, keyword):
    matching_rows = []
    j = 1
    for row in values:
      if keyword.upper() in row[0].upper():
        line = row[0].replace("REDIS_P", "")
        #formatted = f"<br> {j} . " + line  
        matching_rows.append(line)
        j += 1
    write_log("data fetched for redis memory on production")
    return ''.join(matching_rows)

#REDIS_P = REDIS_P(values, "REDIS_P")


def Execute_ShiftReport(sheet_name, sft,range_address): 
  
  write_log("Execute_ShiftReport function triggered")
  access_token = get_access_token(client_id, tenant_id, client_secret)

  drive_id = 'b!yTwCsJCKvUSp5S632YrIfUdUrZniEtZDlUcmynlmtiK9zzTP13o-Q7RK6Fg6xrpn'
  file_id = '024E16A9-2D2C-4729-B393-B5EBA1DE6AB4'
  read_excel_send_email(file_id, sheet_name, range_address, access_token, drive_id, sft)

  
def get_access_token(client_id, tenant_id, client_secret):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )
    
    # Get token from Microsoft Identity platform
    token_response = app.acquire_token_for_client(scopes=scope)
    
    if 'access_token' in token_response:
        return token_response['access_token']
    else:
        raise Exception("Error getting access token: " + json.dumps(token_response, indent=4))

def read_excel_send_email(file_id, sheet_name, range_address, access_token, drive_id, sft):
    write_log("read_excel_send_email function executing")
    
    url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/workbook/worksheets/{sheet_name}/range(address=\'{range_address}\')'

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        values =  data['values']
        write_log("Successfully connected to graph API")
    
        deployment_p_val = deployment_p(values, "WRC_P")
        deployment_s_val = deployment_s(values, "WRC_S")
        CP_P_val = CP_P(values, "CP_P")
        SM_S_val = SM_S(values, "SM_S")
        SM_P_val = SM_P(values, "SM_P")
        SF_S_val = SF_S(values, "SF_S")
        SF_P_val = SF_P(values, "SF_P")
        OTHER_S_val = OTHER_S(values, "OTHER_S")
        OTHER_P_val = OTHER_P(values, "OTHER_P")
        SEV_1_val = SEV_1(values, "SEV_1")
        CP_REPORT_val = CP_REPORT(values, "CP_REPORT")
        BASTION_S_val = BASTION_S(values, "BASTION_S")
        BASTION_P_val = BASTION_P(values, "BASTION_P")
        REDIS_S_val = REDIS_S(values, "REDIS_S")
        REDIS_P_val = REDIS_P(values, "REDIS_P")
        
        with open('SR1.html', 'r') as file:
            html_body = file.read()
          
        html_body = html_body.format(
            Head=Head,
            DATE=DATE,
            sft=sft,
            CP_P_val=CP_P_val,
            deployment_s_val=deployment_s_val,
            deployment_p_val=deployment_p_val,
            SM_S_val=SM_S_val,
            SM_P_val=SM_P_val,
            SF_S_val=SF_S_val,
            SF_P_val=SF_P_val,
            OTHER_S_val=OTHER_S_val,
            OTHER_P_val=OTHER_P_val,
            SEV_1_val=SEV_1_val,
            BASTION_S_val=BASTION_S_val,
            BASTION_P_val=BASTION_P_val,
            CP_REPORT_val=CP_REPORT_val,
            REDIS_S_val=REDIS_S_val,
            REDIS_P_val=REDIS_P_val,
        )
        
        
        body = {
              'Html': {
                  'Data': html_body
              }
          }
        
        try:
          response = ses_client.send_email(
              Source=sender,
              Destination={
                  'ToAddresses': [recipient],
              },
              Message={
                  'Subject': {
                      'Data': subject
                  },
                  'Body': body
              }
          )
          
          write_log(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
              write_log(f"Error sending email: {e.response['Error']['Message']}")
        archive_log()


if __name__ == "__main__":
  shift()