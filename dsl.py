import yaml
import argparse
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import inflect

p = inflect.engine()

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_example(spec: Dict[str, Any], public_data: Dict[str, Any], private_data: Dict[str, Any]) -> str:
    object_name = random.choice(list(spec.keys()))
    object_spec = spec[object_name]
    
    pattern = random.choice(object_spec['patterns'])
    example = pattern

    # Replace action placeholder
    if '{action}' in example:
        action = random.choice(list(object_spec['action'].keys()))
        example = example.replace('{action}', action)
    elif '{action:' in example:
        action_choices = example.split('{action:')[1].split('}')[0].split(',')
        action = random.choice(action_choices)
        example = example.replace(f'{{action:{",".join(action_choices)}}}', action)
    
    # Replace object placeholder
    example = example.replace('{}', object_name)
    
    # Replace public data placeholders
    for key, value in object_spec.get('public', {}).items():
        if key in public_data.get(object_name, {}):
            placeholder = f'{{{key}}}'
            if placeholder in example:
                if value == 'datetime':
                    random_date = datetime.now() + timedelta(days=random.randint(-365, 365))
                    example = example.replace(placeholder, random_date.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    example = example.replace(placeholder, f'"{random.choice(public_data[object_name][key])}"')
    
    # Replace modifiers
    if '{modifiers}' in example:
        action_spec = object_spec['action'].get(action, {})
        if 'modifier' in action_spec:
            modifier = random.choice(action_spec['modifier'])
            if isinstance(modifier, dict):
                key, value_type = list(modifier.items())[0]
                if value_type == 'integer':
                    value = random.randint(1, 10)
                    example = example.replace('{modifiers}', f'{key} {value}')
            else:
                example = example.replace('{modifiers}', modifier)
        else:
            example = example.replace('{modifiers}', '')
    
    return example.strip()

def generate_examples(spec: Dict[str, Any], public_data: Dict[str, Any], private_data: Dict[str, Any], num_examples: int) -> List[str]:
    examples = []
    for _ in range(num_examples):
        examples.append(generate_example(spec, public_data, private_data))
    return examples

def save_examples(examples: List[str], output_file: str):
    with open(output_file, 'w') as file:
        yaml.dump({'examples': examples}, file, default_flow_style=False)

def main():
    parser = argparse.ArgumentParser(description='Generate DSL examples based on YAML specifications.')
    parser.add_argument('spec_file', help='Path to the YAML specification file')
    parser.add_argument('public_file', help='Path to the public data YAML file')
    parser.add_argument('private_file', help='Path to the private data YAML file')
    parser.add_argument('-n', '--num_examples', type=int, default=5, help='Number of examples to generate')
    parser.add_argument('-o', '--output', default='examples.yaml', help='Output file for generated examples')
    
    args = parser.parse_args()
    
    spec = load_yaml(args.spec_file)
    public_data = load_yaml(args.public_file)
    private_data = load_yaml(args.private_file)
    
    examples = generate_examples(spec, public_data, private_data, args.num_examples)
    save_examples(examples, args.output)
    
    print(f"Generated {args.num_examples} examples and saved them to {args.output}")

if __name__ == "__main__":
    main()
