import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope of the application
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its title (replace with your sheet title)
sheet = client.open("ShiftReport").sheet1

# Get all values from the sheet as a list of lists (rows)
data = sheet.get_all_values()

# Example: Structure of the HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shift Report: EU Shift</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }
    .container {
      width: 80%;
      margin: 20px auto;
      background-color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h1, h2 {
      text-align: center;
      color: #333;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 15px;
    }
    th, td {
      padding: 10px;
      border: 1px solid #ddd;
      text-align: left;
    }
    th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
    .task-section {
      margin-bottom: 20px;
    }
    .footer {
      text-align: center;
      font-size: 14px;
      color: #888;
      margin-top: 30px;
    }
  </style>
</head>
<body>

  <div class="container">
    <h1>Shift Report: EU Shift</h1>
    <p><strong>Date:</strong> 11/29/2024</p>

    <!-- Monitoring Section -->
    <div class="task-section">
      <h2 style="text-align: left;">Monitoring</h2>
      <table>
        <tr>
          <th>Task</th>
          <th>Staging</th>
          <th>Production</th>
        </tr>
        <tr>
          <td>{monitoring_task}</td>
          <td>{monitoring_staging}</td>
          <td>{monitoring_production}</td>
        </tr>
      </table>
    </div>

    <!-- Deployment Section -->
    <div class="task-section">
      <h2 style="text-align: left;">Deployment</h2>
      <table>
        <tr>
          <th>Task</th>
          <th>Staging</th>
          <th>Production</th>
        </tr>
        <tr>
          <td>{deployment_task}</td>
          <td>{deployment_staging}</td>
          <td>{deployment_production}</td>
        </tr>
      </table>
    </div>

    <!-- SaaS Memos Section -->
    <div class="task-section">
      <h2 style="text-align: left;">SaaS Memos</h2>
      <table>
        <tr>
          <th>Task</th>
          <th>Staging</th>
          <th>Production</th>
        </tr>
        <tr>
          <td>{saas_memo_task}</td>
          <td>{saas_memo_staging}</td>
          <td>{saas_memo_production}</td>
        </tr>
      </table>
    </div>

    <div class="footer">
      <p>End of Report</p>
    </div>
  </div>

</body>
</html>
"""

# Function to search for a specific keyword in the first column and return all matching rows
def get_rows_by_keyword(sheet_data, keyword):
    matching_rows = []
    for row in sheet_data:
        if keyword.lower() in row[0].lower():
            matching_rows.append(row)
    return matching_rows

# Function to format multiple data entries for HTML
def format_multiple_entries(entries):
    counter = 1
    formatted = f"<br> {counter}".join(entries)
    counter += 1
    return formatted

# Search for relevant rows based on keywords
monitoring_rows = get_rows_by_keyword(data, "Monitoring")
deployment_rows = get_rows_by_keyword(data, "Deployment")
saas_memo_rows = get_rows_by_keyword(data, "SaaS Memo")

# Extract the required information from the rows
# Monitoring Section
monitoring_task = "Not Found"
monitoring_staging = "Not Found"
monitoring_production = "Not Found"
if monitoring_rows:
    monitoring_task = monitoring_rows[0][1]  # Task from first matching row
    monitoring_staging = monitoring_rows[0][2]  # Staging from first matching row
    monitoring_production = format_multiple_entries([row[3] for row in monitoring_rows])  # Combine all production data

# Deployment Section
deployment_task = "Not Found"
deployment_staging = "Not Found"
deployment_production = "Not Found"
if deployment_rows:
    deployment_task = deployment_rows[0][1]
    deployment_staging = deployment_rows[0][2]
    deployment_production = format_multiple_entries([row[3] for row in deployment_rows])  # Combine all production data

# SaaS Memo Section
saas_memo_task = "Not Found"
saas_memo_staging = "Not Found"
saas_memo_production = "Not Found"
if saas_memo_rows:
    saas_memo_task = saas_memo_rows[0][1]
    saas_memo_staging = saas_memo_rows[0][2]
    saas_memo_production = format_multiple_entries([row[3] for row in saas_memo_rows])  # Combine all production data

# Populate the HTML template with the data
html_content = html_template.format(
    monitoring_task=monitoring_task,
    monitoring_staging=monitoring_staging,
    monitoring_production=monitoring_production,
    deployment_task=deployment_task,
    deployment_staging=deployment_staging,
    deployment_production=deployment_production,
    saas_memo_task=saas_memo_task,
    saas_memo_staging=saas_memo_staging,
    saas_memo_production=saas_memo_production
)

# Save the populated HTML to a file
with open("shift_report.html", "w") as file:
    file.write(html_content)

print("HTML Report generated successfully!")
