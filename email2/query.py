import yaml
import argparse
from typing import Dict, List, Any
import re

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_sentence(sentence: str, object_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    parsed = []
    for object_name, object_data in object_spec.items():
        for action, action_data in object_data['action'].items():
            pattern = action_data['sentence'].replace('{}', object_name)
            pattern = re.sub(r'\{[^}]+\}', '(.+?)', pattern)
            match = re.match(pattern, sentence)
            if match:
                parsed.append({
                    'object': object_name,
                    'action': action,
                    'params': match.groups()
                })
    return parsed

def generate_shell_command(parsed_sentence: Dict[str, Any], object_spec: Dict[str, Any]) -> str:
    object_name = parsed_sentence['object']
    action = parsed_sentence['action']
    action_spec = object_spec[object_name]['action'][action]
    shell_pattern = action_spec['shell']
    
    shell_command = shell_pattern.replace('{}', object_name)
    shell_command = shell_command.replace('{action}', action)
    
    public_fields = action_spec.get('public', {})
    for i, (field, _) in enumerate(public_fields.items()):
        if i < len(parsed_sentence['params']):
            shell_command = shell_command.replace(f'{{{field}}}', parsed_sentence['params'][i])
        else:
            shell_command = shell_command.replace(f'{{{field}}}', '')
    
    return shell_command

def process_sentence(sentence: str, object_spec: Dict[str, Any]) -> Dict[str, Any]:
    parsed_sentences = parse_sentence(sentence, object_spec)
    shell_commands = [generate_shell_command(parsed, object_spec) for parsed in parsed_sentences]
    return {
        'sentence': sentence,
        'shell': shell_commands
    }

def main():
    parser = argparse.ArgumentParser(description='Generate shell commands based on YAML specifications.')
    parser.add_argument('sentences_yaml', help='Path to the sentences.yaml file')
    parser.add_argument('object_yaml', help='Path to the object.yaml file')
    parser.add_argument('private_yaml', help='Path to the private.yaml file')
    parser.add_argument('public_yaml', help='Path to the public.yaml file')
    parser.add_argument('-o', '--output', default='query.yaml', help='Output file name')
    
    args = parser.parse_args()
    
    sentences = load_yaml(args.sentences_yaml)['sentences']
    object_spec = load_yaml(args.object_yaml)
    private_data = load_yaml(args.private_yaml)
    public_data = load_yaml(args.public_yaml)
    
    query = [process_sentence(sentence, object_spec) for sentence in sentences]
    
    output = {'query': query}
    with open(args.output, 'w') as file:
        yaml.dump(output, file, default_flow_style=False)
    
    print(f"Generated shell commands and saved them to {args.output}")

if __name__ == "__main__":
    main()
