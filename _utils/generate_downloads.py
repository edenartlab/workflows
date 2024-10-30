import json
import os
import re
import sys

def process_workflow(workflow_dir, download_library_path):
    # Construct the workflow path
    workflow_path = os.path.join(workflow_dir, 'workflow_api.json')

    # Check if the workflow file exists
    if not os.path.exists(workflow_path):
        print(f"Error: Workflow file not found at {workflow_path}")
        return

    # Read the workflow file
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow_content = f.read().lower()  # Convert to lowercase for case-insensitive search

    # Read the downloads file
    with open(download_library_path, 'r') as f:
        download_lib = json.load(f)

    download_library = download_lib['files']
    node_library = download_lib['nodes']

    # Initialize the do_downloads dictionary
    do_downloads = {}

    # Scan the workflow content for each target in the downloads
    for key, value in download_library.items():
        if re.search(re.escape(key.lower()), workflow_content):
            source = value['source']
            target = value['target']
            do_downloads[target] = source

    # Scan the workflow content for each target in the nodes
    for key, item_list in node_library.items():
        if re.search(re.escape(key.lower()), workflow_content):
            # loop through all the downloads for this node:
            for dict_entry in item_list:
                source = dict_entry['source']
                target = dict_entry['target']
                do_downloads[target] = source

    # Save do_downloads.json alongside workflow_api.json
    output_path = os.path.join(os.path.dirname(workflow_path), 'auto_downloads.json')
    with open(output_path, 'w') as f:
        json.dump(do_downloads, f, indent=4)

    print(f"auto_downloads.json has been saved to {output_path}")

if __name__ == '__main__':

    """
    Tries to automatically create downloads.json from workflow_api.json and download_library.json

    example usage:

cd /home/rednax/SSD2TB/Github_repos/Eden/workflows/_utils
python generate_downloads.py /home/rednax/SSD2TB/Github_repos/Eden/workflows/workspaces/flux_inpainting/workflows/flux_inpainting


DRMBT

cd C:\github\workflows\workspaces\flux\workflows\_utils
python generate_downloads.py C:\github\workflows\workspaces\flux\workflows\remix-flux-schnell  

    """

    if len(sys.argv) != 2:
        print("Usage: python generate_downloads.py <workflow_foldername>")
        sys.exit(1)

    workflow_dir = sys.argv[1]
    download_library_path = 'download_library.json'

    process_workflow(workflow_dir, download_library_path)


