import json
from logging import exception
import os
import re
import sys
import requests
from datetime import datetime

def get_commit_date(repo_url, commit_hash):
    """
    Get the date of a commit using the GitHub API.
    """
    # Extract owner and repo name from the URL
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    owner, repo = match.groups()
    repo = repo.replace(".git", "")  # Remove .git from the repo name if it's there
    
    # Make a request to the GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_hash}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Warning: Failed to fetch commit info: {response.status_code} for {api_url}")
        return None  # Return None instead of an integer
    
    commit_data = response.json()
    commit_date = datetime.strptime(commit_data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
    
    return commit_date

def is_more_recent(repo_url, hash1, hash2):
    """
    Compare two commit hashes and return True if hash1 is more recent than hash2.
    """
    date1 = get_commit_date(repo_url, hash1)
    date2 = get_commit_date(repo_url, hash2)
    
    if date1 is None or date2 is None:
        print(f"Warning: Unable to compare commit dates for repo {repo_url} with hashes {hash1} and {hash2}. Skipping comparison.")
        return False  # Default to False if comparison isn't possible
    
    return date1 > date2

def create_environment(root_dir):
    all_downloads = {}
    all_snapshots = {"comfyui": "", "git_custom_nodes": {}}
    workflows_dir = os.path.join(root_dir, "workflows")

    for subdir in os.listdir(workflows_dir):
        subdir_path = os.path.join(workflows_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        for file_name in ['downloads.json', 'auto_downloads.json']:
            file_path = os.path.join(subdir_path, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    try:
                        all_downloads.update(json.load(f))
                    except json.JSONDecodeError as e:
                        print(f"Warning: Failed to parse {file_path}: {e}")
                break

        for file_name in ['snapshot.json', 'auto_snapshot.json']:
            file_path = os.path.join(subdir_path, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    try:
                        snapshot = json.load(f)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Failed to parse {file_path}: {e}")
                        continue  # Skip this snapshot file
                try:    
                    if snapshot.get("comfyui") != all_snapshots["comfyui"]:
                        if all_snapshots["comfyui"]:
                            print(f"Updating ComfyUI hash in {subdir_path}: {all_snapshots['comfyui']} -> {snapshot['comfyui']}")
                    all_snapshots["comfyui"] = snapshot["comfyui"]
                except Exception as e:
                    print(f"Warning: Failed to update ComfyUI hash in {subdir_path}: {e}")
                for repo, data in snapshot.get("git_custom_nodes", {}).items():
                    existing_data = all_snapshots["git_custom_nodes"].get(repo)
                    if existing_data is None or is_more_recent(repo, data["hash"], existing_data.get("hash")):
                        all_snapshots["git_custom_nodes"][repo] = data
                        print(f"Updating hash for {repo} in {subdir_path}")
                break

    # Save merged downloads.json
    downloads_path = os.path.join(root_dir, "downloads.json")
    try:
        with open(downloads_path, 'w') as f:
            json.dump(all_downloads, f, indent=4)
    except IOError as e:
        print(f"Error: Failed to write to {downloads_path}: {e}")
        sys.exit(1)

    # Save merged snapshot.json
    snapshot_path = os.path.join(root_dir, "snapshot.json")
    try:
        with open(snapshot_path, 'w') as f:
            json.dump(all_snapshots, f, indent=4)
    except IOError as e:
        print(f"Error: Failed to write to {snapshot_path}: {e}")
        sys.exit(1)

    print("Environment files created successfully.")

if __name__ == '__main__':

    """
    Tries to automatically merge downloads.json and snapshot.json for all workflows in the specified folder.
    When clashing git hashes are encountered, will resort to using the most recent commit hash and print a warning.

    example usage:

cd /home/rednax/SSD2TB/Github_repos/Eden/workflows/_utils
python generate_environment.py /home/rednax/SSD2TB/Github_repos/Eden/workflows/workspaces/flux_merge

DRMBT

cd C:\github\workflows\workspaces\flux\workflows\_utils
python generate_environment.py C:\github\workflows\workspaces\flux 

    """

    if len(sys.argv) != 2:
        print("Usage: python generate_environment.py <environment_folder>")
        sys.exit(1)

    environment_folder = sys.argv[1]

    create_environment(environment_folder)