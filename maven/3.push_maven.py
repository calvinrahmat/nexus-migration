import argparse
import requests
import pandas as pd
import json
from urllib.parse import urlparse
import os

def download_and_upload_asset(download_url, upload_url, source_auth, target_auth):
    headers = {"User-Agent": "curl/7.68.0", "Content-Type": "application/json"}
    
    maven_res = requests.get(download_url, headers=headers, auth=source_auth)
    
    if maven_res.status_code == 200:
        parsed_url = urlparse(download_url)
        filename = os.path.basename(parsed_url.path)
        print(f"File {filename} downloaded successfully.")
        
        with open(filename, "wb") as f:
            f.write(maven_res.content)
        
        with open(filename, 'rb') as file:
            maven_upload = requests.put(upload_url, data=file, headers=headers, auth=target_auth)
            
            if maven_upload.status_code == 201:
                print(f"Upload successful {upload_url}")
                os.remove(filename)
            else:
                print(maven_upload.content)
    else:
        print(f"Failed to download file from {download_url}.{maven_res.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to download and upload Maven assets')
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

    maven_assets_df = pd.read_excel("maven-assets.xlsx")

    download_folder = "maven-assets"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    os.chdir(download_folder)

    for index, row in maven_assets_df.iterrows():
        download_url = row["downloadUrl"]
        upload_url = row["targetUrl"]
        download_and_upload_asset(download_url, upload_url, source_auth, target_auth)

