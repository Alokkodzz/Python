import requests
import webbrowser
import msal
import json

# Define your Azure AD app credentials and tenant details
client_id = '4c7a7472-b4bc-4e74-bff4-cab2a7588460'  # Replace with your Azure AD application client ID
tenant_id = '699dd9b2-11db-4f3b-8979-518807fc5fb9'  # Replace with your Azure AD tenant ID
client_secret = '54I8Q~7BF_Uo44ZygfpHDF2S20M3XT1EW~_D_cxf'  # Replace with your Azure AD application client secret
scope = ['https://graph.microsoft.com/.default']  # Scope for Microsoft Graph API

# Function to get the access token using MSAL (using App-only authentication)
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

# Function to read data from a specific range in an Excel sheet
def read_excel_range(file_id, sheet_name, range_address, access_token, drive_id):
    
    url = f'https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/workbook/worksheets/{sheet_name}/range(address=\'{range_address}\')'



    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['values']
    else:
        raise Exception(f"Error reading range: {response.text}")

# Main function to interact with Excel using Microsoft Graph
def main():
    # Get access token
    access_token = get_access_token(client_id, tenant_id, client_secret)

    # Example: Read data from a specific range (e.g., 'Sheet1!A1:B5')
    drive_id = 'b!yTwCsJCKvUSp5S632YrIfUdUrZniEtZDlUcmynlmtiK9zzTP13o-Q7RK6Fg6xrpn'
    #file_id = 'F26557A90A973414!1029'
    file_id = '024E16A9-2D2C-4729-B393-B5EBA1DE6AB4'  # Replace with the ID of your Excel file in OneDrive or SharePoint
    sheet_name = 'Sheet1'
    range_address = 'A1:A10'
    range_data = read_excel_range(file_id, sheet_name, range_address, access_token, drive_id)
    print(range_data)

if __name__ == "__main__":
    main()