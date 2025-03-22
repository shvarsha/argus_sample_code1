import requests
import os
import base64
import json
import argparse
import traceback


# Function to fetch the latest scan details from the provided API
def get_latest_scan(project_id):

    print(project_id)
    url = f'http://54.174.73.151:8000/v1/latestScan?project_id={project_id}'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch latest scan data: {response.status_code} - {response.text}")
        traceback.print_exc()

# Function to decode base64 content of the pom.xml
def decode_base64_pom(base64_content):
    try:
        return base64.b64decode(base64_content).decode('utf-8')
    except Exception as e:
        raise Exception(f"Error decoding base64 content: {e}")
        traceback.print_exc()

# Function to get the default branch of the repository
def get_default_branch(repo, token):
    url = f"https://api.github.com/repos/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get("default_branch")
    else:
        raise Exception(f"Failed to fetch repository data: {response.status_code} - {response.text}")
        traceback.print_exc()

# Function to create a new branch based on the default branch
def create_new_branch(repo, commit_id, token, default_branch):
    # Get the SHA of the latest commit on the default branch
    url = f"https://api.github.com/repos/{repo}/git/ref/heads/{default_branch}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        default_branch_data = response.json()
        base_commit_sha = default_branch_data['object']['sha']

        # Create a new branch from the base commit SHA
        new_branch_url = f"https://api.github.com/repos/{repo}/git/refs"
        new_branch_data = {
            "ref": f"refs/heads/{commit_id}",
            "sha": base_commit_sha
        }
        new_branch_response = requests.post(new_branch_url, headers=headers, json=new_branch_data)

        if new_branch_response.status_code == 201:
            print(f"Branch {commit_id} created successfully.")
        else:
            raise Exception(f"Failed to create branch: {new_branch_response.status_code} - {new_branch_response.text}")
    else:
        raise Exception(f"Failed to get default branch data: {response.status_code} - {response.text}")

# Function to replace the contents of a file in the repository and commit the change
def commit_file_changes(repo, commit_id, pom_file, pom_content, token):
    # Get the file's current SHA to update it (if the file doesn't exist, it'll return None)
    url = f"https://api.github.com/repos/{repo}/contents/{pom_file}?ref={commit_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        file_sha = file_data['sha']
    elif response.status_code == 404:
        file_sha = None  # If the file doesn't exist, we create a new file
    else:
        raise Exception(f"Failed to fetch file data: {response.status_code} - {response.text}")

    # Prepare the commit data
    commit_data = {
        "message": f"Replace {pom_file} with new pom.xml contents",
        "content": base64.b64encode(pom_content.encode('utf-8')).decode('utf-8'),  # Encoding the content back to base64 for GitHub API
        "branch": commit_id
    }

    if file_sha:
        commit_data["sha"] = file_sha  # If the file exists, add the SHA for update

    commit_url = f"https://api.github.com/repos/{repo}/contents/{pom_file}"
    commit_response = requests.put(commit_url, headers=headers, json=commit_data)

    if commit_response.status_code == 201 or commit_response.status_code == 200:
        print(f"Changes committed successfully to branch {commit_id}.")
    else:
        raise Exception(f"Failed to commit changes: {commit_response.status_code} - {commit_response.text}")
        traceback.print_exc()

# Main function to handle the workflow
def main():
    
    parser = argparse.ArgumentParser(description="Filter and format JSON data")
    # parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("pom_file", help="Path to the pom.xml file")

    # Fetch environment variables from GitHub Actions
    project_id = os.getenv('PROJECT_ID')  # This should be the project_id passed in as input or environment
    commit_id = os.getenv('GITHUB_SHA')  # The new branch name
    github_token = os.getenv('GITHUB_TOKEN')  # The GitHub token to authenticate API requests
    repo = os.getenv('GITHUB_REPOSITORY')  # GitHub repository (owner/repo)

    try:
        # print( "step 1")
        # # Step 1: Fetch the latest scan data
        # scan_data = get_latest_scan(project_id)
        # scan_data = json.dumps(scan_data, indent=2)
        # scan_data = json.loads(scan_data)

        # print(type(scan_data))

        # print(scan_data)

        # print( "step 2")
        # # Step 2: Decode the base64 encoded pom.xml content
        # pom_base64_content = scan_data['solution']['file']
        # pom_content = decode_base64_pom(pom_base64_content)

        print( "step 3")
        # Step 3: Get the default branch of the repo
        default_branch = get_default_branch(repo, github_token)
        print(default_branch)

        print( "step 4")
        # Step 4: Create a new branch based on the commit ID
        create_new_branch(repo, commit_id, github_token, default_branch)

        print( "step 5")
        # Step 5: Commit the new pom.xml file to the specified path in the new branch
        commit_file_changes(repo, commit_id, pom_file, pom_content, github_token)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
