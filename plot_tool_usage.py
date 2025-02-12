import os
import matplotlib.pyplot as plt
from collections import defaultdict

def analyze_yaml_files(root_folder):
    # Dictionary to store character counts
    char_counts = defaultdict(int)
    
    # Walk through directory tree
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == "api.yaml":
                # Get parent folder name
                parent_folder = os.path.basename(dirpath)
                
                # Read file content
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                    char_counts[parent_folder] = len(content)
    
    return dict(char_counts)

def plot_char_counts(char_counts):
    # Sort data by values
    sorted_data = dict(sorted(char_counts.items(), key=lambda x: x[1], reverse=True))
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(sorted_data.values(), labels=sorted_data.keys(), autopct='%1.1f%%')
    
    # Add legend
    plt.legend(sorted_data.keys(), 
              title="Folders", 
              loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.title('Character Count Distribution in api.yaml Files')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Usage
if __name__ == "__main__":
    root_folder = "/home/rednax/SSD2TB/Github_repos/Eden/eden_eve_new/eve"  # Replace with your root folder path
    char_counts = analyze_yaml_files(root_folder)
    plot_char_counts(char_counts)