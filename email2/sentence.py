import yaml
import argparse
import random
from typing import Dict, List, Any
import re
from datetime import datetime, timedelta

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def pluralize(word: str) -> str:
    irregular_plurals = {
        'person': 'people',
        'child': 'children',
        'ox': 'oxen',
        'man': 'men',
        'woman': 'women',
        'tooth': 'teeth',
        'foot': 'feet',
        'mouse': 'mice',
        'goose': 'geese'
    }
    
    if word in irregular_plurals:
        return irregular_plurals[word]
    elif word.endswith('y') and not word.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    elif word.endswith('f'):
        return word[:-1] + 'ves'
    elif word.endswith('fe'):
        return word[:-2] + 'ves'
    else:
        return word + 's'

def generate_default_value(value_type: str) -> str:
    if value_type == 'string':
        return 'default_string'
    elif value_type == 'datetime':
        return datetime.now().isoformat()
    elif value_type == 'number':
        return str(random.randint(1, 100))
    else:
        return 'default_value'

def get_random_value(values: List[str]) -> str:
    return random.choice(values) if values else generate_default_value('string')

def generate_sentence(object_spec: Dict[str, Any], public_data: Dict[str, Any], private_data: Dict[str, Any]) -> str:
    object_name = random.choice(list(object_spec.keys()))
    object_data = object_spec[object_name]
    
    action = object_data.get('default', random.choice(list(object_data['action'].keys())))
    action_data = object_data['action'][action]
    
    sentence_pattern = action_data['sentence']
    public_params = action_data.get('public', {})
    
    # Generowanie wartości dla parametrów publicznych
    public_values = {}
    for param, param_type in public_params.items():
        if object_name in public_data and param in public_data[object_name]:
            public_values[param] = get_random_value(public_data[object_name][param])
        else:
            public_values[param] = generate_default_value(param_type)
    
    # Przygotowanie parametrów do formatowania
    format_params = {
        'action': action,
        'many': pluralize(object_name.lower()),
        'object': object_name,
        'public': ' '.join(f'{k} "{v}"' for k, v in public_values.items())
    }
    
    # Dodanie modyfikatora, jeśli jest dostępny
    if 'modifier' in action_data:
        modifier = random.choice(list(action_data['modifier'].keys()))
        if action_data['modifier'][modifier]:
            modifier_value = random.randint(1, 10)  # Przykładowa wartość
            format_params['modifier'] = f"{modifier} {modifier_value}"
        else:
            format_params['modifier'] = modifier
    
    # Tworzenie zdania
    sentence = sentence_pattern
    for key, value in format_params.items():
        placeholder = '{' + key + '}'
        if placeholder in sentence:
            sentence = sentence.replace(placeholder, str(value))
    
    # Zastąpienie pozostałych {} nazwą obiektu
    sentence = sentence.replace('{}', object_name)
    
    # Dodawanie obiektu podrzędnego, jeśli jest wymagany
    if 'object' in action_data:
        sub_object = action_data['object']
        sub_sentence = generate_sentence({sub_object: object_spec[sub_object]}, public_data, private_data)
        sentence += f", {sub_sentence}"
    
    return sentence

def validate_sentence(sentence: str, object_spec: Dict[str, Any]) -> bool:
    for object_name, object_data in object_spec.items():
        for action, action_data in object_data['action'].items():
            pattern = re.escape(action_data['sentence'])
            pattern = pattern.replace(r'\{action\}', action)
            pattern = pattern.replace(r'\{many\}', pluralize(object_name.lower()))
            pattern = pattern.replace(r'\{object\}', object_name)
            pattern = pattern.replace(r'\{public\}', r'.*?')
            pattern = pattern.replace(r'\{modifier\}', r'(.*?\s)?')
            pattern = pattern.replace(r'\{\}', object_name)
            if re.match(f'^{pattern}(, .*)?$', sentence):
                return True
    return False

def main(object_file: str, private_file: str, public_file: str, num_sentences: int, output_file: str):
    object_spec = load_yaml(object_file)
    private_data = load_yaml(private_file)
    public_data = load_yaml(public_file)
    
    sentences = []
    while len(sentences) < num_sentences:
        sentence = generate_sentence(object_spec, public_data, private_data)
        if validate_sentence(sentence, object_spec):
            sentences.append(sentence)
    
    with open(output_file, 'w') as f:
        yaml.dump({'sentences': sentences}, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate sentences based on YAML specifications.")
    parser.add_argument("object_file", help="Path to the object.yaml file")
    parser.add_argument("private_file", help="Path to the private.yaml file")
    parser.add_argument("public_file", help="Path to the public.yaml file")
    parser.add_argument("-n", type=int, default=5, help="Number of sentences to generate")
    parser.add_argument("-o", default="sentences.yaml", help="Output file name")
    
    args = parser.parse_args()
    
    main(args.object_file, args.private_file, args.public_file, args.n, args.o)
