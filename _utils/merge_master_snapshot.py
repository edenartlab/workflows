import json
import os
import shutil
import sys
import time
import requests

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def backup_master_snapshot(master_snapshot_path):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = f"snapshot_backups/master_snapshot_{timestamp}.json"
    os.makedirs("snapshot_backups", exist_ok=True)  # Create the backup directory if it doesn't exist
    shutil.copy(master_snapshot_path, backup_path)
    print(f"Backup created: {backup_path}")

def compare_and_merge(input_data, master_data):
    updated_entries = []
    new_entries = []
    untouched_entries = []

    for repo_url, repo_info in input_data['git_custom_nodes'].items():
        if repo_url in master_data['git_custom_nodes']:
            master_hash = master_data['git_custom_nodes'][repo_url]['hash']
            if master_hash != repo_info['hash']:
                # Update the hash in the master data
                master_data['git_custom_nodes'][repo_url]['hash'] = repo_info['hash']
                updated_entries.append(repo_url)
                print(f"Updated hash for {repo_url}: {master_hash} -> {repo_info['hash']}")
            else:
                untouched_entries.append(repo_url)
                print(f"Untouched entry for {repo_url}: {master_hash}")
        else:
            # Add new entry
            master_data['git_custom_nodes'][repo_url] = repo_info
            new_entries.append(repo_url)
            print(f"Added new entry for {repo_url}: {repo_info['hash']}")

    return updated_entries, new_entries, untouched_entries

def update_dependencies(input_data, master_data):
    for package, version in input_data['pips'].items():
        if package in master_data['pips']:
            master_version = master_data['pips'][package]
            if version > master_version:
                master_data['pips'][package] = version
                print(f"Updated dependency {package}: {master_version} -> {version}")
        else:
            master_data['pips'][package] = version
            print(f"Added new dependency {package}: {version}")

def main(input_file):
    # Set the path for the master snapshot in the same directory as the script
    master_snapshot_path = os.path.join(os.path.dirname(__file__), 'master_snapshot.json')
    
    # Load the input and master snapshot data
    input_data = load_json(input_file)
    master_data = load_json(master_snapshot_path)

    # Backup the current master snapshot
    backup_master_snapshot(master_snapshot_path)

    # Compare and merge the data
    updated_entries, new_entries, untouched_entries = compare_and_merge(input_data, master_data)

    # Update dependencies
    update_dependencies(input_data, master_data)

    # Save the updated master snapshot
    save_json(master_snapshot_path, master_data)
    print("Master snapshot updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python merge_master.py <path_to_input_json>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    main(input_file_path)
    
    ### usage

    # python merge_master.py path/to/your/input_file.json