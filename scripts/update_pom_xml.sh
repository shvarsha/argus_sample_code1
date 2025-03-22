#!/bin/bash

# Function to fetch the latest scan details from the provided API
get_latest_scan() {
    local project_id="$1"
    echo "Fetching the latest scan data for project ID: $project_id"
    response=$(curl -s -H "accept: application/json" "http://54.174.73.151:8000/v1/latestScan?project_id=${project_id}")
    
    if [[ $? -eq 0 ]]; then
        echo "$response"
    else
        echo "Failed to fetch latest scan data."
        exit 1
    fi
}

# Function to decode base64 content of the pom.xml
decode_base64_pom() {
    local base64_content="$1"
    echo "$base64_content" | base64 --decode
}

# Function to get the default branch of the repository
get_default_branch() {
    local repo="$1"
    echo "Fetching default branch for repo: $repo"
    default_branch=$(gh repo view "$repo" --json defaultBranch --jq '.defaultBranch')

    if [[ $? -eq 0 ]]; then
        echo "$default_branch"
    else
        echo "Failed to fetch default branch data."
        exit 1
    fi
}

# Function to create a new branch based on the default branch
create_new_branch() {
    local repo="$1"
    local commit_id="$2"
    local default_branch="$3"

    echo "Creating a new branch based on the default branch: $default_branch"
    git fetch origin "$default_branch"
    git checkout -b "$commit_id" origin/"$default_branch"

    if [[ $? -eq 0 ]]; then
        echo "Branch $commit_id created successfully."
    else
        echo "Failed to create new branch."
        exit 1
    fi
}

# Function to commit the file changes to the new branch
commit_file_changes() {
    local repo="$1"
    local commit_id="$2"
    local pom_file="$3"
    local pom_content="$4"

    echo "Committing changes to file $pom_file in branch $commit_id"
    echo "$pom_content" > "$pom_file"

    git add "$pom_file"
    git commit -m "Replace $pom_file with new pom.xml contents"
    git push origin "$commit_id"

    if [[ $? -eq 0 ]]; then
        echo "Changes committed successfully to branch $commit_id."
    else
        echo "Failed to commit changes."
        exit 1
    fi
}

# Function to create a pull request using GitHub CLI (instead of API call)
create_pull_request() {
    local repo="$1"
    local commit_id="$2"
    local tenant_unique_name="$3"
    local github_username="$4"
    
    echo "Creating pull request for branch $commit_id"
    gh pr create --repo "$repo" \
        --title "Service Broker Values for $tenant_unique_name" \
        --body "Service Broker values.yaml for $tenant_unique_name" \
        --head "$github_username:$commit_id" \
        --base main
    
    if [[ $? -eq 0 ]]; then
        echo "Pull request created successfully."
    else
        echo "Failed to create pull request."
        exit 1
    fi
}

# Main function to handle the workflow
main() {
    # Fetch environment variables from GitHub Actions or environment
    project_id="${PROJECT_ID}" # Set project ID
    commit_id="${GITHUB_SHA}"  # The new branch name
    repo="${GITHUB_REPOSITORY}"  # GitHub repository (owner/repo)
    pom_file="$1"  # Path to the pom.xml file
    tenant_unique_name="$2"  # Tenant unique name
    github_username="$3"  # GitHub username

    if [[ -z "$project_id" || -z "$commit_id" || -z "$repo" || -z "$pom_file" || -z "$tenant_unique_name" || -z "$github_username" ]]; then
        echo "Missing required environment variables or arguments."
        exit 1
    fi

    echo "step 1: Fetching latest scan data"
    scan_data=$(get_latest_scan "$project_id")
    pom_base64_content=$(echo "$scan_data" | jq -r '.solution.file')

    echo "step 2: Decoding base64 content of pom.xml"
    pom_content=$(decode_base64_pom "$pom_base64_content")

    echo "step 3: Fetching the default branch of the repository"
    default_branch=$(get_default_branch "$repo")

    echo "step 4: Creating a new branch based on the default branch"
    create_new_branch "$repo" "$commit_id" "$default_branch"

    echo "step 5: Committing changes to the repository"
    commit_file_changes "$repo" "$commit_id" "$pom_file" "$pom_content"

    echo "step 6: Creating a pull request"
    create_pull_request "$repo" "$commit_id" "$tenant_unique_name" "$github_username"
}

# Run the script
main "$@"
