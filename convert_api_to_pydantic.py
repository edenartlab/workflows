import os
import yaml
from collections import OrderedDict

class PreserveLongStringDumper(yaml.SafeDumper):
    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and len(value) > 80:
            style = '|'
        return super().represent_scalar(tag, value, style)

    def represent_sequence(self, tag, sequence, flow_style=None):
        # Force flow style (inline) for 'choices' sequences
        if len(sequence) > 0 and isinstance(sequence[0], str):
            flow_style = True
        return yaml.SafeDumper.represent_sequence(self, tag, sequence, flow_style)

    def represent_mapping(self, tag, mapping, flow_style=None):
        return yaml.SafeDumper.represent_mapping(self, tag, mapping, flow_style)

def convert_parameter_to_property(param):
    property_dict = OrderedDict()
    
    # Handle array types
    if 'type' in param:
        base_type = param['type'].replace('[]', '')
        is_array = param['type'].endswith('[]')
        
        type_mapping = {
            'string': 'str',
            'str': 'str',
            'int': 'int',
            'integer': 'int',
            'float': 'float',
            'bool': 'bool',
            'boolean': 'bool',
            'image': 'image',  
            'video': 'video', 
            'audio': 'audio', 
            'zip': 'zip', 
            'lora': 'lora'
        }
        
        mapped_type = type_mapping.get(base_type, base_type)
        
        if is_array:
            property_dict['type'] = 'array'
            property_dict['items'] = {'type': mapped_type} if mapped_type in ['str', 'int', 'float', 'bool'] else {"type": mapped_type}
        else:
            property_dict['type'] = mapped_type
    
    # Add all other fields
    for k, v in param.items():
        if k != 'name' and k != 'type':
            property_dict[k] = v
    
    # Handle nested comfyui field
    if 'comfyui' in property_dict:
        comfyui = property_dict['comfyui']
        property_dict['comfyui'] = OrderedDict([
            ('node_id', comfyui.get('node_id')),
            ('field', comfyui.get('field')),
            ('subfield', comfyui.get('subfield')),
        ])
        if 'preprocessing' in comfyui:
            property_dict['comfyui']['preprocessing'] = comfyui.get('preprocessing')
        if 'remap' in comfyui:
            remaps = []
            for remap in comfyui.get('remap'):
                remap2 = OrderedDict([
                    ("node_id", remap["node_id"]),
                    ("field", remap["field"]),
                    ("subfield", remap["subfield"]),
                    ("map", {})
                ])
                for r in remap["value"]:
                    remap2['map'][r["input"]] = r["output"]
                remaps.append(remap2)
            property_dict['comfyui']['remap'] = remaps
    
    return property_dict

def convert_yaml(input_file, output_file, copy_tests=False):
    with open(input_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Create initial OrderedDict with non-None values only
    new_data = OrderedDict()
    base_model = data.get('base_model')
    if base_model:
        base_model = base_model.replace("-", "_")
        
    for key, value in [
        ('name', data['name']),
        ('description', data['description']),
        ('tip', data.get('tip')),
        ('thumbnail', data.get('thumbnail')),
        ('cost_estimate', data.get('cost_estimate')),
        ('output_type', data['output_type']),
        ('resolutions', data.get('resolutions')),
        ('gpu', data.get('gpu')),
        ('handler', data.get('handler')),
        ('status', data.get('status')),
        ('visible', data.get('visible')),
        ('access', data.get('access')),
        ('replicate_model', data.get('model')),
        ('version', data.get('version')),
        ('output_handler', data.get('output_handler')),
        ('base_model', base_model),
        ('comfyui_output_node_id', data.get('comfyui_output_node_id')),
        ('comfyui_intermediate_outputs', data.get('comfyui_intermediate_outputs')),
        ('gcr_image_uri', data.get('gcr_image_uri')),
        ('machine_type', data.get('machine_type')), 
        ('gpu', data.get('gpu')),
    ]:
        if value is not None:
            new_data[key] = value
    
    new_data['parameters'] = OrderedDict()
    
    for param in data.get('parameters', []):
        name = param.pop('name')
        new_data['parameters'][name] = convert_parameter_to_property(param)
    
    # Convert comfyui_intermediate_outputs from list to dict if present
    if 'comfyui_intermediate_outputs' in data:
        intermediate_outputs = {}
        for output in data['comfyui_intermediate_outputs']:
            intermediate_outputs[output['name']] = output['node_id']
        new_data['comfyui_intermediate_outputs'] = intermediate_outputs
    
    PreserveLongStringDumper.add_representer(
        OrderedDict,
        lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items())
    )
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        yaml.dump(new_data, f, Dumper=PreserveLongStringDumper, width=float("inf"))

    if copy_tests:
        os.system(f'cp {input_file.replace("api.yaml", "test.json")} {output_file.replace("api.yaml", "test.json")}')

# Usage

input_file = "workspaces/img_tools/workflows/txt2img/api.yaml"
output_file = "workspaces/img_tools/workflows/txt2img/api2.yaml"


input_file = "../eden2/tool3/tools/musicgen/api.yaml"
output_file = "../eden2/tool3/tools/musicgen/api2.yaml"


input_file = "workspaces/video/workflows/animate_3D/api.yaml"
output_file = "workspaces/video/workflows/animate_3D/api2.yaml"




# for tool in [
#     "lora_trainer", "flux_trainer", "news", "runway", "reel", "story"
# ]:
#     input_file = f"/Users/gene/eden/dev/eden2/tools/{tool}/api.yaml"
#     output_file = input_file.replace("eden2", "eden2/tool3")
#     convert_yaml(input_file, output_file, copy_tests=True)



convert_yaml("/Users/gene/eden/dev/eden2/tools/runway/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/runway/api.yaml", copy_tests=True)
convert_yaml("/Users/gene/eden/dev/eden2/tools/reel/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/reel/api.yaml", copy_tests=True)

convert_yaml("/Users/gene/eden/dev/eden2/tool3/tools/media_utils/audio_video_combine/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/media_utils/audio_video_combine/api.yaml", copy_tests=True)
convert_yaml("/Users/gene/eden/dev/eden2/tool3/tools/media_utils/image_concat/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/media_utils/image_concat/api.yaml", copy_tests=True)
convert_yaml("/Users/gene/eden/dev/eden2/tool3/tools/media_utils/image_crop/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/media_utils/image_crop/api.yaml", copy_tests=True)
convert_yaml("/Users/gene/eden/dev/eden2/tool3/tools/media_utils/video_concat/api.yaml", "/Users/gene/eden/dev/eden2/tool3/tools/media_utils/video_concat/api.yaml", copy_tests=True)



# import os

# def find_api_yaml_files(start_path="../private_workflows0"):
#     for root, dirs, files in os.walk(start_path):
#         if "api.yaml" in files:
#             # print(root)
#             root2 = root.replace("../private_workflows0", "../private_workflows0")
#             input_file = root + "/api.yaml"
#             output_file = root2 + "/api.yaml"
#             print(input_file, output_file)
#             # check if both files exist
#             convert_yaml(input_file, output_file)
            
# find_api_yaml_files()
