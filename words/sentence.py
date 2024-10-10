import yaml
import argparse
import random
from typing import Dict, List, Any

def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_sentence(template: str, data: Dict[str, Any]) -> str:
    for key, value in data.items():
        if isinstance(value, list):
            value = random.choice(value)
        template = template.replace(f'{{{key}}}', str(value))
    return template

def main():
    parser = argparse.ArgumentParser(description="Generate sentences based on YAML specifications.")
    parser.add_argument("template_yaml", help="Path to the template YAML file")
    parser.add_argument("data_yaml", help="Path to the data YAML file")
    parser.add_argument("-n", type=int, default=5, help="Number of sentences to generate")
    parser.add_argument("-o", default="sentences.yaml", help="Output file name")
    
    args = parser.parse_args()
    
    templates = load_yaml(args.template_yaml)
    data = load_yaml(args.data_yaml)
    
    sentences = []
    for _ in range(args.n):
        template = random.choice(templates['templates'])
        sentence = generate_sentence(template, data)
        sentences.append(sentence)
    
    output = {"sentences": sentences}
    
    with open(args.o, 'w') as outfile:
        yaml.dump(output, outfile, default_flow_style=False)
    
    print(f"Generated {args.n} sentences and saved to {args.o}")

if __name__ == "__main__":
    main()
