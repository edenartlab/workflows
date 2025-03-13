import json
import requests
from urllib.parse import urlparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_git_repo(url):
    return url.startswith('git clone')

def check_url(file_path, url):
    if is_git_repo(url):
        # For git repos, we'll just assume they're valid if they're from huggingface
        if 'huggingface.co' in url:
            return None
        return (file_path, url, "Git repo not from huggingface")
    
    try:
        # Just send a HEAD request to check if the URL is accessible
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, allow_redirects=True, timeout=10, headers=headers)
        
        if response.status_code == 404:
            return (file_path, url, f"404 Not Found")
        elif response.status_code != 200:
            return (file_path, url, f"HTTP {response.status_code}")
            
        return None
    except requests.exceptions.RequestException as e:
        return (file_path, url, str(e))

def main():
    # Load the JSON file
    with open('downloads.json', 'r') as f:
        downloads = json.load(f)
    
    print(f"Checking {len(downloads)} URLs...")
    
    # Store failed URLs
    failed_urls = []
    
    # Use ThreadPoolExecutor for parallel checking
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {
            executor.submit(check_url, file_path, url): (file_path, url)
            for file_path, url in downloads.items()
        }
        
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                failed_urls.append(result)
    
    # Print results
    if failed_urls:
        print("\nFailed URLs:")
        print("-" * 80)
        for file_path, url, error in failed_urls:
            print(f"\nFile: {file_path}")
            print(f"URL: {url}")
            print(f"Error: {error}")
        print(f"\nTotal failed: {len(failed_urls)} out of {len(downloads)}")
    else:
        print("\nAll URLs are accessible!")

if __name__ == "__main__":
    main()