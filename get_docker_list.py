import requests
import pandas as pd
import json
# Define the URL
excel_filename = "docker-repository-list.xlsx"  # Update the filename if needed
docker_host = "nexusdemo.izenoondemand.com:8081"
df = pd.read_excel(excel_filename)
# Loop through rows using iterrows()
for index, row in df.iterrows():
    repository = row["Repository"]  # Assuming "Repository Name" is the column name
url = f"http://nexusdemo.izenoondemand.com:8081/service/rest/v1/components?repository={repository}"
docker_host = "nexusdemo.izenoondemand.com:8081"
headers = {"User-Agent": "curl/7.68.0"}
auth = ("gEAH43-u", "C-7ram1GLh6z6zTL40pHTSJ9O_blH7BP6CPMwtyifLt_")
response = requests.get(url, headers=headers, auth=auth)
# Fetch the JSON data
json_data = json.loads(response.text)
# Extract repository, name, and version from the JSON
data = json_data.get("items", [])
extracted_data = []
for item in data:
    extracted_data.append({
        "Repository": item["repository"],
        "Name": item["name"],
        "Version": item["version"]
    })

# Create a DataFrame using the extracted data
df = pd.DataFrame(extracted_data)

# Export the DataFrame to an Excel file
excel_filename = "image_data.xlsx"
df.to_excel(excel_filename, index=False)

print("Data exported to", excel_filename)
