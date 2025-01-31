import anthropic
import os
import yaml
import json
import argparse
import glob
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Documentation template
TEMPLATE = """1. Start with frontmatter containing aliases (include tool name variations)
2. Title (same as first alias)
3. Brief description explaining what the tool does and its key features/capabilities
4. Overview section listing main features as bullet points (keep this minimal, don't get hyperbolic or use marketing language, essential features only)
5. Quick Start section with:
   - Web UI steps (use format: Visit [Eden's Tool Name](https://www.eden.art/create/toolname))
   - Reference to API example in API Reference section
   - Chat agent usage ("Ask an Eden agent to use <this tool>")
6. Basic Usage section covering minimal required parameters
7. Technical guidelines (like resolution recommendations) and useful context about the tool/model
8. Section on best practices for inputs
9. Advanced Features section detailing each major feature:
   - What it does
   - Key parameters
   - Usage tips
10. Tips for Best Results section with subsections for:
    - Technical considerations
    - Input optimization
    - Feature combinations
11. Technical Details section listing:
    - Base model/technology
    - Default parameters
    - Supported formats
    - Limitations
12. Common Issues and Solutions section
13. API Reference section with:
    - Endpoint details
    - Headers
    - Basic request example
    - Full request example with all parameters
    - Response format
    - Error handling"""

# Example documentation format
EXAMPLE_DOC = """---
aliases: Create an image (SDXL), Text to Image Generation, txt2img
---
# Text to Image Generator (SDXL)

Generate high-quality images from text descriptions using the powerful SDXL model. This classic tool offers creative flexibility with support for custom models, style transfer, and shape guidance.

## Overview

- Text-driven image creation
- Custom model support (LoRA)
- Style image transfer
- Shape guidance control

## Quick Start

1. Visit [Eden's Text to Image Generator](https://www.eden.art/create/txt2img)
2. Enter your descriptive prompt
3. Choose resolution
4. Click "Create"

See [API Reference](#api-reference) section below for API usage examples.

Ask an Eden agent to use the "Text to Image Generator".

## Basic Usage

Required inputs:
- Text prompt
- Image dimensions

Optional settings:
- Number of samples
- Custom model (LoRA)
- Starting image
- Style image
- Shape guidance

## Technical Guidelines

### Resolution Options
| Aspect Ratio | Dimensions | Use Case |
|--------------|------------|----------|
| 21:9 | 1536x640 | Cinematic |
| 16:9 | 1344x768 | Widescreen |
| 3:2 | 1216x832 | Standard |
| 4:3 | 1152x896 | Classic |
| 1:1 | 1024x1024 | Square |
| 9:16 | 768x1344 | Mobile |
| 9:21 | 640x1536 | Panoramic |

### Generation Settings
- Steps: 10-50 (default: 35)
- Samples: 1-4
- Dimensions: 256-2048px
- Seed: Optional for reproducibility"""

def load_yaml(yaml_path):
    """Load and parse a YAML file"""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def load_test_json(yaml_path):
    """Load the corresponding test.json file if it exists"""
    test_json_path = Path(yaml_path).parent / "test.json"
    if test_json_path.exists():
        print(f"Found test.json at {test_json_path}")
        with open(test_json_path, 'r') as f:
            return json.load(f)
    print(f"No test.json found at {test_json_path}")
    return None

def create_doc_filename(yaml_path, output_dir=None):
    """Create the documentation filename"""
    if output_dir:
        # Use the tool name from the yaml path as the filename
        tool_name = Path(yaml_path).parent.name
        return Path(output_dir) / f"{tool_name}.md"
    else:
        # Default behavior: save next to yaml
        return Path(yaml_path).parent / "docs.md"

