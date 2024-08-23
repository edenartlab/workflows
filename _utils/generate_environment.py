import json
import os
import re
import sys


import json
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
    
    # Make a request to the GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_hash}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch commit info: {response.status_code}")
    
    commit_data = response.json()
    commit_date = datetime.strptime(commit_data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
    
    return commit_date

def is_more_recent(repo_url, hash1, hash2):
    """
    Compare two commit hashes and return True if hash1 is more recent than hash2.
    """
    date1 = get_commit_date(repo_url, hash1)
    date2 = get_commit_date(repo_url, hash2)
    return date1 > date2


def create_environment(root_dir):
    """
    - Iterate over all the individual workflow directories in the root_dir
    - Load all the respective downloads.json and snapshot.json files
    - Create a single downloads.json file (keep all unique entries)
    - Create a single snapshot.json file (keep the most recent commit hash)
    - save these files in the root_dir
    """
    all_downloads = {}
    all_snapshots = {"comfyui": "", "git_custom_nodes": {}}

    workflows_dir = os.path.join(root_dir, "workflows")

    # Iterate through all subdirectories
    for subdir in os.listdir(workflows_dir):
        subdir_path = os.path.join(workflows_dir, subdir)
        if os.path.isdir(subdir_path):
            # Check for downloads.json
            downloads_path = os.path.join(subdir_path, "downloads.json")
            if os.path.exists(downloads_path):
                with open(downloads_path, 'r') as f:
                    downloads = json.load(f)
                    all_downloads.update(downloads)

            # Check for snapshot.json
            snapshot_path = os.path.join(subdir_path, "snapshot.json")
            if os.path.exists(snapshot_path):
                with open(snapshot_path, 'r') as f:
                    snapshot = json.load(f)
                    
                    # Update ComfyUI hash if it's different from the one already stored in all_snapshots
                    if "comfyui" in snapshot and snapshot["comfyui"] != all_snapshots["comfyui"]:
                        if all_snapshots["comfyui"]:
                            print(f"Found different ComfyUI hash in {subdir_path}, updating... (old: {all_snapshots['comfyui']}, new: {snapshot['comfyui']})")
                        all_snapshots["comfyui"] = snapshot["comfyui"]
                    
                    # Update git_custom_nodes
                    for repo, data in snapshot.get("git_custom_nodes", {}).items():
                        if repo not in all_snapshots["git_custom_nodes"]:
                            all_snapshots["git_custom_nodes"][repo] = data
                        elif is_more_recent(repo, data["hash"], all_snapshots["git_custom_nodes"][repo]["hash"]):
                            all_snapshots["git_custom_nodes"][repo] = data
                            print(f"Found newer hash for {repo} in {subdir_path}, updating...")
                            

    # Save merged downloads.json
    with open(os.path.join(root_dir, "env_downloads.json"), 'w') as f:
        json.dump(all_downloads, f, indent=4)

    # Save merged snapshot.json
    with open(os.path.join(root_dir, "env_snapshot.json"), 'w') as f:
        json.dump(all_snapshots, f, indent=4)

    print("Environment files created successfully.")

if __name__ == '__main__':

    """
    Tries to automatically merge downloads.json and snapshot.json for all workflows in the specified folder.
    When clashing git hashes are encountered, will resort to using the most recent commit hash and print a warning.

    example usage:
    cd /home/rednax/SSD2TB/Github_repos/Eden/workflows/_utils
    python generate_environment.py /home/rednax/SSD2TB/Github_repos/Eden/workflows/environments/test
    """

    if len(sys.argv) != 2:
        print("Usage: python generate_environment.py <environment_folder>")
        sys.exit(1)

    environment_folder = sys.argv[1]

    create_environment(environment_folder)