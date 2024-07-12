import os
import json

def update_workflow(original_workflow_path, updated_workflow_path, keys_to_update):
    with open(original_workflow_path, "r") as f:
        original_workflow = json.load(f)

    with open(updated_workflow_path, "r") as f:
        updated_workflow = json.load(f)

    for key in keys_to_update:
        print(f"--- Updating {key} ---")
        
        # Check if the key exists in both JSON structures
        if key in updated_workflow and key in original_workflow:
            if isinstance(updated_workflow[key], dict):
                for sub_key in updated_workflow[key]:
                    if sub_key in original_workflow[key] and original_workflow[key][sub_key] != updated_workflow[key][sub_key]:
                        original_workflow[key][sub_key] = updated_workflow[key][sub_key]
                        print(f"Updated {key}.{sub_key}")
            elif isinstance(updated_workflow[key], str):
                if original_workflow[key] != updated_workflow[key]:
                    original_workflow[key] = updated_workflow[key]
                    print(f"Updated {key}")
            elif isinstance(updated_workflow[key], list):
                # Example of updating list directly, you may want a more sophisticated merging depending on use case
                original_workflow[key] = updated_workflow[key]
                print(f"Updated {key} list")
            else:
                print(f"Skipped unsupported type for key {key}")
        else:
            print(f"Skipped {key} as it does not exist in both workflows")
        
    output_workflow_path = original_workflow_path.replace(".json", "_updated.json")
    with open(output_workflow_path, "w") as f:
        json.dump(original_workflow, f, indent=4)
    


if __name__ == "__main__":

    """
    Takes an up to date snapshot from a ComfyUI export and updates the original snapshot files with the new values where needed.
    This is often needed when you have a new version of ComfyUI / custom_nodes and the workflow has been altered accordingly.
    
    """

    original_snapshot_path = "img2vid_museV/snapshot.json"
    updated_snapshot_path  = "img2vid_museV/new_snapshot.json"


    keys_to_update = [
            "comfyui",
            "git_custom_nodes"
            ]
    
    update_workflow(original_workflow_path, updated_workflow_path, keys_to_update)