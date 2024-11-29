import os
import yaml
import glob
import requests
from urllib.parse import urljoin

def download_thumbnails_from_yamls(tools_dir):
    # Base URL for the S3 bucket
    base_url = "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/"
    
    # Find all api.yaml files recursively
    yaml_files = glob.glob(os.path.join(tools_dir, "**/api.yaml"), recursive=True)
    
    # Process each yaml file
    for yaml_path in yaml_files:
        try:
            # Read and parse the YAML file
            with open(yaml_path, 'r') as file:
                yaml_data = yaml.safe_load(file)
            
            # Check if thumbnail field exists
            if yaml_data.get('status') == 'prod' and not yaml_data.get('private', False) and 'thumbnail' in yaml_data:
                # Get the thumbnail path
                thumbnail_path = yaml_data['thumbnail']
                
                # Create full URL
                full_url = urljoin(base_url, thumbnail_path)
                
                # Get filename from the path
                filename = os.path.basename(thumbnail_path)
                
                # Download the file
                print(f"Downloading {filename} from {full_url}")
                response = requests.get(full_url, stream=True)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                # Save the file
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                print(f"Successfully downloaded {filename}")
                
        except Exception as e:
            print(f"Error processing {yaml_path}: {str(e)}")

if __name__ == "__main__":
    tools_dir = "../workspaces"  # Using the same directory as the original script
    download_thumbnails_from_yamls(tools_dir)