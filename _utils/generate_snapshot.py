import json
import os
import re
import sys
 
IGNORED_NODES = {"Note", "PrimitiveNode", "Reroute"}
 
 
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
 
 
def get_nodes_from_workflow_json_file(filepath):
    # Extract node types from a workflow JSON file.
 
    types = set()
 
    with open(filepath, "r") as file:
        data = json.load(file)
        nodes = data.get("nodes", [])
        for node in nodes:
            node_type = node.get("type")
            if node_type:
                types.add(node_type.strip())
 
    return list(types)
 
 
def compare_nodes(built_in_nodes, workflow_nodes):
    # Compare the built-in nodes with the nodes used in the workflow.
 
    workflow_nodes = [node for node in workflow_nodes if node not in IGNORED_NODES]
    missing_nodes = sorted(
        [
            workflow_node
            for workflow_node in workflow_nodes
            if workflow_node not in built_in_nodes
        ]
    )
    return missing_nodes
 
 
def load_extension_node_map(extension_node_map_path):
    # Load ComfyUI Manager `extension-node-map.json` file if it exists.
 
    if not os.path.exists(extension_node_map_path):
        print(
            "ComfyUI Manager is not installed. Install it to get additional custom node information."
        )
        return None
 
    with open(extension_node_map_path, "r") as file:
        extension_node_map = json.load(file)
 
    return extension_node_map
 
 
def find_node_in_extension_map(node_name, extension_node_map):
    # Find the URL corresponding to a node name in the `extension-node-map.json`.
 
    for url, (nodes, _) in extension_node_map.items():
        if node_name in nodes:
            return url
    return None
 
 
def process_workflow_json(file_path, built_in_nodes, extension_node_map):
    # Process a workflow JSON file, comparing its nodes with the built-in nodes and
    # optionally checking the `extension-node-map.json`.
 
    all_workflow_nodes = get_nodes_from_workflow_json_file(file_path)
    custom_nodes = compare_nodes(built_in_nodes, all_workflow_nodes)
    json_filename = os.path.basename(file_path)  # Get the filename from the path
    print(f"\nParsing {json_filename}...")

    github_urls = []
    custom_nodes_no_url = []

    if custom_nodes:
        for custom_node in custom_nodes:
            if extension_node_map:
                extension_url = find_node_in_extension_map(
                    custom_node, extension_node_map
                )
                if extension_url:
                    print(f"  {custom_node} --> {extension_url}")
                    github_urls.append(extension_url)
                else:
                    print(f"  {custom_node} --> NOT FOUND")
                    custom_nodes_no_url.append(custom_node)
            else:
                print(f"  {custom_node} --> NOT FOUND")
                custom_nodes_no_url.append(custom_node)
    else:
        print("  Workflow does not use custom nodes.")

    return set(github_urls), set(custom_nodes_no_url)
 
 
def process_workflow_dir(
    dir_path, built_in_nodes, extension_node_map, current_level=0, max_levels=2
):
    # Recursively process a directory of workflow JSON files.
 
    if current_level > max_levels:
        return
 
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' not found.")
        sys.exit(1)

    print("WARNING this function is not ready yet and only prints stuff!")
 
    for entry in os.listdir(dir_path):
        entry_path = os.path.join(dir_path, entry)
        if os.path.isfile(entry_path) and entry_path.endswith(".json"):
            github_urls, custom_nodes_no_url = process_workflow_json(entry_path, built_in_nodes, extension_node_map)
        elif os.path.isdir(entry_path):
            process_workflow_dir(
                entry_path, built_in_nodes, extension_node_map, current_level + 1
            )
 
