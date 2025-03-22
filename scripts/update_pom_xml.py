import requests
import os
import base64
import json
import argparse
import traceback
import time


def get_github_repo_id(repo):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("id")
    else:
        raise Exception(f"Failed to fetch repo ID: {response.status_code} - {response.text}")

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

# Function to create a pull request using normal GitHub API
def create_pull_request(repo, token, commit_id, git_org):
    # Adjust the URL to use the normal GitHub API
    url = f"https://api.github.com/repos/{repo}/pulls"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the pull request data
    pr_data = {
        "title": f"detected vulnerabilities fixed in pom.xml",
        "body": f"detected vulnerabilities fixed in pom.xml",
        "head": f"{git_org}:{commit_id}",
        "base": "main"
    }

    # Send the POST request to create the pull request
    response = requests.post(url, headers=headers, json=pr_data)
    

    if response.status_code == 201:
        pr_response_json = response.json()
        print(pr_response_json)
        pr_url = response.json()['html_url']  # Extract the PR URL

        print(pr_url)
        print(f"Pull request created successfully for {commit_id}.")
        return pr_url  # Return the PR URL for use in further steps

    else:
        raise Exception(f"Failed to create pull request: {response.status_code} - {response.text}")

# Function to create a GitHub issue and mention the PR link
def create_github_issue(repo, token, commit_id, pr_url, git_org):
    url = f"https://api.github.com/repos/{repo}/issues"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare the issue data with meaningful details
    issue_data = {
        "title": f"Vulnerabilities fixed in pom.xml for commit {commit_id}",
        "body": (
            f"### Vulnerability Fix Notification\n\n"
            f"#### Pull Request Details:\n"
            f"- **Commit ID:** `{commit_id}`\n"
            f"- **Repository:** `{repo}`\n\n"
            f"#### Summary:\n"
            f"The vulnerabilities detected in the `pom.xml` file have been resolved in the commit `{commit_id}`. "
            f"As part of the security compliance, these vulnerabilities have been addressed to ensure the project "
            f"remains secure and up-to-date.\n\n"
            f"#### Changes Made:\n"
            f"- Fixed vulnerabilities in the `pom.xml` file.\n"
            f"- Updated dependencies to more secure versions.\n"
            f"- Enhanced project configuration for better security.\n\n"
            f"#### Pull Request:\n"
            f"- [View the Pull Request Here]({pr_url})\n\n"
            f"#### Next Steps:\n"
            f"Please review the pull request and merge it once verified. "
            f"Monitor the deployment for any issues after the merge.\n\n"
            f"**Note:** This issue has been created to track the resolution of vulnerabilities and to ensure the project "
            f"stays secure."
        ),
        "labels": ["vulnerabilities", "security", "pom.xml"]
    }

    # Send the POST request to create the issue
    response = requests.post(url, headers=headers, json=issue_data)

    if response.status_code == 201:
        print(f"GitHub issue created successfully for commit {commit_id}.")
    else:
        raise Exception(f"Failed to create issue: {response.status_code} - {response.text}")
        traceback.print_exc()


# Main function to handle the workflow
def main():
    
    parser = argparse.ArgumentParser(description="Filter and format JSON data")
    # parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("pom_file", help="Path to the pom.xml file")


    args = parser.parse_args()
    pom_file = args.pom_file

    # Fetch environment variables from GitHub Actions
    # project_id = os.getenv('PROJECT_ID')  # This should be the project_id passed in as input or environment
    commit_id = os.getenv('GITHUB_SHA')[0:7]  # The new branch name
    github_token = os.getenv('MY_TOKEN')  # The GitHub token to authenticate API requests
    # print(github_token)

    repo = os.getenv('GITHUB_REPOSITORY')  # GitHub repository (owner/repo)
    git_org = repo.split("/")[0]

    try:

        time.sleep(30)

        project_id = get_github_repo_id(repo)

        print( "step 1")
        # Step 1: Fetch the latest scan data
        scan_data = get_latest_scan(project_id)
        scan_data = json.dumps(scan_data, indent=2)
        scan_data = json.loads(scan_data)

        print( "step 2")
        # Step 2: Decode the base64 encoded pom.xml content
        pom_base64_content = scan_data['solution']['file']

        print(pom_base64_content)
        pom_content = decode_base64_pom(pom_base64_content)

        print( "step 3")
        # Step 3: Get the default branch of the repo
        default_branch = get_default_branch(repo, github_token)

        print( "step 4")
        # Step 4: Create a new branch based on the commit ID
        create_new_branch(repo, commit_id, github_token, default_branch)

        print( "step 5")
        # Step 5: Commit the new pom.xml file to the specified path in the new branch
        commit_file_changes(repo, commit_id, pom_file, pom_content, github_token)
        
        print( "step 6")
        # Step 6: Create a pull request
        pr_url = create_pull_request(repo, github_token, commit_id, git_org)

        print( "step 7")
        # Step 7: Create a GitHub issue with a reference to the PR
        create_github_issue(repo, github_token, commit_id, pr_url, git_org)

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
