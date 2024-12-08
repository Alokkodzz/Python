from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from requests.auth import HTTPBasicAuth
import json
import configparser
from google.auth.exceptions import RefreshError
from flask import Flask, request

config = configparser.ConfigParser()
config.read("config.ini")

#Constant values from config for google API

#SCOPES = config.get("Google", "SCOPES")
SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']
#SERVICE_ACCOUNT_FILE = config.get("Google", "SERVICE_ACCOUNT_FILE")
DISCOVERY_DOC = config.get("Google", "DISCOVERY_DOC")
form_id = config.get("Google", "form_id")

#Constant values from config for Jira

url = config.get("Jira", "url")
API_TOKEN = config.get("Jira", "API_TOKEN")
key = config.get("Jira", "Project_key")
id = config.get("Jira", "issuetypes_id")

#API
auth = HTTPBasicAuth("alok63579@gmail.com", API_TOKEN)
creds = Credentials.from_service_account_file("keys.json", scopes=SCOPES)


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])

def Details_from_form():

    

    service = build("forms", "v1", discoveryServiceUrl=DISCOVERY_DOC, credentials=creds,)

    try:
        result = service.forms().responses().list(formId=form_id).execute()
        responses = result["responses"]
        #i = len(responses)
        team = responses[0]["answers"]
        answers = team['72c5e3ca']
        textAnswers = answers['textAnswers']
        a = textAnswers["answers"]
        dept = a[0]["value"]

        answers1 = team['78b83cc2']
        textAnswers1 = answers1['textAnswers']
        a1 = textAnswers1["answers"]
        descri = a1[0]["value"]

        answers2 = team['08d90e4b']
        textAnswers2 = answers2['textAnswers']
        a2 = textAnswers2["answers"]
        title = a2[0]["value"]
    except RefreshError as e:
        print(f"Error details: {e}")
    createjira(title, descri, dept)

def createjira(title, descri, dept):

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    Summary = f"Department : {dept} \n{descri}"
    payload = json.dumps( {
    "fields": {
        "description": {
        "content": [
            {
            "content": [
                {
                "text": Summary,
                "type": "text"
                }
            ],
            "type": "paragraph"
            }
        ],
        "type": "doc",
        "version": 1
        },
        "project": {
        "key": key
        },
        "issuetype": {
        "id": id
        },
        "summary": title,
    },
    "update": {}
    } )

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    #data = response['comment']
    return payload


if __name__ == '__main__':
    Details_from_form()
    app.run(host='0.0.0.0', port=5000)