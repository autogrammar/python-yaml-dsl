import yaml
import sys
import re
from typing import Dict, List, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_query_command(sentence: str, objects: Dict[str, Any], code, prefix = '--') -> str:
    words = sentence.split()
    object_name = next(word for word in words if word in objects)
    action = words[0] if words[0] != object_name else words[1]
    
    object_spec = objects[object_name]
    action_spec = object_spec['action'][action]
    
    query_pattern = action_spec[code]
    
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
    
    # Format the query command
    query_command = query_pattern.format(
        object_name,
        action=action,
        modifier=modifier,
        public=' '.join(f'{prefix}{k} "{v}"' for k, v in public_params.items())
    )
    
    return query_command.strip()


def generate(sentences, objects, code, prefix):

    query_data = {
        'query': {
            'sentences': sentences,
            code: [generate_query_command(sentence, objects, code, prefix) for sentence in sentences]
        }
    }

    return query_data


def main(sentences_file: str, object_file: str, output_file: str, code: str , prefix: str):
    sentences = load_yaml(sentences_file)['sentences']
    objects = load_yaml(object_file)
    query_data = generate(sentences, objects, code, prefix)
    
    with open(output_file, 'w') as file:
        yaml.dump(query_data, file, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python query.py <sentences_file> <object_file> <output_file> <prefix_param>")
        sys.exit(1)

    code = 'shell'
    if len(sys.argv) > 4:
        code = sys.argv[4]

    prefix = '--'
    if len(sys.argv) > 5:
        prefix = sys.argv[5]

    main(sys.argv[1], sys.argv[2], sys.argv[3], code, prefix)