import re
def strip_git_recursive(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            # Strip ".git" from keys
            new_key = re.sub(r'\.git$', '', key)
            
            # Recursively process the value
            new_value = strip_git_recursive(value)
            
            new_data[new_key] = new_value
        return new_data
    elif isinstance(data, list):
        # If it's a list, process each element recursively
        return [strip_git_recursive(item) for item in data]
    elif isinstance(data, str):
        # If it's a string, remove the ".git" suffix
        return re.sub(r'\.git$', '', data)
    else:
        # If it's neither a dict, list, or string, return the data as is
        return data
    


additional_node_url_mappings = {
    "Display Any (rgthree)": "https://github.com/rgthree/rgthree-comfy.git",
    "Image Comparer (rgthree)": "https://github.com/rgthree/rgthree-comfy.git",
    "Get resolution [Crystools]": "https://github.com/crystian/ComfyUI-Crystools",
    "Switch image [Crystools]": "https://github.com/crystian/ComfyUI-Crystools",
    "Get resolution [Crystools]": "https://github.com/crystian/ComfyUI-Crystools",
    "Load image with metadata [Crystools]": "https://github.com/crystian/ComfyUI-Crystools",
    "Context Big (rgthree)": "https://github.com/rgthree/rgthree-comfy.git",
    "Display Any (rgthree)": "https://github.com/rgthree/rgthree-comfy.git",
    "Switch any [Crystools]": "https://github.com/crystian/ComfyUI-Crystools",
    "InversionDemoLazySwitch": "https://github.com/BadCafeCode/execution-inversion-demo-comfyui",

    }




 
def main(comfyui_path=None, workflow_directory=None, master_snapshot_path = None):
    """
    Main function to orchestrate the processing of workflows and comparison of nodes.
 
    Args:
    - comfyui_path (str or None): The path to the ComfyUI root directory.
    - workflow_path (str or None): The path to the workflow JSON file or directory.
    """

    workflow_path = os.path.join(workflow_directory, "workflow_api.json")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    comfyui_path = comfyui_path if comfyui_path else script_dir
    workflow_dir_path = (
        workflow_path if workflow_path else os.path.join(script_dir, "workflows")
    )
 
    built_in_nodes = get_built_in_nodes(comfyui_path)
 
    extension_node_map_path = os.path.join(
        comfyui_path,
        "custom_nodes",
        "ComfyUI-Manager",
        "node_db",
        "new",
        "extension-node-map.json",
    )
    extension_node_map = load_extension_node_map(extension_node_map_path)
 
    if os.path.isfile(workflow_dir_path) and workflow_dir_path.endswith(".json"):
        print("Processing single workflow...")
        github_urls, custom_nodes_no_url = process_workflow_json(workflow_dir_path, built_in_nodes, extension_node_map)
    elif os.path.isdir(workflow_dir_path):
        print("Processing workflow dir...")
        process_workflow_dir(workflow_dir_path, built_in_nodes, extension_node_map)
    else:
        print(f"Error: Provided workflow path '{workflow_dir_path}' is invalid.")
        sys.exit(1)

    # Use additional_node_url_mappings to inject any final missing github_urls
    for node_name, url in additional_node_url_mappings.items():
        if node_name in custom_nodes_no_url:
            print(f"Also injecting {url} because of {node_name}")
            github_urls.add(url)
            custom_nodes_no_url.remove(node_name)

    github_urls = list(set(github_urls)) 
    github_urls = strip_git_recursive(github_urls)



    if len(custom_nodes_no_url) > 0:
        print(f"\n\n--- WARNING, custom nodes missing from snapshot url list:")
        for el in custom_nodes_no_url:
            print(f"--- {el}")

    # Now we get the hashes for each github url from the master_snapshot file:
    with open(master_snapshot_path, 'r') as f:
        master_snapshot = json.load(f)

    master_snapshot['git_custom_nodes'] = strip_git_recursive(master_snapshot['git_custom_nodes'])

    # Filter the git_custom_nodes based on the provided GitHub URLs
    filtered_nodes = {url: data for url, data in master_snapshot['git_custom_nodes'].items() if url in github_urls}
    
    # Create a new dictionary with the filtered data
    filtered_snapshot = {
        "comfyui": master_snapshot["comfyui"],
        "git_custom_nodes": filtered_nodes
    }
    
    # Save the filtered dictionary to disk
    output_path = os.path.join(workflow_directory, "auto_snapshot.json")
    with open(output_path, 'w') as f:
        json.dump(filtered_snapshot, f, indent=4)

    print(f"\nauto_snapshot.json saved to {output_path}")

if __name__ == '__main__':

    """
    Tries to automatically create snapshot.json from workflow.json and comfyui root dir
     - Make sure your comfy environment is active when running this!
     - Make sure your wf is called "workflow.json" inside of the workflow_directory

    Example:
cd /home/rednax/SSD2TB/Github_repos/Eden/workflows/_utils
python generate_snapshot.py /home/rednax/SSD2TB/Github_repos/ComfyUI /home/rednax/SSD2TB/Github_repos/Eden/workflows/workspaces/txt2img_new/workflows/storydiffusion

    """

    if len(sys.argv) != 3:
        print("Usage: python generate_snapshot.py <comfyui_root_dir> <workflow_directory>")
        sys.exit(1)
 
    comfyui_root_dir = sys.argv[1]
    workflow_directory = sys.argv[2]
    master_snapshot_path = "master_snapshot.json"
 
    main(comfyui_root_dir, workflow_directory, master_snapshot_path)