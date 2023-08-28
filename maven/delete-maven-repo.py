import os
import requests
import pandas as pd
import json

target_url = "http://172.178.75.31:8081"

maven_list_df = pd.read_excel("maven-list.xlsx")
headers = {"User-Agent": "curl/7.68.0", "Content-Type": "application/json"}
target_auth = ("admin", "admin123!")

for index,row in maven_list_df.iterrows():
    repository = row["Repository"]
    target_repo = f"{target_url}/service/rest/v1/repositories/{repository}"
    delete_repo = requests.delete(target_repo, headers=headers, auth=target_auth)
    if delete_repo.status_code == 204:
        print(f"Maven repo {repository} deleted")
    else:
        print(f"Cannot delete {repository} {delete_repo.content}")
