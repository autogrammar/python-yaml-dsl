import argparse
import yaml
import random
from typing import List, Dict, Any
import re
from inflection import singularize

class DSLBuilder:
    def __init__(self, object_yaml: str, public_yaml: str, private_yaml: str):
        with open(object_yaml, 'r') as f:
            self.object_spec = yaml.safe_load(f)
        with open(public_yaml, 'r') as f:
            self.public_data = yaml.safe_load(f)
        with open(private_yaml, 'r') as f:
            self.private_data = yaml.safe_load(f)

    def generate_sentences(self, num_sentences: int) -> List[str]:
        sentences = []
        for _ in range(num_sentences):
            sentence = self.generate_sentence()
            sentences.append(sentence)
        return sentences

    def generate_sentence(self) -> str:
        root_object = random.choice(list(self.object_spec.keys()))
        return self.generate_object_sentence(root_object)

    def generate_object_sentence(self, object_name: str) -> str:
        object_spec = self.object_spec[object_name]
        action = object_spec.get('default', random.choice(list(object_spec['action'].keys())))
        action_spec = object_spec['action'][action]

        sentence_pattern = action_spec['sentence']
        public_params = self.generate_public_params(object_name, action_spec.get('public', {}))

        sentence = sentence_pattern.format(action=action, **public_params)
        sentence = sentence.replace('{}', object_name)

        if 'object' in action_spec:
            nested_object = random.choice(action_spec['object'])
            nested_sentence = self.generate_object_sentence(nested_object)
            sentence += f", {nested_sentence}"

        if 'modifier' in action_spec:
            modifier = random.choice(action_spec['modifier'])
            if isinstance(modifier, dict):
                modifier_key = list(modifier.keys())[0]
                modifier_value = random.randint(1, 100)
                sentence = sentence.replace('{many}', f"{modifier_key} {modifier_value}")
            else:
                sentence = sentence.replace('{many}', modifier)

        return sentence

    def generate_public_params(self, object_name: str, public_spec: Dict[str, Any]) -> Dict[str, str]:
        params = {}
        for param, param_type in public_spec.items():
            if param_type == 'string':
                params[param] = random.choice(self.public_data[object_name][param])
            elif param_type == 'datetime':
                params[param] = "2023-05-01 12:00:00"  # Placeholder for datetime
            elif param_type == 'number':
                params[param] = str(random.randint(1, 1000))
        return params

def main():
    parser = argparse.ArgumentParser(description="DSL Builder")
    parser.add_argument("object_yaml", help="Path to the object YAML file")
    parser.add_argument("public_yaml", help="Path to the public YAML file")
    parser.add_argument("private_yaml", help="Path to the private YAML file")
    parser.add_argument("-n", "--num_sentences", type=int, default=5, help="Number of sentences to generate")
    parser.add_argument("-o", "--output", default="sentences.yaml", help="Output file for generated sentences")

    args = parser.parse_args()

    dsl_builder = DSLBuilder(args.object_yaml, args.public_yaml, args.private_yaml)
    sentences = dsl_builder.generate_sentences(args.num_sentences)

    with open(args.output, 'w') as f:
        yaml.dump({"sentences": sentences}, f)

    print(f"Generated {args.num_sentences} sentences and saved them to {args.output}")

if __name__ == "__main__":
    main()