#!/usr/bin/env python3
"""
Extract dependencies from ComfyUI workflows and generate a master snapshot.

This script:
1. Extracts dependencies from workflow.json files
2. Creates individual dependency files for each workflow
3. Generates a master snapshot file (master_snapshot.json)
4. Creates a detailed dependency report (workflow_dependencies_report.md)
5. Backs up previous dependency files with timestamps
6. Creates a changelog comparing current and previous dependencies

Usage:
    python _utils/extract_dependencies.py

Requirements:
    - ComfyUI-Manager installed with cm-cli.py available
    - Workflow files in ./workflows/
    - Dependencies stored in ./deps/
"""

import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
import re

# Configuration - all paths relative to the root directory
ROOT_DIR = os.path.abspath(os.path.curdir)  # Assumes the script is run from the root directory
WORKFLOWS_DIR = os.path.join(ROOT_DIR, "workflows")
DEPS_DIR = os.path.join(ROOT_DIR, "deps")
BACKUP_DIR = os.path.join(DEPS_DIR, "backup")
COMFYUI_DIR = os.path.join(ROOT_DIR, "ComfyUI")
CM_CLI_PATH = os.path.join(COMFYUI_DIR, "custom_nodes/ComfyUI-Manager/cm-cli.py")

# Preferred repository owners - will prioritize these forks when duplicates exist
PREFERRED_OWNERS = ["drmbt", "aiXander", "edenartlab"]

# Repository blacklist - these will never be included in the master snapshot
REPO_BLACKLIST = [
    "https://github.com/ClownsharkBatwing/RES4LYF",
    "https://github.com/807502278/ComfyUI-WJNodes"
]

# Create directories if they don't exist
for directory in [DEPS_DIR, BACKUP_DIR]:
    os.makedirs(directory, exist_ok=True)

