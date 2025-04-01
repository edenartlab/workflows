import json
import os
import re
import sys
import argparse
import shutil
from pathlib import Path
import urllib.request
import urllib.error

def scan_json_for_media(file_path, extensions):
    """
    Scan a JSON file for references to media files with specified extensions.
    Returns a dictionary of found media files.
    """
    media_files = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for file paths with the specified extensions
        for ext in extensions:
            # Find standalone filenames
            pattern = r'[\'"]([\w\-\.\/\\]+\.{})[\'"]'.format(ext)
            matches = re.findall(pattern, content)
            
            # Find URLs
            url_pattern = r'[\'"]?(https?://[^\s\'"]+\.{})[\'"]?'.format(ext)
            url_matches = re.findall(url_pattern, content)
            
            # Add all found media files to the dictionary
            for match in matches:
                if match not in media_files:
                    media_files[match] = {"source": None, "target": match}
            
            # Add all found URLs
            for url in url_matches:
                filename = url.split('/')[-1]
                if filename not in media_files:
                    media_files[filename] = {"source": url, "target": filename}
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    
    return media_files

def lookup_in_download_library(media_files, download_library):
    """
    Look up media files in the download library and update their source URLs if found.
    """
    library_files = download_library.get('files', {})
    library_nodes = download_library.get('nodes', {})
    
    # Check each media file against the download library
    for filename, info in media_files.items():
        # Skip files that already have a source URL
        if info["source"]:
            continue
        
        # Check if the file is in the download library
        if filename in library_files:
            media_files[filename]["source"] = library_files[filename]["source"]
            media_files[filename]["target"] = library_files[filename]["target"]
        
        # Check in node libraries
        for node, item_list in library_nodes.items():
            for item in item_list:
                if Path(item["target"]).name == filename:
                    media_files[filename]["source"] = item["source"]
                    media_files[filename]["target"] = item["target"]
                    break
    
    return media_files

def check_local_files(media_files, local_path):
    """
    Check if media files exist in the specified local path.
    """
    if not os.path.exists(local_path):
        return media_files
    
    for filename, info in media_files.items():
        local_file = os.path.join(local_path, filename)
        if os.path.exists(local_file):
            if not info["source"]:
                info["source"] = f"local:{local_file}"
    
    return media_files

def is_media_file(filename, extensions):
    """
    Check if a file is a media file based on its extension.
    """
    ext = filename.split('.')[-1].lower()
    return ext in extensions

def download_file(url, target_path):
    """
    Download a file from a URL to the target path.
    Returns True if successful, False otherwise.
    """
    try:
        print(f"Downloading {url} to {target_path}...")
        urllib.request.urlretrieve(url, target_path)
        return True
    except urllib.error.URLError as e:
        print(f"Error downloading {url}: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error downloading {url}: {str(e)}")
        return False

