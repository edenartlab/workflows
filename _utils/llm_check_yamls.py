import os
import yaml
import openai
import dotenv
import time, requests, sys
from datetime import datetime

dotenv.load_dotenv()
# Load the API key from the environment variable:
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Define the delimiter
DELIMITER = "\n-----------------------------------\n"

import os
import yaml

def gather_yaml_files(root_path, delimiter):
    concatenated_content = ""
    n_yamls_read = 0

    # Get a sorted list of YAML files from the directory
    yaml_files = []
    for subdir, _, files in os.walk(root_path):
        for file in sorted(files):  # Sort the files to ensure order
            if file.endswith(".yaml"):
                yaml_files.append(os.path.join(subdir, file))

    # Iterate through the sorted list of files
    for file_path in yaml_files:
        print(f"Reading {file_path}")
        with open(file_path, 'r') as f:
            try:
                yaml_content = yaml.safe_load(f)
                # Convert the yaml_content to string and concatenate
                concatenated_content += f"Tool: {file_path}\n" + yaml.dump(yaml_content) + delimiter
                n_yamls_read += 1
            except yaml.YAMLError as e:
                print(f"Error reading {file_path}: {e}")

    # Print info about the number of files and the total number of lines
    print(f"Number of .yaml files parsed: {n_yamls_read}")
    
    # Count the total number of lines in the concatenated content
    total_lines = concatenated_content.count('\n')
    print(f"Total number of .yaml lines in tool documentation: {total_lines}")
    
    return concatenated_content


def call_llm(prompt, model_name, verbose=True):
    start_time = time.time()
    result = None
        
    if verbose:
        print(f"Calling {model_name.capitalize()} with prompt:\n{prompt}")

    if "gemini" in model_name:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        result = response.text
        print("Got response from gemini!")
    elif "gpt" in model_name:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            "max_tokens": 2000
        }
        print("polling gpt result...")
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        result = response.json()["choices"][0]["message"]["content"]
        print("gpt result: ", result)
    else:
        raise ValueError("Unsupported model_name. Use 'gemini' or 'gpt'.")

    elapsed_time = time.time() - start_time
    
    if verbose:
        print(f"---- {model_name.capitalize()} Call took {elapsed_time:.2f} seconds")
    
    return result


if __name__ == "__main__":
    root_path = "../workspaces"

    #model_name = "gpt-4o"
    model_name = "gpt-4-turbo"

    prompt = """\nCarefully investigate all the above descriptions of the Eden tools and their different options & settings. This documentation was written by very busy, human engineers that sometimes make small mistakes. I want you to scan through these descriptions and report back any likely inconsistencies you can find. 
Specifically, check that the descriptions are always clear and understandable and talking about the correct tool/option/setting they belong to. The tip can be more advanced, but it should also be talking about the same tool.
Some examples of common mistakes are:
- descriptions / tips that appear identically in multiple different tools, likely caused by copy/pasting without further adjustments
- descriptions / tips that appear to be talking about another tool/option/setting, eg when the description content really doesn't match the name of the setting/option etc.
- overly complicated and verbose descriptions that could be simplified for better user understanding (tips can be more advanced in this regard)

In general we're simply trying to find subtle mistakes / issues in this documentation that can be improved try to correct them before officially publishing this documentation. List any such inconsistencies you can spot, carefully denoting which tool they belong to (specify the full path to the .yaml!) and which entry in the tool you think is in need of a manual intervention."""

    # Step 1: Gather the contents of all .yaml files
    concatenated_yaml_content = gather_yaml_files(root_path, DELIMITER)
    # Add the concatenated yaml content to the prompt:
    prompt = f"{concatenated_yaml_content}\n\n{prompt}"
    # Save the prompt to a file:
    with open("llm_yaml_prompt.txt", "w") as f:
        f.write(prompt)

    # Step 2: Make the ChatGPT call with the concatenated YAML content and the specified prompt
    print(f"Calling {model_name} for suggestions...")
    chatgpt_output = call_llm(prompt, model_name, verbose=False)

    # Step 3: Print the output from ChatGPT
    print("=== ChatGPT Output ===")
    print(chatgpt_output)

    # Step 4: Save the output to a file:
    output_filename = f"llm_yaml_suggestions_{model_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(output_filename, "w") as f:
        f.write(chatgpt_output)

    print(f"Suggestions saved to {output_filename}!")