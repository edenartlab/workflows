import json
import os
import sys
import shutil
import re
from datetime import datetime
import requests

def backup_master_snapshot(master_snapshot_path):
    # Ensure the backup directory exists
    backup_dir = os.path.join(os.path.dirname(master_snapshot_path), "snapshot_backups")
    os.makedirs(backup_dir, exist_ok=True)

    # Create a backup of the current master_snapshot.json with a formatted timestamp
    timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
    backup_path = os.path.join(backup_dir, f"master_snapshot_{timestamp}.json")
    shutil.copy(master_snapshot_path, backup_path)
    print(f"Backup created at {backup_path}")

def get_commit_date(repo_url, commit_hash):
    # Function to get the commit date from GitHub
    match = re.match(r'https://github.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    owner, repo = match.groups()
    repo = repo.replace(".git", "")
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_hash}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch commit info: {response.status_code} for {api_url}")
        return None
    
    commit_data = response.json()
    commit_date = datetime.strptime(commit_data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
    
    return commit_date

def is_more_recent(repo_url, hash1, hash2):
    # Compare two commit hashes
    date1 = get_commit_date(repo_url, hash1)
    date2 = get_commit_date(repo_url, hash2)
    return date1 > date2

def get_nodes_from_python_file(filepath):
    # Extract node names from a `nodes*.py` file based on its NODE_CLASS_MAPPINGS dictionary.
    if not os.path.exists(filepath):
        print(f"Error: '{filepath}' not found.")
        sys.exit(1)
    if os.path.isdir(filepath):
        print(f"Error: '{filepath}' is a directory, expected a Python file.")
        sys.exit(1)

    nodes = set()
    node_class_mappings_found = False
    node_pattern = re.compile(r'"([^"]+)"')

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("NODE_CLASS_MAPPINGS"):
                node_class_mappings_found = True
                continue
            if node_class_mappings_found:
                if line.startswith("}"):
                    break
                # Find all matches between quotes and add to the set
                matches = node_pattern.findall(line)
                nodes.update(matches)

    return nodes

def get_built_in_nodes(comfyui_path):
    # Collect all built-in nodes by parsing `nodes.py` file and any` nodes_*.py` files
    # in `comfy_extras`.

    main_nodes_py_path = os.path.join(comfyui_path, "nodes.py")
    built_in_nodes = get_nodes_from_python_file(main_nodes_py_path)

    comfy_extras_dir = os.path.join(comfyui_path, "comfy_extras")
    if os.path.exists(comfy_extras_dir) and os.path.isdir(comfy_extras_dir):
        for filename in os.listdir(comfy_extras_dir):
            if filename.startswith("nodes_") and filename.endswith(".py"):
                extras_file_path = os.path.join(comfy_extras_dir, filename)
                extras_nodes = get_nodes_from_python_file(extras_file_path)
                built_in_nodes.update(extras_nodes)

    return built_in_nodes

def update_master_snapshot(comfyui_path, master_snapshot_path):
    # Load the current master snapshot
    with open(master_snapshot_path, 'r') as f:
        master_snapshot = json.load(f)

    # Get built-in nodes
    built_in_nodes = get_built_in_nodes(comfyui_path)

    # Example logic to map node names to repository data
    # This is a placeholder and needs to be replaced with actual logic
    node_to_repo_data = {}  # This should map node names to repo data, e.g., {'node_name': {'hash': '...', 'url': '...'}}

    # Update the master snapshot with new or more recent nodes
    for node_name in built_in_nodes:
        if node_name in node_to_repo_data:
            repo_data = node_to_repo_data[node_name]
            repo_url = repo_data['url']
            if repo_url not in master_snapshot['git_custom_nodes'] or is_more_recent(repo_url, repo_data['hash'], master_snapshot['git_custom_nodes'][repo_url]['hash']):
                master_snapshot['git_custom_nodes'][repo_url] = repo_data
                print(f"Updated hash for {repo_url}")

    # Save the updated master snapshot
    with open(master_snapshot_path, 'w') as f:
        json.dump(master_snapshot, f, indent=4)
    print("Master snapshot updated successfully.")

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python update_master.py <comfyui_path> [<master_snapshot_path>]")
        sys.exit(1)

    comfyui_path = sys.argv[1]
    master_snapshot_path = sys.argv[2] if len(sys.argv) == 3 else os.path.join(os.path.dirname(__file__), "master_snapshot.json")

    backup_master_snapshot(master_snapshot_path)
    update_master_snapshot(comfyui_path, master_snapshot_path)