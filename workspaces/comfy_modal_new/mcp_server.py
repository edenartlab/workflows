#!/usr/bin/env python3
"""
MCP Server for Eden Modal ComfyUI Workflows

This server exposes Modal ComfyUI workflows as MCP tools, allowing Claude to
generate videos and images using deployed ComfyUI workflows.

Installation:
    pip install mcp httpx

Usage:
    # Run the server
    python mcp_server.py

    # Install in Claude Desktop config
    mcp install mcp_server.py
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
import httpx

# Create the MCP server
mcp = FastMCP("Eden ComfyUI Workflows")

# Configuration - these would typically come from environment variables
MODAL_ENDPOINTS = {
    "texture_flow": {
        "url": "https://edenartlab--comfyui-slow-new-texture-flow-stage-comfyui-api.modal.run",
        "description": "Generate texture flow videos from input images",
        "workspace": "slow_new",
        "workflow": "texture_flow"
    }
    # Add more workflows here as they are deployed
}

async def get_workflow_schema(endpoint_url: str) -> Dict[str, Any]:
    """Fetch the parameter schema for a workflow."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{endpoint_url}/schema")
            if response.status_code == 200:
                return response.json()
            else:
                return {"parameters": {}, "error": f"Failed to fetch schema: {response.status_code}"}
    except Exception as e:
        return {"parameters": {}, "error": f"Schema fetch error: {str(e)}"}

@mcp.tool()
async def generate_texture_flow_video(
    images: List[str],
    n_seconds: float = 2.5,
    n_steps: int = 4,
    width: int = 384,
    height: int = 384,
    seed: int = 42,
    upscale: bool = False,
    upscale_esrgan: bool = False,
    use_controlnet1: bool = False,
    preprocessor1: str = "DepthAnythingV2Preprocessor",
    controlnet_strength1: float = 0.5
) -> Dict[str, Any]:
    """
    Generate a texture flow video from input images using ComfyUI.
    
    Args:
        images: List of image URLs to process
        n_seconds: Duration of the output video in seconds
        n_steps: Number of diffusion steps
        width: Output width in pixels
        height: Output height in pixels
        seed: Random seed for reproducible results
        upscale: Whether to upscale the output
        upscale_esrgan: Whether to use ESRGAN for upscaling
        use_controlnet1: Whether to use ControlNet
        preprocessor1: ControlNet preprocessor to use
        controlnet_strength1: Strength of ControlNet influence
    
    Returns:
        Dictionary containing the result status and output file information
    """
    endpoint_url = MODAL_ENDPOINTS["texture_flow"]["url"]
    
    payload = {
        "images": images,
        "n_seconds": n_seconds,
        "n_steps": n_steps,
        "width": width,
        "height": height,
        "seed": seed,
        "upscale": upscale,
        "upscale_esrgan": upscale_esrgan,
        "use_controlnet1": use_controlnet1,
        "preprocessor1": preprocessor1,
        "controlnet_strength1": controlnet_strength1
    }
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{endpoint_url}/api",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "workflow": "texture_flow",
                    "result": result,
                    "message": "Video generation completed successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "workflow": "texture_flow"
                }
                
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timed out after 5 minutes",
            "workflow": "texture_flow"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "workflow": "texture_flow"
        }

@mcp.tool()
async def check_workflow_health(workflow_name: str = "texture_flow") -> Dict[str, Any]:
    """
    Check the health status of a ComfyUI workflow endpoint.
    
    Args:
        workflow_name: Name of the workflow to check
    
    Returns:
        Dictionary containing health status information
    """
    if workflow_name not in MODAL_ENDPOINTS:
        return {
            "success": False,
            "error": f"Unknown workflow: {workflow_name}",
            "available_workflows": list(MODAL_ENDPOINTS.keys())
        }
    
    endpoint_url = MODAL_ENDPOINTS[workflow_name]["url"]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{endpoint_url}/health")
            
            if response.status_code == 200:
                health_data = response.json()
                return {
                    "success": True,
                    "workflow": workflow_name,
                    "health": health_data,
                    "endpoint": endpoint_url
                }
            else:
                return {
                    "success": False,
                    "workflow": workflow_name,
                    "error": f"Health check failed: HTTP {response.status_code}",
                    "endpoint": endpoint_url
                }
                
    except Exception as e:
        return {
            "success": False,
            "workflow": workflow_name,
            "error": f"Health check failed: {str(e)}",
            "endpoint": endpoint_url
        }

@mcp.tool()
async def list_available_workflows() -> Dict[str, Any]:
    """
    List all available ComfyUI workflows and their descriptions.
    
    Returns:
        Dictionary containing available workflows and their information
    """
    workflows = {}
    
    for name, config in MODAL_ENDPOINTS.items():
        # Try to get schema information
        schema = await get_workflow_schema(config["url"])
        
        workflows[name] = {
            "description": config["description"],
            "workspace": config["workspace"],
            "workflow": config["workflow"],
            "endpoint": config["url"],
            "parameters": schema.get("parameters", {}),
            "schema_error": schema.get("error")
        }
    
    return {
        "success": True,
        "workflows": workflows,
        "count": len(workflows)
    }

@mcp.tool()
async def get_workflow_schema_tool(workflow_name: str) -> Dict[str, Any]:
    """
    Get the parameter schema for a specific workflow.
    
    Args:
        workflow_name: Name of the workflow
    
    Returns:
        Dictionary containing the workflow's parameter schema
    """
    if workflow_name not in MODAL_ENDPOINTS:
        return {
            "success": False,
            "error": f"Unknown workflow: {workflow_name}",
            "available_workflows": list(MODAL_ENDPOINTS.keys())
        }
    
    endpoint_url = MODAL_ENDPOINTS[workflow_name]["url"]
    schema = await get_workflow_schema(endpoint_url)
    
    return {
        "success": True,
        "workflow": workflow_name,
        "schema": schema
    }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()