def copy_media_files(media_files, target_dir, download=True):
    """
    Copy media files to the target directory.
    If download is True, download files from URLs.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    
    copied_files = []
    for filename, info in media_files.items():
        source = info.get("source")
        
        # Skip files without a source
        if not source:
            continue
        
        target_path = os.path.join(target_dir, Path(filename).name)
        
        # Handle local files
        if source.startswith("local:"):
            local_path = source[6:]  # Remove 'local:' prefix
            try:
                shutil.copy2(local_path, target_path)
                copied_files.append((local_path, target_path))
                print(f"Copied {local_path} to {target_path}")
            except Exception as e:
                print(f"Error copying {local_path}: {str(e)}")
        
        # Handle URLs
        elif source.startswith("http") and download:
            if download_file(source, target_path):
                copied_files.append((source, target_path))
    
    return copied_files

def generate_downloads_report(workspace_path, media_files, copied_files):
    """
    Generate a markdown report for the downloads.
    """
    report_path = os.path.join(workspace_path, 'downloads_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        workspace_name = os.path.basename(workspace_path)
        f.write(f"# Downloads Report for {workspace_name}\n\n")
        f.write(f"Generated on: {Path(__file__).name} on {Path.cwd()}\n\n")
        
        # Summary statistics
        total_files = len(media_files)
        files_with_source = sum(1 for info in media_files.values() if info.get("source"))
        local_files = sum(1 for info in media_files.values() if info.get("source") and str(info.get("source")).startswith("local:"))
        url_files = sum(1 for info in media_files.values() if info.get("source") and str(info.get("source")).startswith("http"))
        missing_sources = sum(1 for info in media_files.values() if not info.get("source"))
        
        f.write("## Summary\n\n")
        f.write(f"- Total media files found: {total_files}\n")
        f.write(f"- Files with source URLs: {files_with_source}\n")
        f.write(f"- Files with local sources: {local_files}\n")
        f.write(f"- Files with remote URLs: {url_files}\n")
        f.write(f"- Files missing sources: {missing_sources}\n")
        f.write(f"- Files copied: {len(copied_files)}\n\n")
        
        # Categorize files
        remote_files = {k: v for k, v in media_files.items() if v.get("source") and str(v.get("source")).startswith("http")}
        local_files_dict = {k: v for k, v in media_files.items() if v.get("source") and str(v.get("source")).startswith("local:")}
        missing_files = {k: v for k, v in media_files.items() if not v.get("source")}
        
        # List all media files found
        f.write("## Media Files Found\n\n")
        if media_files:
            f.write("| Filename | Source | Target | Status |\n")
            f.write("|----------|--------|--------|--------|\n")
            
            for filename, info in sorted(media_files.items()):
                source = info.get("source", "Not found")
                target = info.get("target", filename)
                
                if not source:
                    status = "[MISSING] Missing source"
                elif str(source).startswith("local:"):
                    status = "[LOCAL] Local file"
                else:
                    status = "[REMOTE] Remote URL"
                    
                f.write(f"| {filename} | {source} | {target} | {status} |\n")
        else:
            f.write("No media files were found.\n")
        
        # Remote files section
        if remote_files:
            f.write("\n## Remote Files\n\n")
            f.write("| Filename | URL | Target |\n")
            f.write("|----------|-----|--------|\n")
            
            for filename, info in sorted(remote_files.items()):
                source = info.get("source")
                target = info.get("target", filename)
                f.write(f"| {filename} | {source} | {target} |\n")
        
        # Local files section
        if local_files_dict:
            f.write("\n## Local Files\n\n")
            f.write("| Filename | Path | Target |\n")
            f.write("|----------|------|--------|\n")
            
            for filename, info in sorted(local_files_dict.items()):
                source = info.get("source")
                if source.startswith("local:"):
                    source = source[6:]  # Remove 'local:' prefix
                target = info.get("target", filename)
                f.write(f"| {filename} | {source} | {target} |\n")
        
        # Missing files section
        if missing_files:
            f.write("\n## Missing Sources\n\n")
            f.write("| Filename | Target |\n")
            f.write("|----------|--------|\n")
            
            for filename, info in sorted(missing_files.items()):
                target = info.get("target", filename)
                f.write(f"| {filename} | {target} |\n")
            
            f.write("\n**Note:** These files need to be located or added to download_library.json.\n")
        
        # Files copied section
        f.write("\n## Files Copied\n\n")
        if copied_files:
            f.write("| Source | Target |\n")
            f.write("|--------|--------|\n")
            
            for source, target in copied_files:
                f.write(f"| {source} | {target} |\n")
        else:
            f.write("No files were copied.\n")
    
    print(f"Downloads report generated at {report_path}")

def filter_model_files(media_files):
    """
    Filter out model files from the media files dictionary.
    """
    non_model_files = {}
    model_targets = [
        'models/checkpoints', 
        'models/unet', 
        'models/vae', 
        'models/loras',
        'models/controlnet',
        'models/clip',
        'models/clip_vision',
        'models/style_models',
        'models/embeddings'
    ]
    
    for filename, info in media_files.items():
        target = info.get("target", "")
        
        # Check if it's a model file
        is_model = any(target.startswith(model_path) for model_path in model_targets)
        
        # If it's not a model, add it to the filtered list
        if not is_model:
            non_model_files[filename] = info
    
    return non_model_files

def process_workspace(workspace_path, download_library_path, local_path, target_dir, download=True):
    """
    Process a workspace directory, scanning all workflow and test JSON files for media.
    """
    # Check if the download library exists
    if not os.path.exists(download_library_path):
        print(f"Error: Download library not found at {download_library_path}")
        return

    # Load the download library
    with open(download_library_path, 'r') as f:
        download_library = json.load(f)

    # Extensions to look for
    media_extensions = ['pth', 'safetensors', 'jpg', 'jpeg', 'png', 'mov', 'mp4']
    
    # Dictionary to store all found media files
    all_media_files = {}
    
    # Track which files were found in which source files
    file_sources = {}
    
    # Walk through the workspace directory
    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            # Only process JSON files
            if not file.endswith('.json'):
                continue
                
            # Process workflow and test files
            if file in ['workflow.json', 'workflow_api.json'] or file.startswith('test'):
                file_path = os.path.join(root, file)
                media_files = scan_json_for_media(file_path, media_extensions)
                
                # Add to the global dictionary, avoiding duplicates
                for filename, info in media_files.items():
                    if filename not in all_media_files:
                        all_media_files[filename] = info
                        file_sources[filename] = [file_path]
                    else:
                        if info["source"] and not all_media_files[filename]["source"]:
                            all_media_files[filename]["source"] = info["source"]
                        if file_path not in file_sources[filename]:
                            file_sources[filename].append(file_path)

    # Look up files in the download library
    all_media_files = lookup_in_download_library(all_media_files, download_library)
    
    # Check if files exist locally
    all_media_files = check_local_files(all_media_files, local_path)
    
    # Filter out model files
    media_only_files = filter_model_files(all_media_files)
    
    # Save downloads.json
    downloads_path = os.path.join(workspace_path, 'downloads.json')
    with open(downloads_path, 'w') as f:
        json.dump(all_media_files, f, indent=4)
    
    print(f"Downloads JSON has been saved to {downloads_path}")
    
    # Copy media files (non-model files only)
    copied_files = copy_media_files(media_only_files, target_dir, download)
    
    # Generate downloads report
    generate_downloads_report(workspace_path, all_media_files, copied_files)
    
    return all_media_files, copied_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate downloads.json for a workspace and collect media assets')
    parser.add_argument('workspace_path', help='Path to the workspace directory')
    parser.add_argument('--library', default='download_library.json', help='Path to the download library file')
    parser.add_argument('--local_path', default='B:/AI/StabilityMatrix-win-x64/Data/Images/input', help='Path to check for local files')
    parser.add_argument('--target_dir', default='B:/AI/StabilityMatrix-win-x64/Data/Images/input/eden_test_assets', help='Path to copy media files to')
    parser.add_argument('--download', action='store_true', help='Download files from URLs')
    
    args = parser.parse_args()
    
    workspace_path = args.workspace_path
    download_library_path = args.library
    local_path = args.local_path
    target_dir = args.target_dir
    download = args.download
    
    if not os.path.exists(workspace_path):
        print(f"Error: Workspace directory not found at {workspace_path}")
        sys.exit(1)
    
    process_workspace(workspace_path, download_library_path, local_path, target_dir, download) 