def ask_claude(yaml_content, yaml_path, test_json=None):
    """Generate documentation using Claude"""
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Extract tool name and label from YAML
    yaml_data = yaml.safe_load(yaml_content)
    display_name = yaml_data.get('name', '')
    
    # Get the case-sensitive tool name from the directory path
    tool_name = Path(yaml_path).parent.name
    print(f"Using case-sensitive tool name from directory: {tool_name}")

    # Extract example URLs from test.json if available
    example_urls = {}
    if test_json:
        for key in ['image', 'init_image', 'style_image', 'video', 'audio', 'subject_image', 'expression_image']:
            if key in test_json.get('args', {}):
                example_urls[key] = test_json['args'][key]
    
    # Prepare the context
    context = f"""Please create markdown documentation for this tool following this exact structure and format.

Important formatting requirements:
1. The Quick Start section must end with `Click "Create"` (not "Generate" or "Submit")
2. The Chat Agent line should be exactly: `Ask an Eden agent to "{display_name}".`
3. Use test.json values in the API examples if available
4. The Web UI link must follow this exact format: `Visit Eden Create: [{display_name}](https://beta.eden.art/create/{tool_name}) tool`
   - Use "Eden Create" as the platform name
   - Use the display name from YAML in the link text
   - Use beta.eden.art/create/{tool_name} as the URL (using case-sensitive tool_name)
   - Add "tool" at the end of the line
5. API requests must follow this exact format, using the case-sensitive tool name:
```bash
curl -X POST "https://api.eden.art/v2/tasks/create" \\
  -H "Content-Type: application/json" \\
  -H "X-Api-Key: YOUR_API_KEY" \\
  -d '{{
    "tool": "{tool_name}",
    "args": {{
      // parameters here
    }}
  }}'
```

6. Response format must include a complete example with all fields:
```json
{{
  "task": {{
    "_id": "task_12345",
    "createdAt": "2024-01-29T21:52:07.171578+00:00",
    "updatedAt": "2024-01-29T21:52:07.171608+00:00",
    "user": "user_id",
    "requester": "requester_id",
    "tool": "{tool_name}",
    "parent_tool": null,
    "output_type": "video",
    "args": {{
      "image": "https://example.com/image.jpg",
      "n_seconds": 6.0,
      "n_steps": 8,
      "resolution": 1024,
      "background_denoise": 0.6,
      "foreground_denoise": 0.3,
      "depth_effect": 0.4,
      "loop": false,
      "use_style_image": true,
      "style_image": "https://example.com/style.jpg",
      "style_strength": 0.8,
      "seed": 1234567890
    }},
    "mock": false,
    "cost": 48,
    "handler_id": "fc-xxxxx",
    "status": "pending",
    "error": null,
    "result": null,
    "performance": null
  }}
}}
```

Template structure:
{TEMPLATE}

Example documentation format:
{EXAMPLE_DOC}

Tool YAML configuration:
{yaml_content}

"""

    if test_json:
        context += f"""Example usage from test.json (use these exact values in the API examples):
{json.dumps(test_json, indent=2)}

Example URLs to use in documentation:
{json.dumps(example_urls, indent=2)}
"""

    context += """Important guidelines:
1. Follow the exact structure from the template
2. Match the style and formatting of the example documentation
3. Use the test.json values in API examples if available
4. Include all sections specified in the template
5. Use proper markdown formatting including code blocks with language tags
6. Create frontmatter with appropriate aliases including tool name variations
7. Keep the tone professional but accessible
8. Include comprehensive API reference section
9. Document all parameters and their usage
10. Include common issues and solutions
11. Ensure the Quick Start section ends with `Click "Create"`
12. Format the Chat Agent line exactly as specified
13. Use the exact URL format specified for the Web UI link
14. Follow the exact API request format provided
15. Include complete response format examples with all possible fields

Please generate the complete markdown documentation now. Do not ask any follow up questions, just try your best
given the context you have. If you are missing information to generate specific sections, just leave them out if you really have to. Your exact response will go live on our website as the documentation page for this tool."""

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        #model="claude-3-5-haiku-latest",
        max_tokens=4096,
        #temperature=0.7,
        messages=[{"role": "user", "content": context}]
    )  

    return message.content[0].text

