#!/usr/bin/env python3
"""
Test script for the deployed ComfyUI texture flow model.
"""

import urllib.request
import json
import time
import pathlib

# Deployed endpoint URL
ENDPOINT_URL = "https://edenartlab--comfyui-slow-new-texture-flow-stage-comfyui-api.modal.run/"

# Test parameters from test.json
test_params = {
    "images": [
        "https://d14i3advvh2bvd.cloudfront.net/53c044a1d7fcc46587ba82ff95c1241f56a4b1d62f95241569d26a15d7aff39a_2560.webp",
        "https://d14i3advvh2bvd.cloudfront.net/66890d4e0d7d975d4a10e0dc9ba0b9e61d15d2deaaf1ceeb0c5a372f8f50e122_2560.webp",
        "https://d14i3advvh2bvd.cloudfront.net/c0379a280e07ab777193b4148e652bb1f830c1f757fd09d35e824b62c12050b9_2560.webp"
    ],
    "n_seconds": 2.5,
    "n_steps": 4,
    "width": 384,
    "height": 384,
    "seed": 42,
    "upscale": False,
    "upscale_esrgan": False,
    "use_controlnet1": False,
    "preprocessor1": "DepthAnythingV2Preprocessor",
    "controlnet_strength1": 0.5
}

OUTPUT_DIR = pathlib.Path("/tmp/comfyui")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

def test_texture_flow():
    """Test the texture flow endpoint with the test parameters."""
    print("Testing ComfyUI texture flow deployment...")
    print(f"Endpoint: {ENDPOINT_URL}")
    print(f"Parameters: {json.dumps(test_params, indent=2)}")
    
    data = json.dumps(test_params).encode("utf-8")
    print("\nSending request...")
    start_time = time.time()
    
    req = urllib.request.Request(
        ENDPOINT_URL, data=data, headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            elapsed = round(time.time() - start_time, 1)
            print(f"✅ Success! Request completed in {elapsed} seconds")
            print(f"Response status: {response.status}")
            print(f"Content type: {response.headers.get('content-type')}")
            
            # Save response based on content type
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                filename = OUTPUT_DIR / f"texture_flow_output_{int(time.time())}.png"
                filename.write_bytes(response.read())
                print(f"Saved image to '{filename}'")
            elif 'json' in content_type:
                result = json.loads(response.read().decode('utf-8'))
                print(f"JSON response: {json.dumps(result, indent=2)}")
            else:
                content = response.read()
                print(f"Response length: {len(content)} bytes")
                # Try to decode as text
                try:
                    text = content.decode('utf-8')
                    print(f"Response text: {text[:500]}...")
                except UnicodeDecodeError:
                    print("Binary response received")
                    
    except urllib.error.HTTPError as e:
        print(f"❌ Request failed with HTTP error: {e.code}")
        try:
            error_response = e.read().decode('utf-8')
            print(f"Error response: {error_response}")
        except:
            print("Could not read error response")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_texture_flow()