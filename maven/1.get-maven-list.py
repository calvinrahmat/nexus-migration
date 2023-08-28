import json
import requests
import argparse
import pandas as pd

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Script to export and update Maven assets')
parser.add_argument('-s', '--url', type=str, required=True, help='Base URL')
parser.add_argument('-u', '--username', type=str, required=True, help='Username')
parser.add_argument('-p', '--password', type=str, required=True, help='Password')
args = parser.parse_args()

# Read the repository list
repo_list = "repository-list.xlsx"
url = args.url
username = args.username
password = args.password

repo_list_df = pd.read_excel(repo_list)
maven_rows = repo_list_df[(repo_list_df['Format'] == 'maven2') & (repo_list_df['Type'] == 'hosted')]

data_list = []
for index, row in maven_rows.iterrows():
    repository = row["Repository"]
    url_assets = f"{url}/service/rest/v1/components?repository={repository}"
    headers = {"User-Agent": "curl/7.68.0"}
    auth = (username, password)
    response = requests.get(url_assets, headers=headers, auth=auth)
    json_data = json.loads(response.text)
    for item in json_data["items"]:
        assets = item.get("assets", [])
        for asset in assets:
            data_list.append({
                "downloadUrl": asset["downloadUrl"]
            })

# Create DataFrame and export to Excel
df = pd.DataFrame(data_list)
excel_file_path = "maven-assets.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Maven Assets exported to {excel_file_path}")

# Update URLs in the exported Excel file
first_url = df.loc[0, "downloadUrl"]
old_url_part = first_url.split("/")[2]
new_url_part = "172.178.75.31:8081"
df["targetUrl"] = df["downloadUrl"].str.replace(old_url_part, new_url_part)

# Update the existing Excel file with the new column
df.to_excel(excel_file_path, index=False)
print(f"Updated Maven Assets exported to {excel_file_path}")

