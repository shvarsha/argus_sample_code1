import json
import base64
import os
import requests
import argparse
import re


def get_github_repo_id(repo):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get("id")
    else:
        raise Exception(f"Failed to fetch repo ID: {response.status_code} - {response.text}")

def filter_json(input_file_path, pom_file_path):
    try:

        with open(input_file_path, 'r') as file:
            data = json.load(file)
            
        scan_id = os.getenv("GITHUB_SHA", "unknown")
        project_name = os.getenv("GITHUB_REPOSITORY", "unknown")
        repo_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{project_name}"
        job_run_id = os.getenv("GITHUB_RUN_ID", "unknown")

        scan_link = repo_url+"/actions/runs/"+job_run_id

        repo_id = get_github_repo_id(project_name)


        with open(pom_file_path, 'rb') as pom_file:
            pom_base64 = base64.b64encode(pom_file.read()).decode('utf-8')

        filtered_data = {
            "project_name": project_name.split("/")[1],
            "project_id": str(repo_id),
            "scan_id": scan_id[0:7],
            "git_link": repo_url,
            "scan_link": [scan_link],
            "cves": [],
            "pom_xml": pom_base64, 
            "tags": [scan_id[0:7]]
            
        }

        for result in data.get("Results", []):
            vulnerabilities = result.get("Vulnerabilities", [])


            for vuln in vulnerabilities:
                title = vuln.get("Title", "")

                category = title.split(":")[-1].strip() if ":" in title else "Unknown"

                filtered_vuln = {
                    "category": category,
                    "solutions": [
                        f"This vulnerability in {vuln.get('PkgID')} package is fixed in {vuln.get('FixedVersion')} versions."
                    ],  
                    "severity": vuln.get("Severity"),
                    "cve_id": vuln.get("VulnerabilityID"),
                    "description": vuln.get("Description"),
                    "vulnerability": title
                }
                filtered_data["cves"].append(filtered_vuln)

        filtered_json = json.dumps(filtered_data, indent=2)
        return filtered_json

    except FileNotFoundError:
        return "The specified file was not found."
    except json.JSONDecodeError:
        return "The file is not a valid JSON."

def main():
    parser = argparse.ArgumentParser(description="Filter and format JSON data")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("pom_file", help="Path to the pom.xml file")

    args = parser.parse_args()

    filtered_json = filter_json(args.input_file, args.pom_file)
    print(filtered_json)


if __name__ == "__main__":
    main()
