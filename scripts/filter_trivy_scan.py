import json
import os
import argparse
import base64

def filter_json(input_file_path, pom_file_path):
    try:

        with open(input_file_path, 'r') as file:
            data = json.load(file)
            
        scan_id = os.getenv("GITHUB_SHA", "unknown")
        project_name = os.getenv("GITHUB_REPOSITORY", "unknown")
        repo_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{project_name}.git"

        with open(pom_file_path, 'rb') as pom_file:
            pom_base64 = base64.b64encode(pom_file.read()).decode('utf-8')

        filtered_data = {
            "scanId": scan_id[0:7],
            "projectName": project_name,
            "repo_url": repo_url,
            "pom.xml": pom_base64, 
            "vulnerabilities": []
        }

        for result in data.get("Results", []):
            vulnerabilities = result.get("Vulnerabilities", [])


            for vuln in vulnerabilities:
                title = vuln.get("Title", "")

                category = title.split(":")[-1].strip() if ":" in title else "Unknown"

                filtered_vuln = {
                    "VulnerabilityID": vuln.get("VulnerabilityID"),
                    "PkgID": vuln.get("PkgID"),
                    "PkgName": vuln.get("PkgName"),
                    "Remediation": [
                        f"This vulnerability in {vuln.get('PkgID')} is fixed in {vuln.get('FixedVersion')}"
                    ],   
                    "Category": category,
                    "Title": title,
                    "Description": vuln.get("Description"),
                    "Severity": vuln.get("Severity"),
                }
                filtered_data["vulnerabilities"].append(filtered_vuln)

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
