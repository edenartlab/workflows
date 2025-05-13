import json
import os

DOWNLOADS_FILE = "workspaces/mono_workspace/downloads.json"
WORKFLOWS_DIR = "workspaces/mono_workspace/workflows"

def analyze_model_usage():
    """
    Analyzes downloads.json and workflow_api.json files to determine model usage.
    Outputs a summary of how often each downloaded model is referenced in workflows.
    """
    try:
        with open(DOWNLOADS_FILE, 'r') as f:
            downloads_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {DOWNLOADS_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DOWNLOADS_FILE}.")
        return

    model_usage = {}

    print(f"Iterating through {DOWNLOADS_FILE}...")
    for model_path_key in downloads_data.keys():
        model_usage[model_path_key] = {
            "count": 0,
            "found_in_workflows": set()  # Using a set to store unique directory names
        }

    print(f"Searching for workflow_api.json files in {WORKFLOWS_DIR}...")
    workflow_api_files = []
    for root, _, files in os.walk(WORKFLOWS_DIR):
        for file in files:
            if file == "workflow_api.json":
                workflow_api_files.append(os.path.join(root, file))

    if not workflow_api_files:
        print(f"No workflow_api.json files found in {WORKFLOWS_DIR}.")
    else:
        print(f"Found {len(workflow_api_files)} workflow_api.json files. Analyzing...")

    for model_path_key in model_usage.keys():
        # Extract the filename part from the model_path_key for searching
        # This assumes we are looking for the filename, e.g. "Eden_SDXL.safetensors"
        # rather than the full path like "models/checkpoints/Eden_SDXL.safetensors"
        # If the full path needs to be matched, this line should be:
        # search_string = model_path_key
        #
        # Based on the user's request "try and find string matches of these files",
        # it implies matching the file name or the full path.
        # Using the full path seems more robust to avoid ambiguous matches if
        # different models share the same filename but different paths.
        search_string = model_path_key

        for wf_api_file_path in workflow_api_files:
            try:
                with open(wf_api_file_path, 'r', encoding='utf-8') as f_wf:
                    workflow_content = f_wf.read()
                
                if search_string in workflow_content:
                    model_usage[model_path_key]["count"] += 1
                    # Get the parent directory of the workflow_api.json file
                    workflow_dir = os.path.basename(os.path.dirname(wf_api_file_path))
                    model_usage[model_path_key]["found_in_workflows"].add(workflow_dir)
            except FileNotFoundError:
                print(f"Warning: {wf_api_file_path} not found during analysis (should not happen).")
            except Exception as e:
                print(f"Warning: Could not read or process {wf_api_file_path}: {e}")


    print("\n--- Model Usage Summary ---")
    unused_models_count = 0
    for model_path, usage_data in model_usage.items():
        print(f"\nModel: {model_path}")
        print(f"  Referenced in: {usage_data['count']} workflow_api.json file(s)")
        if usage_data['count'] > 0:
            print(f"  Found in workflow directories: {', '.join(sorted(list(usage_data['found_in_workflows'])))}")
        else:
            print("  This model appears to be unused in any workflow_api.json.")
            unused_models_count += 1
    
    print(f"\n--- Summary ---")
    print(f"Total models in downloads.json: {len(downloads_data)}")
    print(f"Total workflow_api.json files found: {len(workflow_api_files)}")
    print(f"Number of potentially unused models: {unused_models_count}")

if __name__ == "__main__":
    analyze_model_usage() 