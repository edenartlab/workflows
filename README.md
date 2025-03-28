<div align="center">
  <img src="assets/eden.png" alt="Eden.art Logo" width="300">
  <h1>Eden.art ComfyUI Tools</h1>
</div>

## 🌿 Introduction

Welcome to the official repository of all production-ready ComfyUI workflows for [Eden.art](https://www.eden.art/). This collection powers our creative AI platform, enabling rich generative experiences through our ecosystem of creative agents.

Our mission is to build an open, collaborative platform where creators can contribute their custom tools and reach a wider audience through Eden's creative agents.

For those interested in extending our ecosystem, our public node pack is available on [GitHub](https://github.com/edenartlab/eden_comfy_pipelines).

## 🤝 Contribute Your Tools

We enthusiastically welcome contributions from the community! By adding your custom ComfyUI tools to our repository, you make them available to all Eden.art creative agents.

We're currently developing revenue-sharing models for tool builders. This means you can potentially earn from your contributions as they're used across our platform. Stay tuned for more details on this exciting opportunity.

## 🔧 How Tools Work: The api.yaml Interface

Each ComfyUI "tool" in our ecosystem comes with an `api.yaml` file that defines:
- The tool's functionality
- Required inputs
- Expected outputs

This standardized interface allows our creative agents to discover and utilize these tools through natural language conversation.

To see this in action, have a chat with [Eve](https://beta.eden.art/chat/eve), our flagship creative agent.

### Global Tool Fields

The top section of each `api.yaml` file contains global parameters that define the tool's core properties...

| Field | Description |
|-------|-------------|
| `name` | Unique identifier for the tool |
| `description` | Detailed explanation of the parameter's purpose and usage |
| `tip` | Additional advice or context for using the parameter effectively (targetted to help AI agents use the tool well) |
| `output_type` | Output type of the tool (image, video, audio, string) |
| `handler` | What backend the tool is running on |
| `comfyui_output_node_id` | ComfyUI output node id if applicable |
| `base_model` | Display the base model in the UI (flux-dev, flux-schnell, sdxl, sd15, sd3) |
| `active` | (true/false) |

## Parameter Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier for the parameter |
| `label` | Human-readable name for the parameter |
| `description` | Detailed explanation of the parameter's purpose and usage |
| `thumbnail` | url to optimized thumbnail image or vid less than 500kb. square aspect, 480 or 640, upload [here](https://us-east-1.console.aws.amazon.com/s3/buckets/edenartlab-prod-data?region=us-east-1&bucketType=general&prefix=app/&showversions=false) |
| `tip` | Additional advice or context for using the parameter effectively (targetted to help AI agents use the tool well) |
| `type` | Data type of the parameter (e.g., string, int, float, bool, image, video, image[], lora, audio) |
| `default` | Default value for the parameter if not specified |
| `minimum` | Minimum allowed value for numeric types |
| `maximum` | Maximum allowed value for numeric types |
| `min_length` | Min length of array types |
| `max_length` | Max length of array types |
| `step` | For numeric types, specifies the increment step in the UI (e.g., 8 for width/height) |
| `choices` | List of predefined options for the parameter, if applicable |
| **Special Fields** |
| `hide_from_agent` | Boolean indicating whether to hide the parameter from AI agents (true/false), defaults to false when not provided |
| `hide_from_ui` | Boolean indicating whether to hide the parameter from the Eden webapp UI (true/false), defaults to false when not provided |
| `required` | Boolean indicating if the parameter is mandatory (true/false), defaults to false when not provided |
| comfyui: |
| `node_id` | Identifier for the ComfyUI node |
| `field` | Field within the node |
| `subfield` | Specific subfield within the node field |
| `preprocessing` | Any preprocessing steps required to properly parse this input (e.g., "folder" for image arrays, which saves a set of imgs to a tmp folder and passes that path in ComfyUI) |

Making toggle menus with folded parameters in the UI:
`requires the toggle to start with use_ `

Remapping labels to multiple nodes example:
```
- name: preprocessor1
  label: Controlnet1 preprocessor
  description: Type of controlnet preprocessor. Examples can be seen at https://github.com/lllyasviel/ControlNet-v1-1-nightly?tab=readme-ov-file#controlnet-11-depth
  tip:  depth will try to maintain the perceived depth of the input scene. Canny edge creates strong edges adhering to the shape of your image, whereas scribble will create guidance towards a rougher sketched shape of your starting image and often produces better quality video at the cost of less finegrained correspondence with the control image. Pose will try to extract the pose from a person and inject it into the video.
  type: string
  visible_if: use_controlnet1=true
  default: CannyEdgePreprocessor
  choices: [CannyEdgePreprocessor, DepthAnythingV2Preprocessor, AnyLineArtPreprocessor_aux, DensePosePreprocessor, Scribble_XDoG_Preprocessor, none]
  choices_labels: [Edges (Canny), Depth, Lineart, human pose, Scribble lines, Luminance (QR dark/bright patterns)]
  comfyui: 
    node_id: 406
    field: inputs
    subfield: preprocessor    
    remap:
      - node_id: 107
        field: inputs
        subfield: control_net_name
        value:
          - input: CannyEdgePreprocessor
            output: control_v11p_sd15_canny.pth
          - input: DepthAnythingV2Preprocessor
            output: control_v11f1p_sd15_depth.pth
          - input: AnyLineArtPreprocessor_aux
            output: control_v11p_sd15_lineart.pth
          - input: DensePosePreprocessor
            output: control_v11p_sd15_openpose.pth
          - input: Scribble_XDoG_Preprocessor
            output: control_v11p_sd15_scribble.pth
          - input: none
            output: controlnetQRPatternQR_v2Sd15.safetensors
```
