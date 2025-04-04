#!/usr/bin/env python3

import os
import sys
import yaml
import argparse
from collections import defaultdict
from typing import Dict, List, Optional, Set

def load_yaml_header(file_path: str) -> Optional[Dict]:
    """Load YAML file and return header section (before comfyui_output_node_id)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split at comfyui_output_node_id to get header
        parts = content.split('comfyui_output_node_id:')
        if len(parts) < 2:
            return None
            
        # Parse just the header portion without adding dummy value
        header = parts[0].strip()
        return yaml.safe_load(header)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_all_workflows(workspace_path: str) -> List[str]:
    """Get list of all workflow directories in the workspace."""
    try:
        return [d for d in os.listdir(workspace_path) 
                if os.path.isdir(os.path.join(workspace_path, d))]
    except Exception as e:
        print(f"Error accessing workspace {workspace_path}: {e}")
        return []

def collect_header_data(workspace_path: str, workflows: Optional[List[str]] = None) -> Dict:
    """Collect header data from all specified workflows."""
    data = {}
    all_fields = set()
    
    if workflows is None:
        workflows = get_all_workflows(workspace_path)
    
    for workflow in workflows:
        api_path = os.path.join(workspace_path, workflow, 'api.yaml')
        if not os.path.exists(api_path):
            continue
            
        header = load_yaml_header(api_path)
        if header:
            data[workflow] = header
            all_fields.update(header.keys())
    
    return data, all_fields

def generate_field_table(field: str, data: Dict) -> str:
    """Generate markdown table for a specific field."""
    table = f"\n### {field}\n\n"
    table += "| Workflow | Value |\n"
    table += "|----------|-------|\n"
    
    for workflow, header in sorted(data.items()):
        value = header.get(field, "❌ Missing")
        if isinstance(value, (list, dict)):
            value = yaml.dump(value, default_flow_style=False).strip()
        value = str(value).replace("\n", "<br>")
        table += f"| {workflow} | {value} |\n"
    
    return table

def generate_complete_table(data: Dict, fields: Set[str]) -> str:
    """Generate complete table with all fields as columns."""
    table = "\n### Complete Field Analysis\n\n"
    
    # Header row
    table += "| Workflow | " + " | ".join(sorted(fields)) + " |\n"
    table += "|" + "---|" * (len(fields) + 1) + "\n"
    
    # Data rows
    for workflow, header in sorted(data.items()):
        row = [workflow]
        for field in sorted(fields):
            value = header.get(field, "❌")
            if isinstance(value, (list, dict)):
                value = "✓"  # Use checkmark for complex values
            row.append(str(value))
        table += "| " + " | ".join(row) + " |\n"
    
    return table

def generate_report(workspace_path: str, workflows: Optional[List[str]] = None) -> str:
    """Generate complete markdown report."""
    data, fields = collect_header_data(workspace_path, workflows)
    
    if not data:
        return "No workflow data found!"
    
    report = "# Workflow Header Analysis Report\n\n"
    
    # Add workflow count and list
    report += f"## Analysis of {len(data)} workflows\n\n"
    report += "Workflows analyzed:\n"
    for workflow in sorted(data.keys()):
        report += f"- {workflow}\n"
    
    # Add individual field tables
    report += "\n## Individual Field Analysis\n"
    for field in sorted(fields):
        report += generate_field_table(field, data)
        report += "\n"
    
    # Add complete table
    report += generate_complete_table(data, fields)
    
    return report

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate workflow header analysis report',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Analyze all workflows in mono_workspace
  workflow_header_report.py
  
  # Using positional arguments
  workflow_header_report.py mono_workspace workflow1,workflow2
  
  # Using flags
  workflow_header_report.py --workspace mono_workspace --workflows workflow1,workflow2
  workflow_header_report.py -w mono_workspace -f workflow1,workflow2
''')

    # Add arguments
    parser.add_argument('workspace', nargs='?', default='mono_workspace',
                       help='Workspace name (default: mono_workspace)')
    parser.add_argument('workflow_list', nargs='?',
                       help='Comma-separated list of workflows')
    
    # Add flag alternatives
    parser.add_argument('-w', '--workspace', dest='workspace_flag',
                       help='Workspace name (alternative to positional argument)')
    parser.add_argument('-f', '--workflows', dest='workflows_flag',
                       help='Comma-separated list of workflows (alternative to positional argument)')

    args = parser.parse_args()

    # Resolve workspace (prefer flag over positional)
    workspace = args.workspace_flag if args.workspace_flag else args.workspace

    # Resolve workflows (prefer flag over positional)
    workflows = None
    if args.workflows_flag:
        workflows = args.workflows_flag.split(',')
    elif args.workflow_list:
        workflows = args.workflow_list.split(',')

    return workspace, workflows

def main():
    workspace, workflows = parse_args()
    
    # Construct workspace path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_path = os.path.join(script_dir, "..", "workspaces", workspace)  # Remove "workflows" from path
    workflows_path = os.path.join(workspace_path, "workflows")  # Add separate workflows path
    
    if not os.path.exists(workflows_path):
        print(f"Error: Workflows path not found: {workflows_path}")
        sys.exit(1)
    
    report = generate_report(workflows_path, workflows)  # Pass workflows_path to generate_report
    
    # Save report to workspace root directory
    report_path = os.path.join(workspace_path, "header_analysis.md")  # Use workspace_path for report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main()