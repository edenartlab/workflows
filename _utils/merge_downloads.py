import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

def extract_test_json_assets(file_path):
    """
    Extract image or video assets from test*.json files
    """
    assets = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Look for common patterns of downloadable assets in test files
        # This might need customization based on your test file structure
        if isinstance(data, dict):
            # Look for URLs in the test file that might be image or video assets
            asset_patterns = [
                r'https?://.*\.(png|jpg|jpeg|gif|webp|mp4|webm|mov)',
                r'https?://.*\b(image|img|video|media|asset)\b'
            ]
            
            def search_dict_for_assets(d, path=""):
                found_assets = {}
                for k, v in d.items():
                    current_path = f"{path}/{k}" if path else k
                    
                    if isinstance(v, str):
                        for pattern in asset_patterns:
                            if re.match(pattern, v, re.IGNORECASE):
                                # Use a reasonable filename based on the path or extract from URL
                                filename = v.split('/')[-1]
                                if '?' in filename:
                                    filename = filename.split('?')[0]
                                asset_path = f"input/{filename}"
                                found_assets[asset_path] = v
                    
                    elif isinstance(v, dict):
                        nested_assets = search_dict_for_assets(v, current_path)
                        found_assets.update(nested_assets)
                        
                    elif isinstance(v, list):
                        for i, item in enumerate(v):
                            if isinstance(item, dict):
                                nested_assets = search_dict_for_assets(item, f"{current_path}[{i}]")
                                found_assets.update(nested_assets)
                            elif isinstance(item, str):
                                for pattern in asset_patterns:
                                    if re.match(pattern, item, re.IGNORECASE):
                                        filename = item.split('/')[-1]
                                        if '?' in filename:
                                            filename = filename.split('?')[0]
                                        asset_path = f"input/{filename}"
                                        found_assets[asset_path] = item
                                        
                return found_assets
            
            assets = search_dict_for_assets(data)
                
    except Exception as e:
        print(f"Error processing test file {file_path}: {e}")
    
    return assets

def process_workspace(workspace_dir):
    """
    Process a workspace directory to find and merge download files
    """
    all_downloads = {}
    file_counts = defaultdict(int)
    workflow_stats = defaultdict(lambda: {'downloads': 0, 'auto_downloads': 0, 'test_files': 0, 'total_urls': 0})
    
    print(f"\n\033[1mProcessing workspace: {workspace_dir}\033[0m")
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(workspace_dir):
        relative_root = os.path.relpath(root, workspace_dir)
        parent_folder = relative_root.split(os.sep)[0] if relative_root != '.' else 'root'
        
        # Process regular downloads.json and auto_downloads.json files
        for filename in files:
            if filename == 'downloads.json':
                file_path = os.path.join(root, filename)
                print(f"  Found downloads.json in {relative_root}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        downloads = json.load(f)
                    
                    if isinstance(downloads, dict):
                        for target, url in downloads.items():
                            all_downloads[target] = url
                            file_counts['downloads.json'] += 1
                            workflow_stats[parent_folder]['downloads'] += 1
                            workflow_stats[parent_folder]['total_urls'] += 1
                            
                except Exception as e:
                    print(f"    \033[31mError processing {file_path}: {e}\033[0m")
            
            elif filename == 'auto_downloads.json':
                file_path = os.path.join(root, filename)
                print(f"  Found auto_downloads.json in {relative_root}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        downloads = json.load(f)
                    
                    if isinstance(downloads, dict):
                        for target, url in downloads.items():
                            all_downloads[target] = url
                            file_counts['auto_downloads.json'] += 1
                            workflow_stats[parent_folder]['auto_downloads'] += 1
                            workflow_stats[parent_folder]['total_urls'] += 1
                            
                except Exception as e:
                    print(f"    \033[31mError processing {file_path}: {e}\033[0m")
            
            # Process test*.json files
            elif filename.startswith('test') and filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                print(f"  Found test file {filename} in {relative_root}")
                
                try:
                    assets = extract_test_json_assets(file_path)
                    if assets:
                        print(f"    Extracted {len(assets)} assets from {filename}")
                        
                        for target, url in assets.items():
                            all_downloads[target] = url
                            file_counts[f'test_files'] += 1
                            workflow_stats[parent_folder]['test_files'] += 1
                            workflow_stats[parent_folder]['total_urls'] += 1
                            
                except Exception as e:
                    print(f"    \033[31mError processing {file_path}: {e}\033[0m")
    
    # Sort the downloads by their root folder
    sorted_downloads = {}
    
    # Get unique root folders and sort them
    root_folders = sorted(set(target.split('/')[0] for target in all_downloads.keys()))
    
    # Build sorted dictionary
    for folder in root_folders:
        # Get all items with this root folder
        folder_items = {k: v for k, v in all_downloads.items() if k.split('/')[0] == folder}
        # Sort by key and add to the result
        for k in sorted(folder_items.keys()):
            sorted_downloads[k] = folder_items[k]
    
    return sorted_downloads, file_counts, workflow_stats

def generate_report(file_counts, workflow_stats):
    """
    Generate a summary report of the processing using markdown formatting
    """
    print("\n" + "="*80)
    print("\033[1mSUMMARY REPORT\033[0m")
    print("="*80)
    
    # Files processed table in markdown format
    print("\n\033[1mFiles Processed:\033[0m")
    print("| File Type | Count |")
    print("|-----------|-------|")
    for file_type, count in file_counts.items():
        print(f"| {file_type} | {count} |")
    
    # Workflow statistics table in markdown format
    print("\n\033[1mWorkflow Statistics:\033[0m")
    print("| Workflow | Regular Downloads | Auto Downloads | Test File Assets | Total URLs |")
    print("|----------|-------------------|---------------|-----------------|------------|")
    for workflow, stats in sorted(workflow_stats.items()):
        print(f"| {workflow} | {stats['downloads']} | {stats['auto_downloads']} | {stats['test_files']} | {stats['total_urls']} |")
    
    total_urls = sum(stats["total_urls"] for stats in workflow_stats.values())
    print(f"\nTotal unique download URLs: {total_urls}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python merge_downloads.py <workspace_directory>")
        sys.exit(1)
    
    workspace_dir = sys.argv[1]
    if not os.path.isdir(workspace_dir):
        print(f"Error: {workspace_dir} is not a valid directory")
        sys.exit(1)
    
    downloads, file_counts, workflow_stats = process_workspace(workspace_dir)
    
    # Save the merged downloads
    output_path = os.path.join(workspace_dir, 'downloads_merged.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(downloads, f, indent=4)
    
    print(f"\n\033[1mMerged {len(downloads)} unique download URLs into {output_path}\033[0m")
    
    # Generate the report
    generate_report(file_counts, workflow_stats)

if __name__ == '__main__':
    main() 