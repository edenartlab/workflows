
# Basic Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier for the parameter |
| `label` | Human-readable name for the parameter |
| `description` | Detailed explanation of the parameter's purpose and usage |
| `tip` | Additional advice or context for using the parameter effectively (targetted to help AI agents use the tool well) |
| `output_type` | Output type of the tool (image, video, audio) |
| `handler` | What backend the tool is running on |
| `comfyui_output_node_id` | ComfyUI output node id if applicable |

# Parameter Fields

| Field | Description |
|-------|-------------|
| `type` | Data type of the parameter (e.g., string, int, float, bool, image, video, image[], lora, audio |
| `default` | Default value for the parameter if not specified |
| `minimum` | Minimum allowed value for numeric types, or min length of array types |
| `maximum` | Maximum allowed value for numeric types, or max length of array types |
| `step` | For numeric types, specifies the increment step in the UI (e.g., 8 for width/height) |
| `choices` | List of predefined options for the parameter |

## ComfyUI Fields

| Field | Description |
|-------|-------------|
| `node_id` | Identifier for the ComfyUI node |
| `field` | Field within the node |
| `subfield` | Specific subfield within the node field |
| `preprocessing` | Any preprocessing steps required to properly parse this input (e.g., "folder" for image arrays, which saves a set of imgs to a tmp folder and passes that path in ComfyUI) |

## Special Fields

| Field | Description |
|-------|-------------|
| `hide_from_agent` | Boolean indicating whether to hide the parameter from AI agents (true/false) |
| `required` | Boolean indicating if the parameter is mandatory (true/false) |
