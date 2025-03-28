import json
import os
import glob
import argparse
from pathlib import Path
from typing import Dict, Any, Set, DefaultDict, Optional, List
from collections import defaultdict

def get_workflow_name(file_path: str) -> str:
    """Extract workflow name from file path (parent directory of the json file)."""
    return os.path.basename(os.path.dirname(file_path))

def normalize_path(path: str) -> str:
    """Normalize a path to use forward slashes and remove any leading/trailing slashes."""
    return path.replace('\\', '/').strip('/')

def collect_downloads(workspace_path: str, target_folders: Optional[List[str]] = None) -> tuple[Dict[str, str], DefaultDict[str, Set[str]], DefaultDict[str, Set[str]]]:
    """
    Collect all downloads from *download*.json files in the workspace and its subdirectories.
    Args:
        workspace_path: Root path to start scanning
        target_folders: Optional list of specific folders to scan. If None, scans all folders.
                       Folders can be specified with or without 'workspaces/' prefix.
    Returns:
        - merged dictionary of all downloads
        - dictionary mapping assets to their origin workflows
        - dictionary mapping assets to workflows where they are used
    """
    # Initialize the tracking dictionaries
    merged_downloads = {}
    asset_origins = defaultdict(set)  # Maps asset -> set of workflows where it was first defined
    asset_usage = defaultdict(set)    # Maps asset -> set of workflows where it appears
    
    # Find all *download*.json files recursively
    patterns = [
        os.path.join(workspace_path, "**", "downloads*.json"),
        os.path.join(workspace_path, "**", "auto_downloads*.json")
    ]
    download_files = []
    for pattern in patterns:
        download_files.extend(glob.glob(pattern, recursive=True))
    
    # Filter files if target folders specified
    if target_folders:
        filtered_files = []
        for file in download_files:
            file_dir = os.path.dirname(file)
            # Get the relative path from workspace_path
            rel_path = os.path.relpath(file_dir, workspace_path)
            # Check if any target folder is in the path
            if any(target in rel_path or target.replace('workspaces/', '') in rel_path for target in target_folders):
                filtered_files.append(file)
        download_files = filtered_files
    
    print(f"Found {len(download_files)} downloads files")
    
    # Process each downloads file
    for file_path in download_files:
        workflow = get_workflow_name(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                downloads = json.load(f)
                
            # Handle case where downloads is a string (URL)
            if isinstance(downloads, str):
                # We should never get here as downloads.json should always be a dictionary
                print(f"Warning: {file_path} contains a string instead of a dictionary")
                continue
                
            # Merge downloads, keeping the most complete information
            for path, info in downloads.items():
                # Get the target path - either from info dict or use the original path
                if isinstance(info, dict) and info.get("target"):
                    target_path = info["target"]
                else:
                    target_path = path
                    
                # Normalize the path
                normalized_path = normalize_path(target_path)
                
                # Handle case where info is a string (URL)
                if isinstance(info, str):
                    if normalized_path not in merged_downloads:
                        merged_downloads[normalized_path] = info
                        asset_origins[normalized_path].add(workflow)
                    asset_usage[normalized_path].add(workflow)
                else:
                    # If info is a dict, use the source URL
                    source = info.get("source")
                    if source:
                        if normalized_path not in merged_downloads:
                            merged_downloads[normalized_path] = source
                            asset_origins[normalized_path].add(workflow)
                        asset_usage[normalized_path].add(workflow)
                        
            print(f"Processed: {file_path}")
            
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    return merged_downloads, asset_origins, asset_usage

def generate_markdown_report(downloads: Dict[str, str], 
                           origins: DefaultDict[str, Set[str]], 
                           usage: DefaultDict[str, Set[str]], 
                           output_path: str,
                           new_library_entries: list = None):
    """Generate a detailed markdown report about the downloads."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Downloads Collection Report\n\n")
        
        # Summary statistics
        f.write("## Summary\n\n")
        f.write(f"- Total unique assets: {len(downloads)}\n")
        f.write(f"- Total unique workflows: {len(set().union(*origins.values()))}\n")
        if new_library_entries:
            f.write(f"- New entries added to download library: {len(new_library_entries)}\n")
        f.write("\n")
        
        # New library entries section
        if new_library_entries:
            f.write("## New Entries Added to Download Library\n\n")
            f.write("| Filename | Target Path | Source |\n")
            f.write("|----------|-------------|--------|\n")
            for entry in sorted(new_library_entries, key=lambda x: x["filename"]):
                f.write(f"| `{entry['filename']}` | `{entry['target']}` | {entry['source']} |\n")
            f.write("\n")
        
        # Assets by type
        f.write("## Assets by Type\n\n")
        asset_types = defaultdict(list)
        for path in downloads.keys():
            ext = os.path.splitext(path)[1].lower()
            asset_types[ext].append(path)
        
        for ext, assets in sorted(asset_types.items()):
            f.write(f"### {ext or 'No extension'}\n\n")
            f.write("| Asset | Origin Workflow | Used In | Source |\n")
            f.write("|-------|----------------|----------|--------|\n")
            for asset in sorted(assets):
                origin_str = ", ".join(sorted(origins[asset]))
                usage_str = ", ".join(sorted(usage[asset]))
                source = downloads[asset]
                f.write(f"| `{asset}` | {origin_str} | {usage_str} | {source} |\n")
            f.write("\n")
        
        # Workflows and their assets
        f.write("## Workflows and their Assets\n\n")
        workflows = set().union(*origins.values())
        for workflow in sorted(workflows):
            f.write(f"### {workflow}\n\n")
            f.write("| Asset | Is Origin | Source |\n")
            f.write("|-------|-----------|--------|\n")
            
            # Get all assets for this workflow
            workflow_assets = [asset for asset in downloads.keys() 
                             if workflow in usage[asset]]
            
            for asset in sorted(workflow_assets):
                is_origin = "Yes" if workflow in origins[asset] else "No"
                source = downloads[asset]
                f.write(f"| `{asset}` | {is_origin} | {source} |\n")
            f.write("\n")

def save_master_downloads(downloads: Dict[str, str], output_path: str):
    """
    Save the merged downloads to a master_downloads.json file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(downloads, f, indent=4, sort_keys=True)
        print(f"\nMaster downloads saved to: {output_path}")
        print(f"Total unique entries: {len(downloads)}")
    except Exception as e:
        print(f"Error saving master downloads: {str(e)}")

def update_download_library(merged_downloads: Dict[str, str], workspace_path: str) -> list:
    """
    Update download_library.json with any missing entries from merged_downloads.
    Preserves the existing structure and format of download_library.json.
    Returns a list of newly added entries.
    """
    library_path = os.path.join(os.path.dirname(__file__), "download_library.json")
    
    try:
        # Read existing library
        with open(library_path, 'r', encoding='utf-8') as f:
            library = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, create new structure
        library = {"files": {}, "nodes": {}}
    
    # Track which entries we've processed to avoid duplicates
    processed_entries = set()
    new_entries = []
    
    # Update files section
    for path, source in merged_downloads.items():
        # Skip if we've already processed this entry
        if path in processed_entries:
            continue
            
        # Get filename without path
        filename = os.path.basename(path)
        
        # Skip if already in library
        if filename in library["files"]:
            processed_entries.add(path)
            continue
            
        # Add new entry in the correct format
        library["files"][filename] = {
            "source": source,
            "target": path
        }
        new_entries.append({
            "filename": filename,
            "source": source,
            "target": path
        })
        processed_entries.add(path)
    
    # Save updated library
    try:
        with open(library_path, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=4, sort_keys=True)
        print(f"\nDownload library updated at: {library_path}")
        print(f"Total entries in library: {len(library['files'])}")
        print(f"New entries added: {len(new_entries)}")
    except Exception as e:
        print(f"Error saving download library: {str(e)}")
    
    return new_entries

def main():
    parser = argparse.ArgumentParser(description='Collect and manage downloads from workflow files.')
    parser.add_argument('--skip-library', action='store_true', 
                      help='Skip updating the download library')
    parser.add_argument('--skip-report', action='store_true',
                      help='Skip generating the markdown report')
    parser.add_argument('--folders', nargs='+', type=str,
                      help='Specific folders to scan (e.g., "flux sdxl" or "workspaces/flux workspaces/sdxl")')
    args = parser.parse_args()

    # Get the current directory as the workspace path
    current_dir = os.getcwd()
    
    # If we're in _utils, go up one level to get to the parent directory
    if os.path.basename(current_dir) == '_utils':
        workspace_path = os.path.dirname(current_dir)
        utils_dir = current_dir
    else:
        workspace_path = current_dir
        utils_dir = os.path.join(current_dir, '_utils')
    
    print(f"Scanning workspace: {workspace_path}")
    if args.folders:
        print(f"Target folders: {', '.join(args.folders)}")
    
    # Collect all downloads and their metadata
    merged_downloads, asset_origins, asset_usage = collect_downloads(workspace_path, args.folders)
    
    # Save the master downloads file in _utils directory
    output_path = os.path.join(utils_dir, "master_downloads.json")
    save_master_downloads(merged_downloads, output_path)
    
    # Update download library with any missing entries
    new_entries = []
    if not args.skip_library:
        new_entries = update_download_library(merged_downloads, workspace_path)
    
    # Generate the markdown report in _utils directory
    if not args.skip_report:
        report_path = os.path.join(utils_dir, "collect_downloads_report.md")
        generate_markdown_report(merged_downloads, asset_origins, asset_usage, report_path, new_entries)
        print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main() 