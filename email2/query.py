import yaml
import sys
import re
from typing import Dict, List, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_shell_command(sentence: str, objects: Dict[str, Any], prefix = '--') -> str:
    words = sentence.split()
    object_name = next(word for word in words if word in objects)
    action = words[0] if words[0] != object_name else words[1]
    
    object_spec = objects[object_name]
    action_spec = object_spec['action'][action]
    
    shell_pattern = action_spec['shell']
    
    # Extract public parameters
    public_params = {}
    for param, param_type in action_spec.get('public', {}).items():
        param_pattern = rf'{param} "([^"]*)"'
        match = re.search(param_pattern, sentence)
        if match:
            public_params[param] = match.group(1)
    
    # Handle modifier if present
    modifier = ''
    if 'modifier' in action_spec:
        for mod in action_spec['modifier']:
            if mod in sentence:
                modifier = mod
                break
    
    # Format the shell command
    shell_command = shell_pattern.format(
        object_name,
        action=action,
        modifier=modifier,
        public=' '.join(f'{prefix}{k} "{v}"' for k, v in public_params.items())
    )
    
    return shell_command.strip()

def main(sentences_file: str, object_file: str, output_file: str, prefix: str):
    sentences = load_yaml(sentences_file)['sentences']
    objects = load_yaml(object_file)
    
    query_data = {
        'query': {
            'sentences': sentences,
            'shell': [generate_shell_command(sentence, objects, prefix) for sentence in sentences]
        }
    }
    
    with open(output_file, 'w') as file:
        yaml.dump(query_data, file, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python query.py <sentences_file> <object_file> <output_file> <prefix_param>")
        sys.exit(1)

    prefix = '--'
    if len(sys.argv) > 4:
        prefix = sys.argv[4]

    main(sys.argv[1], sys.argv[2], sys.argv[3], prefix)
