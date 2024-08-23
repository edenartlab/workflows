import json
import os
import re
import sys

def process_workflow(subfolder, download_library_path):
    # Construct the workflow path
    workflow_path = os.path.join('..', 'public_workflows', subfolder, 'workflow_api.json')

    # Check if the workflow file exists
    if not os.path.exists(workflow_path):
        print(f"Error: Workflow file not found at {workflow_path}")
        return

    # Read the workflow file
    with open(workflow_path, 'r') as f:
        workflow_content = f.read().lower()  # Convert to lowercase for case-insensitive search

    # Read the downloads file
    with open(download_library_path, 'r') as f:
        download_library = json.load(f)

    # Initialize the do_downloads dictionary
    do_downloads = {}

    # Scan the workflow content for each target in the downloads
    for key, value in download_library.items():
        if re.search(re.escape(key.lower()), workflow_content):
            source = value['source']
            target = value['target']
            do_downloads[target] = source

    # Save do_downloads.json alongside workflow.json
    output_path = os.path.join(os.path.dirname(workflow_path), 'auto_downloads.json')
    with open(output_path, 'w') as f:
        json.dump(do_downloads, f, indent=4)

    print(f"auto_downloads.json has been saved to {output_path}")

if __name__ == '__main__':

    """
    Tries to automatically create downloads.json from workflow.json and download_library.json
    """

    if len(sys.argv) != 2:
        print("Usage: python generate_downloads.py <workflow_foldername>")
        sys.exit(1)

    subfolder = sys.argv[1]
    download_library_path = 'download_library.json'

    process_workflow(subfolder, download_library_path)