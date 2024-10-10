import yaml
import argparse
import random
from typing import Dict, List, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_example_sentences(spec: Dict[str, Any], public_data: Dict[str, Any], num_sentences: int = 5) -> List[str]:
    sentences = []
    objects = list(spec.keys())

    for _ in range(num_sentences):
        sentence = generate_sentence(spec, public_data, objects)
        sentences.append(sentence)

    return sentences

def generate_sentence(spec: Dict[str, Any], public_data: Dict[str, Any], objects: List[str]) -> str:
    main_object = random.choice(objects)
    action = random.choice(list(spec[main_object]['action'].keys()))
    
    sentence_pattern = spec[main_object]['action'][action]['sentence']
    public_params = spec[main_object]['action'][action].get('public', {})
    
    public_values = {}
    for k in public_params:
        if k in public_data[main_object]:
            public_values[k] = random.choice(public_data[main_object][k])
        else:
            public_values[k] = f"default_{k}"
    
    sentence_pattern = sentence_pattern.replace('{}', pluralize(main_object))
    sentence_pattern = sentence_pattern.replace('{action:read}', 'read')  # Dodaj tę linię
    sentence_pattern = sentence_pattern.replace('{action}', action)  # Zmień tę linię
    
    for key, value in public_values.items():
        sentence_pattern = sentence_pattern.replace(f'{{{key}}}', str(value))
    
    sentence = sentence_pattern
    
    if 'modifier' in spec[main_object]['action'][action]:
        modifier = random.choice(spec[main_object]['action'][action]['modifier'])
        if isinstance(modifier, dict):
            for mod_key, mod_value in modifier.items():
                sentence = sentence.replace('{many}', f"{mod_key} {random.randint(1, 10)}")
        else:
            sentence = sentence.replace('{many}', modifier)
    
    if 'object' in spec[main_object]['action'][action]:
        nested_object = random.choice(spec[main_object]['action'][action]['object'])
        nested_sentence = generate_sentence(spec, public_data, [nested_object])
        sentence += f", {nested_sentence}"
    
    return sentence

def pluralize(word: str) -> str:
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith('s') or word.endswith('x') or word.endswith('z') or word.endswith('ch') or word.endswith('sh'):
        return word + 'es'
    else:
        return word + 's'

def main():
    parser = argparse.ArgumentParser(description='Generate sentences based on YAML specifications.')
    parser.add_argument('object_yaml', help='Path to the object.yaml file')
    parser.add_argument('private_yaml', help='Path to the private.yaml file')
    parser.add_argument('public_yaml', help='Path to the public.yaml file')
    parser.add_argument('-n', type=int, default=5, help='Number of sentences to generate')
    parser.add_argument('-o', default='sentences.yaml', help='Output file name')
    
    args = parser.parse_args()
    
    spec = load_yaml(args.object_yaml)
    private_data = load_yaml(args.private_yaml)
    public_data = load_yaml(args.public_yaml)
    
    example_sentences = generate_example_sentences(spec, public_data, args.n)
    
    with open(args.o, 'w') as outfile:
        yaml.dump({'sentences': example_sentences}, outfile, default_flow_style=False)
    
    print(f"Generated {args.n} example sentences and saved them to {args.o}")

if __name__ == "__main__":
    main()