def find_yaml_files(workspaces_dir, workflows=None):
    """Find all api.yaml files in the specified directories"""
    base_path = Path(workspaces_dir).resolve()
    print(f"Searching for YAML files in: {base_path}")
    
    if workflows:
        # Search in specific workflow directories
        yaml_files = []
        for workflow in workflows:
            print(f"Looking for workflow: {workflow}")
            # Try different possible path patterns
            patterns = [
                base_path / workflow / "api.yaml",  # Direct subdirectory
                base_path / workflow / "**/api.yaml",  # Nested under workflow name
                base_path / "*" / workflow / "api.yaml",  # Workflow under category
                base_path / "workspaces" / "*" / workflow / "api.yaml",  # Under workspaces and category
                base_path / "workspaces" / "*" / "workflows" / workflow / "api.yaml",  # Full path with workflows dir
                base_path / "*" / "*" / "workflows" / workflow / "api.yaml"  # Any nested path with workflows dir
            ]
            for pattern in patterns:
                print(f"Trying pattern: {pattern}")
                matches = glob.glob(str(pattern), recursive=True)
                if matches:
                    print(f"Found matches: {matches}")
                yaml_files.extend(matches)
    else:
        # Search all directories recursively
        pattern = str(base_path / "**/api.yaml")
        print(f"Searching all with pattern: {pattern}")
        yaml_files = glob.glob(pattern, recursive=True)
        if yaml_files:
            print(f"Found {len(yaml_files)} files:")
            for yaml_file in yaml_files:
                print(yaml_file)
    
    if not yaml_files:
        print("No api.yaml files found!")
        
    return yaml_files

def tool_is_live_on_prod(yaml_content):
    # grab status (fallback to 'prod' if missing:)
    status = yaml_content.get('status', 'prod')
    visible = yaml_content.get('status', True)
    return (status == "prod") and visible

def maybe_inject_thumbnail(doc_content, yaml_content):
    thumbnail_url = yaml_content.get('thumbnail', '')

    if thumbnail_url:
        # Inject the thumbnail display line just below the page title (first # line)
        thumbnail_url = "https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/" + thumbnail_url

        if '.mp4' in thumbnail_url:
            thumbnail_display = f"""<video width="50%" controls>
            <source src="{thumbnail_url}" type="video/mp4" />
            </video>"""
        else:
            thumbnail_display = f"![alt text]({thumbnail_url})"

        lines = doc_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# '):
                lines.insert(i + 1, thumbnail_display)
        return '\n'.join(lines) 
       
    return doc_content

def generate_docs(workspaces_dir, workflows=None, output_dir=None):
    """Generate documentation for all found YAML files"""
    yaml_files = find_yaml_files(workspaces_dir, workflows)
    
    if output_dir:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"Saving documentation files to: {output_dir}")
    
    for yaml_path in yaml_files:
        #try:
        print(f"Processing {yaml_path}...")
        
        # Load YAML and test.json
        yaml_content = load_yaml(yaml_path)
        if not tool_is_live_on_prod(yaml_content): # skip making docs for this tool
            continue
        
        print(f"Generating docs for {yaml_path}...")
        test_json = load_test_json(yaml_path)
        
        doc_path = create_doc_filename(yaml_path, output_dir)
        raw_yaml_string = yaml.dump(yaml_content)

        # Generate documentation
        doc_content = ask_claude(raw_yaml_string, yaml_path, test_json)
        doc_content = maybe_inject_thumbnail(doc_content, yaml_content)
        
        # Save documentation
        with open(doc_path, 'w') as f:
            f.write(doc_content)

        print(f"Created documentation: {doc_path}")
            
        #except Exception as e:
        #    print(f"Error processing {yaml_path}: {str(e)}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate documentation for YAML files')
    parser.add_argument('--workspaces', type=str, default='..',
                       help='Directory containing workspaces')
    parser.add_argument('workflows', nargs='*',
                       help='Optional specific workflows to document')
    parser.add_argument('--output-dir', type=str, default='../docs_md',
                       help='Optional output directory for documentation files')
    
    args = parser.parse_args()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    
    generate_docs(args.workspaces, args.workflows, args.output_dir)

if __name__ == '__main__':
    main() 