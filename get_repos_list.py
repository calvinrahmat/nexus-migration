import json
import requests
import pandas as pd
import os
import subprocess
import re

url = "http://nexusdemo.izenoondemand.com:8081"
docker_host = "nexusdemo.izenoondemand.com:8081"
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

excel_file = "repository-list.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")

print(f"Data exported to {excel_file}")

