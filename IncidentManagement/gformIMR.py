from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from requests.auth import HTTPBasicAuth
import json
import configparser
from google.auth.exceptions import RefreshError
from flask import Flask, request, jsonify

#To read config
config = configparser.ConfigParser()
config.read("Config.ini")

# Constants for Google API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = "keys.json"
SPREADSHEET_ID = config.get("Sheet", "SPREADSHEET_ID")
RANGE_NAME = config.get("Sheet", "RANGE_NAME")

# Authenticate for Google Sheets API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

#Constant values from config for Jira

url = config.get("Jira", "url")
API_TOKEN = config.get("Jira", "API_TOKEN")
key = config.get("Jira", "Project_key")
id = config.get("Jira", "issuetypes_id")

#Authenticate for Jira API
auth = HTTPBasicAuth("alok63579@gmail.com", API_TOKEN)


app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])

def Details_from_sheet():

        with app.app_context():
            try:
                service = build('sheets', 'v4', credentials=creds)
                sheet = service.spreadsheets()
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
                values = result.get('values', [])

                if not values:
                    print('No data found.')
                    return None
                last_response = values[-1]
                
                team = last_response[1]
                title = last_response[2]
                description = last_response[3]

                createjira(title, description, team)

                return jsonify({
                    'Team': team,
                    'Title': title,
                    'Description': description
                }), 200

            except Exception as e:
                print(f"An error occurred: {e}")
                return None
    
            

def createjira(title, description, team):

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    Summary = f"Department : {team} \n{description}"
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
    print(payload)


if __name__ == '__main__':
    with app.app_context():
        Details_from_sheet()
    app.run(host='0.0.0.0', port=5000)