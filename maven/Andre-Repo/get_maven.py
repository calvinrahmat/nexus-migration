import requests

source_nexus_base_url = "http://nexusdemo.izenoondemand.com:8081/repository/maven-releases/"
target_nexus_base_url = "http://172.178.75.31:8081/repository/maven-releases/"
group_id = "org.springframework.boot"
artifact_id = "spring-boot-web-jsp"
version = "2.1"
artifact_path = f"{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"

# Construct the source and target artifact URLs
source_artifact_url = f"{source_nexus_base_url}{artifact_path}"
target_artifact_url = f"{target_nexus_base_url}{artifact_path}"

# Authentication credentials for source and target repositories
source_auth = ("gEAH43-u", "C-7ram1GLh6z6zTL40pHTSJ9O_blH7BP6CPMwtyifLt_")
target_auth = ("admin", "admin123!")

# Send a GET request to the source artifact URL to get the content
response = requests.get(source_artifact_url, auth=source_auth)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    pom_content = response.text
    local_file_path = f"{artifact_id}-{version}.pom"
    with open(local_file_path, "w") as f:
        f.write(pom_content) 
    # Send a PUT request to the target artifact URL to push the content
    put_response = requests.put(target_artifact_url, data=pom_content, headers={"Content-Type": "application/xml"}, auth=target_auth)
    
    # Check if the PUT request was successful (status code 201)
    if put_response.status_code == 201:
        print(f"POM file pushed successfully to {target_artifact_url}")
    else:
        print(f"Failed to push the POM file. {put_response.text} PUT status code: {put_response.status_code}")
else:
    print(f"Failed to retrieve the POM file. GET status code: {response.status_code}")

