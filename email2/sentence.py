import yaml
import argparse
import random
from typing import Dict, List, Any
import re
from datetime import datetime, timedelta

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_default_value(value_type: str) -> Any:
    if value_type == 'string':
        return "default_string"
    elif value_type == 'integer':
        return random.randint(1, 100)
    elif value_type == 'number':
        return round(random.uniform(1, 100), 2)
    elif value_type == 'datetime':
        return datetime.now().isoformat()
    else:
        return "default_value"

def get_public_value(public_data: Dict[str, Any], object_name: str, field: str) -> str:
    if object_name in public_data and field in public_data[object_name]:
        return random.choice(public_data[object_name][field])
    return generate_default_value('string')

def generate_sentence(object_spec: Dict[str, Any], action: str, object_name: str, public_data: Dict[str, Any]) -> str:
    action_spec = object_spec['action'][action]
    sentence_pattern = action_spec['sentence']
    
    public_fields = action_spec.get('public', {})
    public_values = []
    for field, value_type in public_fields.items():
        value = get_public_value(public_data, object_name, field)
        public_values.append(f'{field} "{value}"')
    
    public_str = " ".join(public_values)
    
    modifier = ""
    if 'modifier' in action_spec:
        modifier_type = random.choice(list(action_spec['modifier'].keys()))
        if action_spec['modifier'][modifier_type]:
            modifier_value = generate_default_value(action_spec['modifier'][modifier_type])
            modifier = f"{modifier_type} {modifier_value}"
        else:
            modifier = modifier_type
    
    # Replace placeholders with actual values
    sentence = sentence_pattern.replace("{action}", action)
    sentence = sentence.replace("{modifier}", modifier)
    sentence = sentence.replace("{public}", public_str)
    sentence = sentence.replace("{}", object_name)
    
    # Handle optional parts
    sentence = re.sub(r'\((.*?)\)', lambda m: random.choice(['', m.group(1)]), sentence)
    
    return sentence.strip()

def generate_sentences(spec: Dict[str, Any], public_data: Dict[str, Any], num_sentences: int) -> List[str]:
    sentences = []
    for _ in range(num_sentences):
        object_name = random.choice(list(spec.keys()))
        object_spec = spec[object_name]
        action = random.choice(list(object_spec['action'].keys()))
        
        sentence = generate_sentence(object_spec, action, object_name, public_data)

        dependent_object = ''
        if 'object' in object_spec:
            dependent_object = object_spec['object']

        if 'object' in object_spec['action'][action]:
            dependent_object = object_spec['action'][action]['object']

        if len(dependent_object):

            print(dependent_object)
            # check if dependent_object is type dict
            # just for selected action is available in dependent_object
            if isinstance(dependent_object, dict):
                for dependent_object_name, dependent_object_action in dependent_object.items():
                    dependent_action = random.choice(list(spec[dependent_object_name]['action'].keys()))

                    if dependent_object_action == dependent_action:
                        dependent_action = random.choice(list(spec[dependent_object_name]['action'].keys()))
                        dependent_sentence = generate_sentence(spec[dependent_object_name], dependent_action,
                                                               dependent_object_name, public_data)
                        sentence += f", {dependent_sentence}"
            else:
                # for all actions
                dependent_action = random.choice(list(spec[dependent_object]['action'].keys()))
                dependent_sentence = generate_sentence(spec[dependent_object], dependent_action, dependent_object,
                                                       public_data)
                sentence += f", {dependent_sentence}"

        sentences.append(sentence)
    
    return sentences

def main():
    parser = argparse.ArgumentParser(description='Generate sentences based on YAML specifications.')
    parser.add_argument('object_yaml', help='Path to the object.yaml file')
    parser.add_argument('private_yaml', help='Path to the private.yaml file')
    parser.add_argument('public_yaml', help='Path to the public.yaml file')
    parser.add_argument('-n', '--num_sentences', type=int, default=5, help='Number of sentences to generate')
    parser.add_argument('-o', '--output', default='sentences.yaml', help='Output file name')
    
    args = parser.parse_args()
    
    object_spec = load_yaml(args.object_yaml)
    private_data = load_yaml(args.private_yaml)
    public_data = load_yaml(args.public_yaml)
    
    sentences = generate_sentences(object_spec, public_data, args.num_sentences)
    
    output = {'sentences': sentences}
    with open(args.output, 'w') as file:
        yaml.dump(output, file, default_flow_style=False)
    
    print(f"Generated {args.num_sentences} sentences and saved them to {args.output}")

if __name__ == "__main__":
    main()
