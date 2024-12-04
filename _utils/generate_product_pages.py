import anthropic
import os
import yaml
from datetime import datetime
import glob

key = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Client(api_key=key)

def ask_claude(prompt):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return message.content[0].text

def convert_yamls_into_product_pages(tools_dir, output_folder, task_description):

    os.makedirs(output_folder, exist_ok=True)

    # Find all api.yaml files recursively
    yaml_files = glob.glob(os.path.join(tools_dir, "**/api.yaml"), recursive=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Process each yaml file
    for yaml_path in yaml_files:
        try:
            # Read and parse the YAML file
            with open(yaml_path, 'r') as file:
                yaml_content = file.read()
                yaml_data = yaml.safe_load(yaml_content)
            
            # Check if the tool should be processed
            if yaml_data.get('status') == 'prod' and not yaml_data.get('private', False):
                # Get the tool name from the parent directory
                tool_name = os.path.basename(os.path.dirname(yaml_path))
                
                # Create the prompt for Claude
                prompt = f"{task_description}\nTool description:\n{yaml_content}\nReply with just the full markdown of the product page."
                
                # Get the product page content from Claude
                product_page = ask_claude(prompt)
                
                # Create output filename
                output_filename = f"{tool_name}_{timestamp}.md"
                output_path = os.path.join(output_folder, output_filename)
                
                # Save the product page
                with open(output_path, 'w') as file:
                    file.write(product_page)
                
                print(f"Generated product page for {tool_name}: {output_filename}")
                
        except Exception as e:
            print(f"Error processing {yaml_path}: {str(e)}")

if __name__ == "__main__":
    tools_dir     = "../workspaces"
    output_folder = "../tool_pages"

    task_description = """Task: Create an SEO-Optimized Product Page for an AI Tool thats part of our creative agent stack.
Objective:
Create a compelling, user-friendly product page that showcases one of our autonomous creative assistants capabilities, based on the provided API interaction pattern (api.yaml). 
The page should be accessible to non-technical users while effectively communicating the tool's value and practical applications in the context of a larger creative agent platform.
Key Requirements:

Format: Write in markdown
Target Audience: Non-technical users seeking AI solutions and trying to understand creative AI agents capabilities
SEO Focus: Optimize for search engine discovery and user intent
Integration Context: Present as one component (tool) part of an agent building platform that offers a range of visual and creative AI agent capabilities.

Required Sections:

Engaging title
Brief, clear introduction to the tool itself
Key features list
Representative use cases/examples (you can add media placeholders for later population with visual examples)
Practical applications and problem-solving scenarios in which this tool can be used (either by a human directly or by the creative agent)

Content Guidelines:

Transform technical API descriptions into user-friendly explanations
Minimize technical jargon; focus on practical benefits and results
Emphasize capabilities and solutions rather than technical limitations
Include clear, relatable examples of specific problems the tool can solve
Write in an approachable, solution-focused tone
Present the tool as part of a larger AI solution suite (creative AI agent platform)
Serve as both a discovery tool and a practical usage template (documentation)
Dont dwell on the limitations of each tool (eg resolution limits etc), just focus on what makes the tool awesome and what users can do with it.

Marketing Approach:

Position each tool as a component of a larger creative AI agent solution suite (agent builder platform)
Focus on user benefits and practical applications
Make complex capabilities accessible and understandable through specific, real-world examples
Drive organic search traffic through problem-solution focused content

Expected Input:

API specification/documentation in YAML format containing tool description and parameter details as wel as example usage patterns

The final output should transform technical API documentation into engaging marketing content that functions as both a promotional asset and a practical guide, 
helping users quickly understand how they can leverage this specific tool for their needs while driving organic discovery through search engines.

Now, take a deep breath, think like a master product / marketing genius and generate the product page for the following tool:
"""

    convert_yamls_into_product_pages(tools_dir, output_folder, task_description)