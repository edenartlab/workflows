import yaml
from collections import OrderedDict

class PreserveLongStringDumper(yaml.SafeDumper):
    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and len(value) > 80:
            style = '|'
        return super().represent_scalar(tag, value, style)

    def represent_mapping(self, tag, mapping, flow_style=None):
        return yaml.SafeDumper.represent_mapping(self, tag, mapping, flow_style)

def convert_parameter_to_property(param):
    property_dict = OrderedDict()
    
    # Ensure 'type' is the first field
    if 'type' in param:
        type_mapping = {
            'string': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'image': 'str',  # Assuming image is represented as a string (path or URL)
            'lora': 'str'    # Assuming lora is represented as a string
        }
        property_dict['type'] = type_mapping.get(param['type'], param['type'])
    
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
            ('subfield', comfyui.get('subfield'))
        ])
    
    return property_dict

def convert_yaml(input_file, output_file):
    with open(input_file, 'r') as f:
        data = yaml.safe_load(f)
    
    new_data = OrderedDict([
        ('name', data.get('name', '')),
        ('description', data.get('description', '')),
        ('tip', data.get('tip', '')),
        ('cost_estimate', data.get('cost_estimate', '')),
        ('comfyui_output_node', data.get('comfyui_output_node_id', '')),
        ('comfyui_intermediate_outputs', data.get('comfyui_intermediate_outputs', {})),
        ('properties', OrderedDict())
    ])
    
    for param in data.get('parameters', []):
        name = param.pop('name')
        new_data['properties'][name] = convert_parameter_to_property(param)
    
    PreserveLongStringDumper.add_representer(
        OrderedDict,
        lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items())
    )
    
    with open(output_file, 'w') as f:
        yaml.dump(new_data, f, Dumper=PreserveLongStringDumper, width=float("inf"))

# Usage

input_file = "workspaces/img_tools/workflows/txt2img/api.yaml"

output_file = "workspaces/img_tools/workflows/txt2img/api2.yaml"
convert_yaml(input_file, output_file)
