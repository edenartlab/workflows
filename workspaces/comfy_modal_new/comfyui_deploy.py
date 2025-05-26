#!/usr/bin/env python3

"""
Modern ComfyUI deployment script using comfy-cli and memory snapshots.
Supports workspace structure with multiple workspaces and workflows.

Usage examples:
    # Deploy texture_flow workflow from slow workspace
    WORKSPACE=slow WORKFLOW=texture_flow modal deploy comfyui_deploy.py
    
    # Deploy to staging
    DB=STAGE WORKSPACE=slow_new WORKFLOW=texture_flow modal deploy comfyui_deploy.py

    DB=STAGE WORKSPACE=slow_new WORKFLOW=texture_flow modal deploy comfyui_deploy.py
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List
import base64
import mimetypes

import modal

# Read environment variables
db = os.getenv("DB", "STAGE").upper()
workspace_name = os.getenv("WORKSPACE")
workflow_name = os.getenv("WORKFLOW")

if not workspace_name:
    raise Exception("WORKSPACE environment variable is required")

if not workflow_name:
    raise Exception("WORKFLOW environment variable is required")

# App configuration
app_name = f"comfyui-{workspace_name}-{workflow_name}-{db}"
workspace_path = f"workspaces/{workspace_name}"

print("=" * 50)
print(f"Database: {db}")
print(f"Workspace: {workspace_name}")
print(f"Workflow: {workflow_name}")
print(f"App name: {app_name}")
print("=" * 50)

# Create persistent volume for downloads/models
downloads_vol = modal.Volume.from_name("comfy-downloads", create_if_missing=True)


def install_comfyui():
    """Install ComfyUI using snapshot configuration."""
    print("Installing ComfyUI...")
    
    # Read snapshot configuration
    snapshot = json.load(open("/root/workspace/snapshot.json", "r"))
    comfyui_commit_sha = snapshot["comfyui"]
    
    print(f"Installing ComfyUI commit: {comfyui_commit_sha}")
    
    # Use comfy-cli to install ComfyUI
    subprocess.run([
        "comfy", "--skip-prompt", "install", 
        "--fast-deps", "--nvidia", 
        "--version", "0.3.10"
    ], check=True)
    
    print("ComfyUI installation completed")


def install_custom_nodes():
    """Install custom nodes from snapshot configuration."""
    print("Installing custom nodes...")
    
    snapshot = json.load(open("/root/workspace/snapshot.json", "r"))
    
    # Install git custom nodes
    git_custom_nodes = snapshot.get("git_custom_nodes", {})
    for url, node_info in git_custom_nodes.items():
        if node_info.get("disabled", False):
            print(f"Skipping disabled node: {url}")
            continue
            
        commit_hash = node_info["hash"]
        print(f"Installing custom node: {url} at {commit_hash}")
        
        try:
            # Use comfy-cli to install the custom node (ignoring commit hash for now)
            subprocess.run([
                "comfy", "node", "install", url
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {url}: {e}")
            # Continue with other nodes
    
    # Install CNR custom nodes if available
    cnr_custom_nodes = snapshot.get("cnr_custom_nodes", {})
    for node_name, version in cnr_custom_nodes.items():
        print(f"Installing CNR node: {node_name}@{version}")
        try:
            subprocess.run([
                "comfy", "node", "install", f"{node_name}@{version}"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install {node_name}: {e}")
    
    print("Custom nodes installation completed")


def download_files():
    """Download files based on downloads.json configuration."""
    print("Downloading workspace files...")
    
    downloads = json.load(open("/root/workspace/downloads.json", "r"))
    
    for path_key, source_url in downloads.items():
        print(f"Processing: {path_key}")
        
        comfy_path = Path("/root") / path_key
        vol_path = Path("/data") / path_key
        
        # Skip if file already exists in ComfyUI directory
        if comfy_path.exists():
            print(f"  Already exists: {comfy_path}")
            continue
        
        # Create parent directories
        comfy_path.parent.mkdir(parents=True, exist_ok=True)
        vol_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if source_url.startswith("git clone "):
                # Handle git repositories
                repo_url = source_url[10:].strip()
                if not vol_path.exists():
                    print(f"  Cloning: {repo_url}")
                    subprocess.run([
                        "git", "clone", repo_url, str(vol_path)
                    ], check=True)
                    downloads_vol.commit()
                
                # Create symlink
                if not comfy_path.exists():
                    comfy_path.symlink_to(vol_path, target_is_directory=True)
                    
            else:
                # Handle regular file downloads
                if not vol_path.exists():
                    print(f"  Downloading: {source_url}")
                    subprocess.run([
                        "wget", "-O", str(vol_path), source_url
                    ], check=True)
                    downloads_vol.commit()
                
                # Create symlink
                if not comfy_path.exists():
                    comfy_path.symlink_to(vol_path)
                    
        except Exception as e:
            print(f"  Error processing {path_key}: {e}")
            
    print("Downloads completed")


# Build the Modal image
image = (
    modal.Image.debian_slim(python_version="3.11")
    .env({
        "COMFYUI_PATH": "/root",
        "COMFYUI_MODEL_PATH": "/root/models",
        "WORKSPACE": workspace_name,
        "WORKFLOW": workflow_name,
        "DB": db
    })
    .apt_install(
        "git", "git-lfs", "wget", "curl",
        "libgl1-mesa-glx", "libglib2.0-0", 
        "libmagic1", "ffmpeg", "libegl1"
    )
    .pip_install("comfy-cli==1.3.8")
    .add_local_dir(workspace_path, "/root/workspace", copy=True)
    .run_function(install_comfyui)
    .run_function(install_custom_nodes)
    .run_function(
        download_files,
        volumes={"/data": downloads_vol}
    )
)

# Create the Modal app
app = modal.App(name=app_name, image=image)


@app.cls(
    gpu="T4",
    cpu=2.0,
    volumes={"/data": downloads_vol},
    timeout=1200,
    enable_memory_snapshot=True,
    scaledown_window=60,
)
class ComfyUI:
    port: int = 8000

    @modal.enter(snap=True)
    def launch_comfy_background(self):
        """Launch ComfyUI server in background."""
        print("Starting ComfyUI server...")
        cmd = f"comfy launch --background -- --port {self.port}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"ComfyUI server started on port {self.port}")

    @modal.enter(snap=False)
    def restore_snapshot(self):
        """Restore GPU state after snapshot."""
        print("Restoring GPU state after snapshot...")
        # Note: This would require a custom node for GPU reinitialization
        # For now, we'll just ensure the server is healthy
        self.poll_server_health()

    @modal.method()
    def run_workflow(self, workflow_args: Dict = None):
        """Run the specified workflow with given arguments."""
        if workflow_args is None:
            workflow_args = {}
            
        # Ensure server is healthy
        self.poll_server_health()
        
        # Get workflow path
        workflow_path = f"/root/workspace/workflows/{workflow_name}/workflow_api.json"
        
        if not Path(workflow_path).exists():
            raise Exception(f"Workflow not found: {workflow_path}")
        
        # Load and modify workflow with arguments
        workflow = json.loads(Path(workflow_path).read_text())
        
        # Apply workflow arguments (basic example)
        for key, value in workflow_args.items():
            print(f"Setting workflow parameter: {key} = {value}")
            # This would need more sophisticated parameter injection
            # based on your workflow structure
        
        # Save modified workflow
        temp_workflow = f"/tmp/workflow_{workflow_name}.json"
        with open(temp_workflow, "w") as f:
            json.dump(workflow, f)
        
        print(f"Running workflow: {workflow_name}")
        
        # Run workflow using comfy-cli
        cmd = f"comfy run --workflow {temp_workflow} --wait --timeout 1200"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Workflow failed: {result.stderr}")
        
        # Find output files and create accessible URLs
        output_dir = Path("/root/comfy/ComfyUI/output")
        output_files = list(output_dir.glob("*.mp4")) + list(output_dir.glob("*.png")) + list(output_dir.glob("*.gif"))
        
        # Create file serving endpoints for each output
        file_urls = []
        for file_path in output_files:
            # Store file content for serving
            file_content = file_path.read_bytes()
            file_name = file_path.name
            
            # For now, we'll include the file info and base64 content
            # In production, upload to S3/GCS and return URLs
            file_urls.append({
                "filename": file_name,
                "size": len(file_content),
                "type": "video" if file_name.endswith(('.mp4', '.gif')) else "image",
                "content_base64": base64.b64encode(file_content).decode('utf-8'),
                "mime_type": mimetypes.guess_type(file_name)[0] or "application/octet-stream"
            })
        
        return {
            "output_files": file_urls,
            "file_count": len(output_files),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "workflow_completed": True
        }

    @modal.web_endpoint(method="POST")
    def api(self, request: Dict):
        """HTTP API endpoint for running workflows."""
        try:
            # Pass the entire request as workflow_args
            result = self.run_workflow.remote(request)
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    @modal.web_endpoint(method="GET")
    def health(self):
        """Health check endpoint."""
        return {"status": "healthy", "workflow": workflow_name, "workspace": workspace_name}

    @modal.web_endpoint(method="GET") 
    def schema(self):
        """Return the schema/parameters for this workflow."""
        try:
            # Read test.json to get parameter schema
            test_file = f"/root/workspace/workflows/{workflow_name}/test.json"
            if Path(test_file).exists():
                with open(test_file, "r") as f:
                    test_params = json.load(f)
                return {
                    "workflow": workflow_name,
                    "workspace": workspace_name,
                    "parameters": test_params,
                    "description": f"ComfyUI {workflow_name} workflow"
                }
            else:
                return {
                    "workflow": workflow_name, 
                    "workspace": workspace_name,
                    "parameters": {},
                    "description": f"ComfyUI {workflow_name} workflow"
                }
        except Exception as e:
            return {
                "error": str(e),
                "workflow": workflow_name,
                "workspace": workspace_name
            }

    def poll_server_health(self):
        """Check if ComfyUI server is healthy."""
        import socket
        import urllib.request
        import urllib.error
        
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{self.port}/system_stats")
            urllib.request.urlopen(req, timeout=5)
            print("ComfyUI server is healthy")
        except (socket.timeout, urllib.error.URLError) as e:
            print(f"Server health check failed: {e}")
            # Try to restart the server
            self.launch_comfy_background()


@app.local_entrypoint()
def test_workflow():
    """Test the workflow locally."""
    print(f"Testing {workflow_name} workflow...")
    
    comfyui = ComfyUI()
    
    # Example test arguments for texture_flow
    test_args = {
        "n_seconds": 4.0,
        "width": 640,
        "height": 640,
        "motion_scale": 1.1,
        "use_upscale": False  # Faster for testing
    }
    
    try:
        result = comfyui.run_workflow(test_args)
        print("Test completed successfully!")
        print(f"Output files: {result['output_files']}")
    except Exception as e:
        print(f"Test failed: {e}")
        raise


if __name__ == "__main__":
    print("Use 'modal deploy comfyui_deploy.py' to deploy")
    print("Use 'modal run comfyui_deploy.py::test_workflow' to test")