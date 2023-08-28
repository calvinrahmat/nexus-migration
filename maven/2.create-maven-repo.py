import argparse
import requests
import pandas as pd
import json

def copy_repository(source_url, target_url, source_auth, target_auth, repository):
    headers = {"User-Agent": "curl/7.68.0", "Content-Type": "application/json"}

    source_repo = f"{source_url}/service/rest/v1/repositories/maven/hosted/{repository}"
    target_repo = f"{target_url}/service/rest/v1/repositories/maven/hosted"

    source_repo_res = requests.get(source_repo, headers=headers, auth=source_auth)

    if source_repo_res.status_code == 200:
        json_data = source_repo_res.json()
        json_data.pop('url', None)

        create_repo_res = requests.post(target_repo, json=json_data, headers=headers, auth=target_auth)

        if create_repo_res.status_code == 201:
            print(f"Repository {repository} created  successfully.")
        else:
            print(f"Failed to copy repository {repository}. Status code: {create_repo_res.status_code}")
            print(create_repo_res.text)
    else:
        print(f"Source repository {repository} not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to copy Maven repositories between Nexus instances')
    parser.add_argument('-s', '--source-url', type=str, required=True, help='Source URL')
    parser.add_argument('-u', '--source-username', type=str, required=True, help='Source username')
    parser.add_argument('-p', '--source-password', type=str, required=True, help='Source password')
    parser.add_argument('-t', '--target-url', type=str, required=True, help='Target URL')
    parser.add_argument('-U', '--target-username', type=str, required=True, help='Target username')
    parser.add_argument('-P', '--target-password', type=str, required=True, help='Target password')
    args = parser.parse_args()

    source_url = args.source_url
    source_auth = (args.source_username, args.source_password)
    target_url = args.target_url
    target_auth = (args.target_username, args.target_password)

    maven_list_df = pd.read_excel("maven-list.xlsx")

    for index, row in maven_list_df.iterrows():
        repository = row["Repository"]
        copy_repository(source_url, target_url, source_auth, target_auth, repository)

