import os
import yaml
import glob
import argparse
from yaml.representer import SafeRepresenter
import textwrap

# Custom YAML formatting
class LiteralString(str): pass

def literal_presenter(dumper, data):
    # Always use |- style for literal blocks
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|-')

yaml.add_representer(LiteralString, literal_presenter)

def format_multiline_string(text):
    if not text:
        return text
    if isinstance(text, str):
        # Remove any existing quotes and |- markers
        text = text.replace('"', '').replace("'", '')
        text = text.replace('|-', '').strip()
        
        # Split into lines and wrap long lines
        lines = []
        for line in text.split('\n'):
            if len(line.strip()) > 80:
                # Wrap long lines at word boundaries
                wrapped = textwrap.wrap(line.strip(), width=80, break_long_words=False, break_on_hyphens=False)
                lines.extend(wrapped)
            else:
                lines.append(line.strip())
        
        # Remove empty lines at start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
            
        # Return as LiteralString with proper indentation
        return LiteralString(text.strip())
    return text

def standardize_yaml(content):
    # Parse YAML content
    data = yaml.safe_load(content)
    
    # Format tip at root level
    if 'tip' in data:
        data['tip'] = format_multiline_string(data['tip'])
    
    # Ensure visible field exists and is set correctly based on status
    if 'status' in data:
        if data['status'] == 'stage':
            data['status'] = 'prod'
        data['visible'] = data['status'] != 'inactive'
    else:
        data['visible'] = True
        
    # Ensure resolutions exists
    if 'resolutions' not in data:
        data['resolutions'] = None

    # Format any tips in parameters
    if 'parameters' in data:
        for param_name, param_data in data['parameters'].items():
            if isinstance(param_data, dict) and 'tip' in param_data:
                param_data['tip'] = format_multiline_string(param_data['tip'])
    
    # Create new ordered dictionary with desired order
    ordered_data = {
        'name': data.get('name', ''),
        'description': data.get('description', ''),
        'tip': data.get('tip', ''),
        'output_type': data.get('output_type', ''),
        'cost_estimate': data.get('cost_estimate', ''),
        'thumbnail': data.get('thumbnail', ''),
        'status': data.get('status', ''),
        'visible': data['visible'],
        'resolutions': data.get('resolutions', None),
        'handler': data.get('handler', ''),
        'base_model': data.get('base_model', '')
    }
    
    # Add remaining fields that should come after the standardized header
    for key, value in data.items():
        if key not in ordered_data:
            ordered_data[key] = value
            
    return ordered_data

class OrderedDumper(yaml.Dumper):
    def represent_str(self, data):
        if isinstance(data, LiteralString) or '\n' in data:
            return self.represent_scalar('tag:yaml.org,2002:str', data, style='|-')
        return self.represent_scalar('tag:yaml.org,2002:str', data)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Process the YAML content
    processed_data = standardize_yaml(content)
    
    # Write back to file with custom formatting
    with open(file_path, 'w', encoding='utf-8') as f:
        OrderedDumper.add_representer(str, OrderedDumper.represent_str)
        OrderedDumper.add_representer(LiteralString, literal_presenter)
        yaml_str = yaml.dump(processed_data, Dumper=OrderedDumper, allow_unicode=True, sort_keys=False, default_flow_style=False, width=float("inf"))
        # Remove any escaped newlines and fix string formatting
        yaml_str = yaml_str.replace('\\n', '\n').replace('"', '')
        f.write(yaml_str)

def find_api_files(workspace=None, workflow=None):
    # Get the parent directory of _utils
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Build the search pattern
    if workspace and workflow:
        pattern = os.path.join(parent_dir, workspace, workflow, '**/api.yaml')
    elif workspace:
        pattern = os.path.join(parent_dir, workspace, '**/api.yaml')
    else:
        pattern = os.path.join(parent_dir, '**/api.yaml')
    
    # Find all matching api.yaml files
    return glob.glob(pattern, recursive=True)

def main():
    parser = argparse.ArgumentParser(description='Process api.yaml files with optional workspace and workflow filters')
    parser.add_argument('--workspace', help='Filter by workspace name')
    parser.add_argument('--workflow', help='Filter by workflow name (requires workspace to be specified)')
    args = parser.parse_args()
    
    if args.workflow and not args.workspace:
        parser.error("--workflow requires --workspace to be specified")
    
    api_files = find_api_files(args.workspace, args.workflow)
    
    print(f"Found {len(api_files)} api.yaml files to process")
    
    for file_path in api_files:
        print(f"Processing {file_path}")
        try:
            process_file(file_path)
            print(f"Successfully processed {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            
if __name__ == "__main__":
    main() 