import json
import requests
import pandas as pd
import os
import subprocess

url = "http://nexusdemo.izenoondemand.com:8081"
url_repo = f"{url}/service/rest/v1/repositories"
headers = {"User-Agent": "curl/7.68.0"}
auth = ("gEAH43-u", "C-7ram1GLh6z6zTL40pHTSJ9O_blH7BP6CPMwtyifLt_")
response = requests.get(url_repo, headers=headers, auth=auth)


json_data = json.loads(response.text)

data_list = []
for item in json_data:
    data_list.append({
        "Repository Name": item["name"],
        "Format": item["format"],
        "Type": item["type"],
        "URL": item["url"]
    })

df = pd.DataFrame(data_list)

excel_file = "output.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")

print(f"Data exported to {excel_file}")

if not os.path.exists("./repos"):
    try:
        os.makedirs("./repos")
    except Exception as e:
        print(f"An error occurred while creating folder: {e}")
    else:
        print("Folder repos created successfully.")
else:
    print("Folder 'repos' already exists.")

parent_directory = "./repos"  # Replace with your desired parent directory path

for item in json_data:
    folder_name = item["name"]
    folder_path = os.path.join(parent_directory, folder_name)
    url_asset = f"{url}/service/rest/v1/assets?repository={folder_name}"
    response = requests.get(url_asset, headers=headers, auth=auth)

    json_data = json.loads(response.text)

    download_url  = [item["downloadUrl"] for item in json_data["items"]]
    formats = [item["format"] for item in json_data["items"]]
    df = pd.DataFrame({"DownloadUrl": download_url, "Format": formats})

    excel_file = f"{folder_path}/assets.xlsx"
    file_name = item["name"]
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            print(f"Folder '{folder_name}' created at '{folder_path}'")
        except OSError as e:
            print(f"Error creating folder '{folder_name}': {e}")
    else:
        print(f"Folder '{folder_path}' already exists.")
    df.to_excel(excel_file, index=False, engine="openpyxl")
