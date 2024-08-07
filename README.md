# Parameter Fields

## Basic Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier for the parameter |
| `label` | Human-readable name for the parameter |
| `description` | Detailed explanation of the parameter's purpose and usage |
| `type` | Data type of the parameter (e.g., string, int, float, bool, image, video, image[], lora) |

## Value Constraints

| Field | Description |
|-------|-------------|
| `default` | Default value for the parameter if not specified |
| `minimum` | Minimum allowed value for numeric types |
| `maximum` | Maximum allowed value for numeric types |
| `step` | Increment step for numeric types in user interfaces |
| `choices` | List of predefined options for the parameter |
| `required` | Boolean indicating if the parameter is mandatory (true/false) |

## Special Fields

| Field | Description |
|-------|-------------|
| `tip` | Additional advice or context for using the parameter effectively |
| `hide_from_agent` | Boolean indicating whether to hide the parameter from AI agents (true/false) |
| `comfyui` | Configuration for ComfyUI integration |
| - `node_id` | Identifier for the ComfyUI node |
| - `field` | Field within the node |
| - `subfield` | Specific subfield within the node field |
| - `preprocessing` | Any preprocessing steps required (e.g., "folder" for image arrays) |

## Array-specific Fields

| Field | Description |
|-------|-------------|
| `minimum` / `min_length` | Minimum number of items in an array |
| `maximum` / `max_length` | Maximum number of items in an array |

## Formatting

| Field | Description |
|-------|-------------|
| `step` | For numeric types, specifies the increment step (e.g., 8 for width/height) |

This summary covers the main parameter fields encountered in the YAML files. Each field plays a specific role in defining the behavior, constraints, and user interface representation of a parameter in the workflows.
