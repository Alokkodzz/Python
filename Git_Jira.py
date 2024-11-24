import requests
import json
from requests.auth import HTTPBasicAuth
from flask import Flask
app = Flask(__name__)

@app.route('/createjira', methods=['POST', 'GET'])

def get_comment():

    urls = "https://api.github.com/repos/Alokkodzz/Myrepo/issues/comments"

    token = ""
        
    result = requests.get(urls, headers={'Authorization': 'token {}'.format(token), 'Accept' : 'application/vnd.github.raw+json'})

    output = result.json()

    url = "https://alok63579.atlassian.net/rest/api/3/issue"

    API_TOKEN = ""

    auth = HTTPBasicAuth("alok63579@gmail.com", API_TOKEN)

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    
    payload = json.dumps( {
    "fields": {
        "description": {
        "content": [
            {
            "content": [
                {
                "text": "My first jira ticket",
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
        "key": "AK"
        },
        "issuetype": {
        "id": "10014"
        },
        "summary": "New JIRA Ticket",
    },
    "update": {}
    } )

    
    #a = len(output)
    #b = int(len(output)-1)
   # c = int(len(output)-2)
    #for i in range(0, len(output)):
        #print(i)
        #if i == (len(output)-1):
    i = len(output)-1
    outputs = output[i]
    #print(b)
    v = outputs['body']
    arg = "/createJira"
    #print(i)
    #print(v)
    #return outputs
    if arg == v:
        #print(v)
        responses = requests.request("POST", url, data=payload, headers=headers, auth=auth)
        return json.dumps(json.loads(responses.text), sort_keys=True, indent=4, separators=(",", ": "))
    else:
        return json.dumps(json.loads(responses.text), sort_keys=True, indent=4, separators=(",", ": "))
        #print(i)

if __name__ == '__main__':
    get_comment()
    app.run(host='0.0.0.0', port=5000)