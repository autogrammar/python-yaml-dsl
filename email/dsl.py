import yaml
import argparse
import random
from datetime import datetime
from typing import Dict, List, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data: List[str], file_path: str):
    with open(file_path, 'w') as file:
        yaml.dump({"examples": data}, file, default_flow_style=False)

def generate_value(value_type: str) -> Any:
    if value_type == 'string':
        return "default_string"
    elif value_type == 'integer':
        return random.randint(1, 100)
    elif value_type == 'datetime':
        return datetime.now().isoformat()
    elif value_type == 'number':
        return random.uniform(1, 100)
    else:
        return "default_value"

def get_random_value(values: List[str]) -> str:
    return random.choice(values)

def pluralize(word: str) -> str:
    # Podstawowe reguły tworzenia liczby mnogiej w języku angielskim
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    else:
        return word + 's'

def generate_example(spec: Dict[str, Any], public_data: Dict[str, Any], object_name: str) -> str:
    pattern = random.choice(spec[object_name]['patterns'])
    result = []

    for part in pattern.split():
        if part.startswith('{') and part.endswith('}'):
            key = part[1:-1]
            if ':' in key:
                key, value = key.split(':')
            else:
                value = None

            if key == 'action':
                if value:
                    action = value
                else:
                    action_type = random.choice(list(spec[object_name]['action'].keys()))
                    action = get_random_value(spec[object_name]['action'][action_type])
                result.append(action)
            elif key == 'many':
                if 'many' in spec[object_name]:
                    many_option = random.choice(spec[object_name]['many'])
                    if isinstance(many_option, dict):
                        result.append(f"last {generate_value('integer')}")
                    else:
                        result.append(many_option)
            elif key == 'public':
                for public_key, public_type in spec[object_name]['public'].items():
                    if public_key in public_data[object_name]:
                        value = get_random_value(public_data[object_name][public_key])
                    else:
                        value = generate_value(public_type)
                    result.append(f"{public_key} \"{value}\"")
            elif key == 'object':
                nested_object = random.choice(spec[object_name]['object'])
                result.append(generate_example(spec, public_data, nested_object))
            elif key == '':
                result.append(object_name)
        else:
            result.append(part)

    return ' '.join(result)

def main():
    parser = argparse.ArgumentParser(description='Generate DSL examples based on YAML specifications.')
    parser.add_argument('spec_file', help='Path to the YAML specification file')
    parser.add_argument('private_file', help='Path to the private YAML file')
    parser.add_argument('public_file', help='Path to the public YAML file')
    parser.add_argument('-n', '--num_examples', type=int, default=5, help='Number of examples to generate')
    parser.add_argument('-o', '--output', default='examples.yaml', help='Output file for generated examples')
    args = parser.parse_args()

    spec = load_yaml(args.spec_file)
    private_data = load_yaml(args.private_file)
    public_data = load_yaml(args.public_file)

    examples = []
    for _ in range(args.num_examples):
        root_object = random.choice(list(spec.keys()))
        example = generate_example(spec, public_data, root_object)
        examples.append(example)

    save_yaml(examples, args.output)
    print(f"Generated {args.num_examples} examples and saved them to {args.output}")

if __name__ == "__main__":
    main()
