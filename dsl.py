import yaml
import random
from typing import List, Dict, Any
import itertools


def load_yaml_spec(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_properties(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_examples(examples: List[str], file_path: str):
    with open(file_path, 'w') as file:
        yaml.dump({"examples": examples}, file, default_flow_style=False)

def generate_sentence(pattern: str, spec: Dict[str, Any], properties: Dict[str, Any]) -> str:
    parts = pattern.split()
    result = []

    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            key = part[1:-1]
            if ":" in key:
                key, value_type = key.split(":")
                if value_type == "integer":
                    result.append(f"{key}:{random.randint(1, 10)}")
                elif value_type == "boolean":
                    result.append(f"{key}")
            elif "." in key:
                entity, prop_type = key.split(".")
                if prop_type == "properties" and entity in properties:
                    prop = random.choice(list(properties[entity].keys()))
                    value = random.choice(properties[entity][prop])
                    result.append(f'{prop} "{value}"')
            elif key in spec:
                if key == "Account" and "Account" in properties:
                    email = random.choice(properties["Account"]["email"])
                    result.append(f'Account email "{email}"')
                else:
                    result.append(key)
            else:
                for entity, details in spec.items():
                    if key in details.get("properties", {}):
                        if key in properties.get(entity, {}):
                            value = random.choice(properties[entity][key])
                            result.append(f'{key} "{value}"')
                        else:
                            result.append(f"{key}:{random.choice(list(details['properties'].keys()))}")
                        break
                    elif key in details.get("modifiers", {}):
                        if key == "last":
                            result.append(f"last:{random.randint(1, 10)}")
                        else:
                            result.append(key)
                        break
                    elif key in details.get("parameters", []):
                        result.append(key)
                        break
                else:
                    result.append(key)
        else:
            result.append(part)

    return " ".join(result)

def generate_examples(spec: Dict[str, Any], properties: Dict[str, Any], num_examples: int = 5) -> List[str]:
    patterns = generate_patterns(spec)
    examples = []

    for _ in range(num_examples):
        pattern = random.choice(patterns)
        examples.append(generate_sentence(pattern, spec, properties))

    return examples

def generate_patterns(spec: Dict[str, Any]) -> List[str]:
    patterns = []

    for entity, details in spec.items():
        if "actions" in details:
            for action in details["actions"]:
                if isinstance(action, dict):
                    for main_action, sub_actions in action.items():
                        base_pattern = f"{main_action} {entity}"
                        patterns.append(base_pattern)
                        for sub_action in sub_actions:
                            patterns.append(f"{main_action} {{{sub_action}}} {entity}")
                else:
                    base_pattern = f"{action} {entity}"
                    patterns.append(base_pattern)

                if "properties" in details:
                    for prop in details["properties"]:
                        patterns.append(f"{base_pattern} {{{prop}}}")

                if "parameters" in details:
                    for param in details["parameters"]:
                        patterns.append(f"{base_pattern} {param} {{{entity}}}")

                if "prefix" in details:
                    for prefix in details["prefix"]:
                        patterns.append(f"{prefix} {base_pattern}")

                if "suffix" in details:
                    for suffix in details["suffix"]:
                        patterns.append(f"{base_pattern} {suffix}")

                if "modifiers" in details:
                    for modifier in details["modifiers"]:
                        patterns.append(f"{base_pattern} {{{modifier}}}")

        if "hasMany" in details:
            for related_entity in details["hasMany"]:
                patterns.append(f"{{{related_entity}}} from {entity}")

    return list(set(patterns))  # Remove duplicates

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate DSL sentences based on YAML specification.")
    parser.add_argument("yaml_file", help="Path to the YAML specification file")
    parser.add_argument("properties_file", help="Path to the properties YAML file")
    parser.add_argument("-n", "--num_examples", type=int, default=5, help="Number of examples to generate (default: 5)")
    parser.add_argument("-o", "--output", default="examples.yaml",
                        help="Output file for generated examples (default: examples.yaml)")
    args = parser.parse_args()

    try:
        spec = load_yaml_spec(args.yaml_file)
        properties = load_properties(args.properties_file)
        examples = generate_examples(spec, properties, num_examples=args.num_examples)

        print(f"Generated {args.num_examples} examples:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")

        save_examples(examples, args.output)
        print(f"\nExamples saved to {args.output}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")