def backup_existing_files():
    """Backup existing dependency files to a timestamped directory."""
    # Get timestamp for backup directory (YY-MM-DD format)
    date_str = datetime.now().strftime("%y-%m-%d")
    
    # Check if backup directories for today already exist
    existing_backups = [d for d in os.listdir(BACKUP_DIR) if d.startswith(date_str)]
    
    # If there are existing backups, append a number
    if existing_backups:
        suffix = len(existing_backups)
        backup_dir_name = f"{date_str}_{suffix}"
    else:
        backup_dir_name = f"{date_str}_0"
    
    backup_subdir = os.path.join(BACKUP_DIR, backup_dir_name)
    os.makedirs(backup_subdir, exist_ok=True)
    
    # Copy individual workflow dependency files
    dep_files = [f for f in os.listdir(DEPS_DIR) if f.endswith("_deps.json")]
    for file in dep_files:
        src = os.path.join(DEPS_DIR, file)
        dst = os.path.join(backup_subdir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    # Copy report file if it exists
    report_src = os.path.join(DEPS_DIR, "dependencies_report.md")
    report_dst = os.path.join(backup_subdir, "dependencies_report.md")
    if os.path.exists(report_src):
        shutil.copy2(report_src, report_dst)
    
    print(f"Backed up existing dependency files to {backup_subdir}")
    return backup_subdir, backup_dir_name

def extract_workflow_dependencies(workflow_path, deps_file):
    """
    Extract dependencies from a workflow file using ComfyUI-Manager's cm-cli.py.
    
    Args:
        workflow_path: Path to the workflow.json file
        deps_file: Path where the dependencies should be saved
    
    Returns:
        Dictionary of dependencies
    """
    try:
        # The command format for cm-cli.py is 'deps-in-workflow --workflow <path> --output <output_path>'
        subprocess.run(
            ["python", CM_CLI_PATH, "deps-in-workflow", "--workflow", workflow_path, "--output", deps_file],
            capture_output=True, 
            text=True,
            check=True
        )
        
        # Read the generated deps file
        with open(deps_file, 'r') as f:
            dependencies = json.load(f)
        return dependencies
    except subprocess.CalledProcessError as e:
        print(f"Error extracting dependencies from {workflow_path}: {e}")
        print(f"stderr: {e.stderr}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing dependencies JSON from {deps_file}: {e}")
        return {}

def process_workflows():
    """Process all workflow files and extract dependencies."""
    all_dependencies = {}
    workflow_deps = {}
    workflow_files = []
    
    # Only look for workflow.json files directly in immediate subdirectories
    for item in os.listdir(WORKFLOWS_DIR):
        subdir_path = os.path.join(WORKFLOWS_DIR, item)
        if os.path.isdir(subdir_path):
            workflow_file = os.path.join(subdir_path, "workflow.json")
            if os.path.isfile(workflow_file):
                # Use the directory name as the workflow name
                workflow_name = item
                workflow_files.append((workflow_name, workflow_file))
    
    if not workflow_files:
        print(f"No workflow.json files found in {WORKFLOWS_DIR} subdirectories")
        return all_dependencies, workflow_deps
    
    print(f"Found {len(workflow_files)} workflow.json files")
    
    for workflow_name, workflow_path in workflow_files:
        print(f"Extracting dependencies from {workflow_name}/workflow.json...")
        
        # Define output file path
        deps_file = os.path.join(DEPS_DIR, f"{workflow_name}_deps.json")
        
        # Extract dependencies directly to the deps file
        dependencies = extract_workflow_dependencies(workflow_path, deps_file)
        
        # Store the dependency information
        all_dependencies[workflow_name] = dependencies
        
        # Build the workflow_deps dictionary for repository -> workflows mapping
        if "custom_nodes" in dependencies:
            for repo_url in dependencies["custom_nodes"]:
                if repo_url not in workflow_deps:
                    workflow_deps[repo_url] = []
                workflow_deps[repo_url].append(workflow_name)
    
    return all_dependencies, workflow_deps

def load_existing_snapshot():
    """Load the existing snapshot.json file."""
    snapshot_path = os.path.join(ROOT_DIR, "snapshot.json")
    if os.path.exists(snapshot_path):
        try:
            with open(snapshot_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error parsing existing snapshot.json, ignoring it")
    return None

def extract_owner_from_url(url):
    """Extract the owner from a GitHub repository URL."""
    match = re.search(r"github\.com/([^/]+)/", url)
    if match:
        return match.group(1)
    return None

def extract_repo_name_from_url(url):
    """Extract the repository name from a GitHub repository URL."""
    match = re.search(r"github\.com/[^/]+/([^/]+)", url)
    if match:
        return match.group(1)
    return None

def normalize_url(url):
    """
    Normalize a URL for fuzzy matching by converting to lowercase and removing dashes/underscores.
    """
    return url.lower().replace("-", "").replace("_", "").replace(" ", "")

def find_matching_repo_hash(repo_url, existing_snapshot):
    """
    Find a matching repository hash from the existing snapshot using fuzzy matching.
    
    Args:
        repo_url: The repository URL to look up
        existing_snapshot: The existing snapshot.json data
        
    Returns:
        The hash value if found, otherwise "-"
    """
    if not existing_snapshot or "git_custom_nodes" not in existing_snapshot:
        return "-"
    
    # Normalize the target URL
    normalized_repo = normalize_url(repo_url)
    
    # First try exact match
    if repo_url in existing_snapshot["git_custom_nodes"]:
        return existing_snapshot["git_custom_nodes"][repo_url].get("hash", "-")
    
    # Try fuzzy match
    for existing_url in existing_snapshot["git_custom_nodes"]:
        normalized_existing = normalize_url(existing_url)
        if normalized_repo == normalized_existing:
            return existing_snapshot["git_custom_nodes"][existing_url].get("hash", "-")
    
    # No match found
    return "-"

def generate_master_snapshot(all_dependencies, existing_snapshot):
    """
    Generate a master snapshot from all workflow dependencies,
    preserving the structure from the existing snapshot.json if available.
    """
    # Initialize with snapshot structure if available, otherwise create new
    if existing_snapshot:
        # Create a copy of existing snapshot but only include the keys we want to preserve
        master_snapshot = {}
        
        # Copy over the comfyui hash
        if "comfyui" in existing_snapshot:
            master_snapshot["comfyui"] = existing_snapshot["comfyui"]
        
        # Initialize git_custom_nodes for our workflow dependencies
        master_snapshot["git_custom_nodes"] = {}
        
        # Preserve pips section exactly as it appears in snapshot.json
        if "pips" in existing_snapshot:
            master_snapshot["pips"] = existing_snapshot["pips"]
            
        # Copy other important sections
        for key in ["file_custom_nodes", "cnr_custom_nodes"]:
            if key in existing_snapshot:
                master_snapshot[key] = existing_snapshot[key]
    else:
        master_snapshot = {
            "comfyui": "",
            "git_custom_nodes": {},
            "pips": {},
            "file_custom_nodes": [],
            "cnr_custom_nodes": []
        }
    
    # First build a map of all workflows to their dependencies
    workflow_to_deps = {}
    for workflow_name, deps in all_dependencies.items():
        if "custom_nodes" in deps:
            workflow_to_deps[workflow_name] = list(deps["custom_nodes"].keys())
    
    # Track all repositories and their associated info
    repo_info_map = {}
    
    # Group repositories by name (ignoring owner) to detect forks
    repos_by_name = defaultdict(list)
    
    # Process all dependencies from all workflows
    for workflow_name, deps in all_dependencies.items():
        if "custom_nodes" in deps:
            for repo_url, info in deps["custom_nodes"].items():
                # Skip blacklisted repositories
                if repo_url in REPO_BLACKLIST:
                    continue
                
                # Store repo info for later use
                if repo_url not in repo_info_map:
                    # Look up the hash from existing snapshot first using fuzzy matching
                    if not info.get("hash") or info.get("hash") == "-":
                        info["hash"] = find_matching_repo_hash(repo_url, existing_snapshot)
                    repo_info_map[repo_url] = info
                
                # Group by repo name for fork detection
                repo_name = extract_repo_name_from_url(repo_url)
                owner = extract_owner_from_url(repo_url)
                if repo_name and owner:
                    repos_by_name[repo_name].append((repo_url, owner))
    
    # If existing snapshot exists, also check for repositories from preferred owners that 
    # aren't in any workflow but are in the snapshot
    if existing_snapshot and "git_custom_nodes" in existing_snapshot:
        for repo_url in existing_snapshot["git_custom_nodes"]:
            owner = extract_owner_from_url(repo_url)
            # Only process if from preferred owner and not already accounted for
            if owner in PREFERRED_OWNERS and repo_url not in repo_info_map:
                repo_name = extract_repo_name_from_url(repo_url)
                if repo_name:
                    info = existing_snapshot["git_custom_nodes"][repo_url]
                    repo_info_map[repo_url] = info
                    repos_by_name[repo_name].append((repo_url, owner))
            
    # Initialize the git_custom_nodes dictionary
    git_custom_nodes = {}
    preferred_repos = []
    
    # Handle repository selection for forks
    for repo_name, repo_info_list in repos_by_name.items():
        # Make sure repo_info_list contains tuples of (url, owner)
        # Some might have been appended as just urls, so convert those
        normalized_repo_info = []
        for item in repo_info_list:
            if isinstance(item, tuple):
                normalized_repo_info.append(item)
            else:
                # Item is just a URL
                owner = extract_owner_from_url(item)
                normalized_repo_info.append((item, owner))
        
        # Sort by preferred owners
        def get_owner_preference(repo_info):
            _, owner = repo_info
            if owner in PREFERRED_OWNERS:
                return PREFERRED_OWNERS.index(owner)
            return float('inf')  # Non-preferred owners go last
        
        # Sort by preferred owners
        sorted_repos = sorted(normalized_repo_info, key=get_owner_preference)
        
        # Select the repository from the most preferred owner
        selected_repo_url, selected_owner = sorted_repos[0]
        is_preferred = selected_owner in PREFERRED_OWNERS
        
        # Get the hash from repo_info_map or existing_snapshot
        hash_value = "-"
        if selected_repo_url in repo_info_map:
            hash_info = repo_info_map[selected_repo_url]
            if isinstance(hash_info, dict) and "hash" in hash_info:
                hash_value = hash_info["hash"]
        elif existing_snapshot and "git_custom_nodes" in existing_snapshot and selected_repo_url in existing_snapshot["git_custom_nodes"]:
            hash_value = existing_snapshot["git_custom_nodes"][selected_repo_url].get("hash", "-")
        
        # Add to git_custom_nodes
        git_custom_nodes[selected_repo_url] = {
            "hash": hash_value,
            "disabled": False
        }
        
        # Add to preferred_repos list if from a preferred owner
        if is_preferred:
            preferred_repos.append((selected_repo_url, selected_owner, repo_name))
    
    # Update the master snapshot with our git_custom_nodes
    master_snapshot["git_custom_nodes"] = git_custom_nodes
    
    # Write the master snapshot to file, matching the indentation style of snapshot.json (4 spaces)
    master_path = os.path.join(ROOT_DIR, "master_snapshot.json")
    with open(master_path, "w") as f:
        json.dump(master_snapshot, f, indent=4)
    
    print(f"Generated master snapshot: {master_path}")
    return master_snapshot, preferred_repos

def generate_report(all_dependencies, workflow_deps, master_snapshot, preferred_repos, existing_snapshot, backup_timestamp):
    """Generate a detailed report of workflow dependencies."""
    report_path = os.path.join(DEPS_DIR, "dependencies_report.md")
    
    # Count how many workflows use each dependency
    usage_counts = {repo: len(workflows) for repo, workflows in workflow_deps.items()}
    
    # Identify common and singleton packages
    common_packages = {repo: workflows for repo, workflows in workflow_deps.items() if len(workflows) > 1}
    singleton_packages = {repo: workflows[0] for repo, workflows in workflow_deps.items() if len(workflows) == 1}
    
    # Get hash information by looking up in master_snapshot first, then falling back to fuzzy match in existing_snapshot
    repo_hashes = {}
    for repo_url in workflow_deps:
        # First check if it's in the master_snapshot we just created
        if "git_custom_nodes" in master_snapshot and repo_url in master_snapshot["git_custom_nodes"]:
            repo_hashes[repo_url] = master_snapshot["git_custom_nodes"][repo_url].get("hash", "-")
        else:
            # If not found, use the fuzzy matching function
            repo_hashes[repo_url] = find_matching_repo_hash(repo_url, existing_snapshot)
    
    # Find any repos in the existing snapshot that aren't in any workflow
    unused_packages = []
    if existing_snapshot and "git_custom_nodes" in existing_snapshot:
        existing_repos = list(existing_snapshot["git_custom_nodes"].keys())
        unused_packages = [repo for repo in existing_repos if repo not in workflow_deps]
    
    # Find any missing repos that are in workflows but not in the snapshot
    missing_packages = []
    if existing_snapshot and "git_custom_nodes" in existing_snapshot:
        # First create a map of normalized URLs for fuzzy matching
        normalized_map = {normalize_url(url): url for url in existing_snapshot["git_custom_nodes"]}
        
        for repo_url in workflow_deps:
            # Check for exact match
            if repo_url in existing_snapshot["git_custom_nodes"]:
                continue
                
            # Check for fuzzy match
            normalized = normalize_url(repo_url)
            if normalized not in normalized_map:
                missing_packages.append(repo_url)
    
    # Get repository fork information - group by repo name
    repos_by_name = defaultdict(list)
    for repo_url in workflow_deps:
        repo_name = extract_repo_name_from_url(repo_url)
        owner = extract_owner_from_url(repo_url)
        if repo_name and owner:
            repos_by_name[repo_name].append((repo_url, owner))
            
    # Add any repositories from the existing snapshot that might not be in workflows
    if existing_snapshot and "git_custom_nodes" in existing_snapshot:
        for repo_url in existing_snapshot["git_custom_nodes"]:
            if repo_url not in workflow_deps:
                repo_name = extract_repo_name_from_url(repo_url)
                owner = extract_owner_from_url(repo_url)
                if repo_name and owner:
                    repos_by_name[repo_name].append((repo_url, owner))
    
    # Identify forked repositories (where multiple repos have the same name)
    forked_repos = {name: repos for name, repos in repos_by_name.items() if len(repos) > 1}
    
    # Get ComfyUI hash
    comfyui_hash = master_snapshot.get("comfyui", "-")
    
    with open(report_path, "w") as f:
        f.write("# ComfyUI Dependencies Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary statistics
        f.write("## Summary\n")
        # Calculate total unique workflows
        total_workflows = set()
        for workflows_list in workflow_deps.values():
            total_workflows.update(workflows_list)
        
        f.write(f"- ComfyUI Hash: `{comfyui_hash}`\n")
        f.write(f"- Total Repositories: {len(workflow_deps)}\n")
        f.write(f"- Workflows analyzed: {len(total_workflows)}\n")
        f.write(f"- Preferred Owners: {', '.join(PREFERRED_OWNERS)}\n")
        
        # Add information about blacklisted repositories
        blacklisted_repos_found = [repo for repo in REPO_BLACKLIST if repo in workflow_deps]
        if blacklisted_repos_found:
            f.write(f"- Blacklisted Repositories: {len(blacklisted_repos_found)}\n")
        f.write("\n")
        
        # Repository Dependency Analysis
        f.write("## Repository Dependency Analysis\n\n")
        
        # Common Packages Section
        if common_packages:
            f.write("### Common Packages (used by multiple workflows)\n")
            f.write("| Repository | Count | Workflows | Hash | Status |\n")
            f.write("|------------|-------|-----------|------|--------|\n")
            
            # Sort by usage count (descending)
            sorted_common = sorted(common_packages.items(), key=lambda x: len(x[1]), reverse=True)
            for repo, workflows in sorted_common:
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                is_preferred = owner in PREFERRED_OWNERS
                preferred_tag = " (PREFERRED)" if is_preferred else ""
                hash_value = repo_hashes.get(repo, "-")
                workflow_count = len(workflows)
                
                # Format workflows as a comma-separated list
                workflow_list = ", ".join(sorted(workflows))
                
                # Check if blacklisted
                status = "BLACKLISTED" if repo in REPO_BLACKLIST else ""
                
                f.write(f"| [{repo_name}]({repo}) | {workflow_count} | {workflow_list} | `{hash_value}` | {status} |\n")
            f.write("\n")
        
        # Singleton Packages
        if singleton_packages:
            f.write("### Singleton Packages (used by only one workflow)\n")
            f.write("| Repository | Workflow | Hash | Status |\n")
            f.write("|------------|-----------|------|--------|\n")
            
            # Sort by repository name
            for repo, workflow in sorted(singleton_packages.items(), key=lambda x: extract_repo_name_from_url(x[0]).lower()):
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                hash_value = repo_hashes.get(repo, "-")
                
                # Check if blacklisted
                status = "BLACKLISTED" if repo in REPO_BLACKLIST else ""
                
                f.write(f"| [{repo_name}]({repo}) | {workflow} | `{hash_value}` | {status} |\n")
            f.write("\n")
        
        # Forked Repositories
        if forked_repos:
            f.write("### Forked Repositories (multiple versions)\n")
            f.write("| Repository | Owner | Selected | Count | Workflows | Status |\n")
            f.write("|------------|-------|----------|-------|-----------|--------|\n")
            
            for repo_name, repos in sorted(forked_repos.items()):
                # Sort by preferred owners first
                def get_owner_preference(repo_info):
                    repo_url, owner = repo_info
                    if owner in PREFERRED_OWNERS:
                        return PREFERRED_OWNERS.index(owner)
                    return float('inf')
                
                sorted_repos = sorted(repos, key=get_owner_preference)
                
                # Group by repository name
                for i, (repo_url, owner) in enumerate(sorted_repos):
                    workflows = workflow_deps.get(repo_url, [])
                    is_preferred = owner in PREFERRED_OWNERS
                    is_blacklisted = repo_url in REPO_BLACKLIST
                    is_selected = repo_url in master_snapshot.get("git_custom_nodes", {})
                    
                    # Format the "Selected" column
                    selected = "✓" if is_selected else ""
                    preferred = " (PREFERRED)" if is_preferred else ""
                    
                    # Count and format workflows
                    count = len(workflows)
                    workflow_str = ", ".join(sorted(workflows)) if workflows else "None"
                    
                    # Status column
                    status = "BLACKLISTED" if is_blacklisted else ""
                    
                    f.write(f"| {repo_name if i == 0 else ''} | [{owner}]({repo_url}){preferred} | {selected} | {count} | {workflow_str} | {status} |\n")
            f.write("\n")
        
        # Blacklisted Repositories
        if blacklisted_repos_found:
            f.write("### Blacklisted Repositories (excluded from snapshot)\n")
            f.write("| Repository | Owner | Count | Workflows |\n")
            f.write("|------------|-------|-------|----------|\n")
            
            for repo in sorted(blacklisted_repos_found, key=lambda x: extract_repo_name_from_url(x).lower()):
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                workflows = workflow_deps.get(repo, [])
                count = len(workflows)
                workflow_str = ", ".join(sorted(workflows)) if workflows else "None"
                
                f.write(f"| [{repo_name}]({repo}) | {owner} | {count} | {workflow_str} |\n")
            f.write("\n")
        
        # Missing & Unused Packages
        if missing_packages or unused_packages:
            f.write("## Package Status\n\n")
            
            # Missing Packages
            if missing_packages:
                f.write("### Missing Packages (in workflows but not in snapshot)\n")
                f.write("| Repository | Owner | Workflows | Status |\n")
                f.write("|------------|-------|-----------|--------|\n")
                
                for repo in sorted(missing_packages, key=lambda x: extract_repo_name_from_url(x).lower()):
                    owner = extract_owner_from_url(repo)
                    repo_name = extract_repo_name_from_url(repo)
                    workflows = workflow_deps.get(repo, [])
                    
                    # Format workflows
                    workflow_str = ", ".join(sorted(workflows)) if workflows else "None"
                    
                    # Check if blacklisted
                    status = "BLACKLISTED" if repo in REPO_BLACKLIST else ""
                    
                    f.write(f"| [{repo_name}]({repo}) | {owner} | {workflow_str} | {status} |\n")
                f.write("\n")
            
            # Unused Packages
            if unused_packages:
                f.write("### Unused Packages (in snapshot but not in workflows)\n")
                f.write("| Repository | Owner | Hash | Status |\n")
                f.write("|------------|-------|------|--------|\n")
                
                for repo in sorted(unused_packages, key=lambda x: extract_repo_name_from_url(x).lower()):
                    owner = extract_owner_from_url(repo)
                    repo_name = extract_repo_name_from_url(repo)
                    is_preferred = owner in PREFERRED_OWNERS
                    preferred_tag = " (PREFERRED)" if is_preferred else ""
                    from_preferred_owner = owner in PREFERRED_OWNERS
                    owner_note = " (from preferred owner)" if from_preferred_owner else ""
                    hash_value = repo_hashes.get(repo, "-")
                    
                    # Check if blacklisted
                    status = "BLACKLISTED" if repo in REPO_BLACKLIST else ""
                    
                    f.write(f"| [{repo_name}]({repo}) | {owner}{preferred_tag} | `{hash_value}`{owner_note} | {status} |\n")
                f.write("\n")
                
        # Per-Workflow Dependencies
        f.write("## Per-Workflow Dependencies\n\n")
        workflows = set()
        for wf_list in workflow_deps.values():
            workflows.update(wf_list)
        
        for workflow in sorted(workflows):
            f.write(f"### {workflow}\n")
            f.write("| Repository | Owner | Hash | Status |\n")
            f.write("|------------|-------|------|--------|\n")
            workflow_repos = [repo for repo, wfs in workflow_deps.items() if workflow in wfs]
            for repo in sorted(workflow_repos, key=lambda x: extract_repo_name_from_url(x).lower()):
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                is_preferred = owner in PREFERRED_OWNERS
                preferred_tag = " (PREFERRED)" if is_preferred else ""
                hash_value = repo_hashes.get(repo, "-")
                
                # Check if blacklisted
                status = "BLACKLISTED" if repo in REPO_BLACKLIST else ""
                
                f.write(f"| [{repo_name}]({repo}) | {owner}{preferred_tag} | `{hash_value}` | {status} |\n")
            f.write("\n")
    
    print(f"Generated dependency report: {report_path}")
    return report_path

def generate_changelog(backup_dir, all_dependencies, master_snapshot, preferred_repos, backup_timestamp):
    """Generate a changelog comparing current and previous dependencies."""
    # Try to find previous dependencies in the backup directory
    prev_deps_files = [f for f in os.listdir(backup_dir) if f.endswith("_deps.json")]
    if not prev_deps_files:
        print("No previous dependency files found in backup, skipping changelog generation")
        return
    
    # Load current master snapshot git_custom_nodes
    current_custom_nodes = {url: info for url, info in master_snapshot.get("git_custom_nodes", {}).items()}
    
    # Find a previous snapshot.json in the backup
    prev_snapshot_path = os.path.join(backup_dir, "snapshot.json")
    prev_custom_nodes = {}
    if os.path.exists(prev_snapshot_path):
        try:
            with open(prev_snapshot_path, "r") as f:
                prev_snapshot = json.load(f)
                prev_custom_nodes = {url: info for url, info in prev_snapshot.get("git_custom_nodes", {}).items()}
        except:
            print("Error loading previous snapshot.json, will compare with backup dependency files")
    
    # If no previous snapshot, build from individual dependency files
    if not prev_custom_nodes:
        for dep_file in prev_deps_files:
            try:
                with open(os.path.join(backup_dir, dep_file), "r") as f:
                    deps = json.load(f)
                    if "custom_nodes" in deps:
                        for url, info in deps["custom_nodes"].items():
                            prev_custom_nodes[url] = info
            except:
                print(f"Error loading {dep_file}, skipping")
    
    # Identify added and removed repositories
    added_repos = [url for url in current_custom_nodes if url not in prev_custom_nodes]
    removed_repos = [url for url in prev_custom_nodes if url not in current_custom_nodes]
    
    # Generate changelog
    changelog_path = os.path.join(backup_dir, "dependencies_changelog.md")
    with open(changelog_path, "w") as f:
        f.write("# ComfyUI Workflow Dependencies Changelog\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Comparing current dependencies with backup from {backup_timestamp}\n\n")
        f.write(f"Preferred Owners: {', '.join(PREFERRED_OWNERS)}\n\n")
        
        if not added_repos and not removed_repos:
            f.write("No changes detected in dependencies.\n")
            return changelog_path
        
        # Added repositories
        if added_repos:
            f.write("## Added Repositories\n\n")
            for repo in added_repos:
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                is_preferred = owner in PREFERRED_OWNERS
                preferred_tag = " (PREFERRED)" if is_preferred else ""
                
                # Find which workflows use this new repository
                workflows_using = []
                for workflow_name, deps in all_dependencies.items():
                    if "custom_nodes" in deps and repo in deps["custom_nodes"]:
                        workflows_using.append(workflow_name)
                
                f.write(f"- {repo_name} ({owner}{preferred_tag}): {repo}\n")
                if workflows_using:
                    f.write(f"  - Used by: {', '.join(workflows_using)}\n")
            f.write("\n")
        
        # Removed repositories
        if removed_repos:
            f.write("## Removed Repositories\n\n")
            for repo in removed_repos:
                owner = extract_owner_from_url(repo)
                repo_name = extract_repo_name_from_url(repo)
                is_blacklisted = repo in REPO_BLACKLIST
                blacklist_tag = " (BLACKLISTED)" if is_blacklisted else ""
                
                f.write(f"- {repo_name} ({owner}){blacklist_tag}: {repo}\n")
            f.write("\n")
        
        # Preferred repositories
        if preferred_repos:
            f.write("## Preferred Repositories\n\n")
            f.write("These repositories are from preferred owners and are prioritized:\n\n")
            for repo_url, owner, repo_name in preferred_repos:
                is_new = repo_url in added_repos
                new_tag = " (NEW)" if is_new else ""
                
                # Find which workflows use this preferred repository
                workflows_using = []
                for workflow_name, deps in all_dependencies.items():
                    if "custom_nodes" in deps and repo_url in deps["custom_nodes"]:
                        workflows_using.append(workflow_name)
                        
                f.write(f"- {repo_name} ({owner}){new_tag}: {repo_url}\n")
                workflow_count = len(workflows_using)
                if workflows_using:
                    f.write(f"  - Used by {workflow_count} workflow(s): {', '.join(sorted(workflows_using))}\n")
                else:
                    f.write(f"  - Not used by any workflow (from preferred owner)\n")
            f.write("\n")
            
        # Blacklisted repositories
        blacklisted_in_workflows = []
        for workflow_name, deps in all_dependencies.items():
            if "custom_nodes" in deps:
                for repo_url in deps["custom_nodes"]:
                    if repo_url in REPO_BLACKLIST and repo_url not in blacklisted_in_workflows:
                        blacklisted_in_workflows.append(repo_url)
        
        if blacklisted_in_workflows:
            f.write("## Blacklisted Repositories\n\n")
            f.write("These repositories are blacklisted and excluded from the master snapshot:\n\n")
            for repo_url in blacklisted_in_workflows:
                owner = extract_owner_from_url(repo_url)
                repo_name = extract_repo_name_from_url(repo_url)
                
                # Find which workflows use this blacklisted repository
                workflows_using = []
                for workflow_name, deps in all_dependencies.items():
                    if "custom_nodes" in deps and repo_url in deps["custom_nodes"]:
                        workflows_using.append(workflow_name)
                        
                f.write(f"- {repo_name} ({owner}): {repo_url}\n")
                workflow_count = len(workflows_using)
                if workflows_using:
                    f.write(f"  - Used by {workflow_count} workflow(s): {', '.join(sorted(workflows_using))}\n")
            f.write("\n")
    
    print(f"Generated dependency changelog: {changelog_path}")
    return changelog_path

def main():
    """Main function to extract dependencies and generate reports."""
    print("Starting ComfyUI workflow dependency extraction...")
    
    # Check if ComfyUI-Manager is installed
    if not os.path.exists(CM_CLI_PATH):
        print(f"Error: ComfyUI-Manager not found at {CM_CLI_PATH}")
        print("Please install ComfyUI-Manager first")
        sys.exit(1)
    
    # Backup existing dependency files
    backup_dir, backup_timestamp = backup_existing_files()
    
    # Process workflows and extract dependencies
    all_dependencies, workflow_deps = process_workflows()
    if not all_dependencies:
        print("No dependencies found in workflows")
        sys.exit(1)
    
    # Load existing snapshot.json
    existing_snapshot = load_existing_snapshot()
    
    # Generate master snapshot
    master_snapshot, preferred_repos = generate_master_snapshot(all_dependencies, existing_snapshot)
    
    # Generate dependency report
    report_path = generate_report(all_dependencies, workflow_deps, master_snapshot, preferred_repos, existing_snapshot, backup_timestamp)
    
    # Generate changelog
    changelog_path = generate_changelog(backup_dir, all_dependencies, master_snapshot, preferred_repos, backup_timestamp)
    
    print("\nSummary:")
    # Calculate unique workflows
    unique_workflows = set()
    for workflows in workflow_deps.values():
        unique_workflows.update(workflows)
        
    print(f"- Processed {len(unique_workflows)} workflows")
    print(f"- Found {len(workflow_deps)} unique repositories")
    print(f"- Identified {len(preferred_repos)} preferred repositories")
    
    # Count blacklisted repositories
    blacklisted_repos_found = [repo for repo in REPO_BLACKLIST if repo in workflow_deps]
    if blacklisted_repos_found:
        print(f"- Found {len(blacklisted_repos_found)} blacklisted repositories")
        
    print(f"- Generated master snapshot: {os.path.join(ROOT_DIR, 'master_snapshot.json')}")
    print(f"- Generated dependency report: {os.path.join(DEPS_DIR, 'dependencies_report.md')}")
    if changelog_path:
        print(f"- Generated dependency changelog: {changelog_path}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()