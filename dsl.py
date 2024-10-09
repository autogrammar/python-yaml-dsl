import yaml
import random
from typing import List, Dict, Any


def load_yaml_spec(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def generate_sentence(pattern: str, spec: Dict[str, Any]) -> str:
    parts = pattern.split()
    result = []

    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            options = part[1:-1].split("|")
            choice = random.choice(options)

            if choice == "action":
                result.append(random.choice(get_all_actions(spec)))
            elif choice == "modifier":
                result.append(random.choice(get_all_modifiers(spec)))
            elif choice == "parameter":
                result.append(random.choice(get_all_parameters(spec)))
            elif choice == "object":
                result.append(random.choice(list(spec.keys())))
            elif choice == "property":
                entity = random.choice(list(spec.keys()))
                if "properties" in spec[entity]:
                    prop = random.choice(list(spec[entity]["properties"].keys()))
                    result.append(f"{prop}")
            else:
                result.append(choice)
        else:
            result.append(part)

    return " ".join(result)


def get_all_actions(spec: Dict[str, Any]) -> List[str]:
    actions = []
    for entity in spec.values():
        if isinstance(entity, dict) and "actions" in entity:
            actions.extend(entity["actions"])
    return list(set(actions))


def get_all_modifiers(spec: Dict[str, Any]) -> List[str]:
    modifiers = []
    for entity in spec.values():
        if isinstance(entity, dict) and "modifiers" in entity:
            modifiers.extend(entity["modifiers"].keys())
    return list(set(modifiers))


def get_all_parameters(spec: Dict[str, Any]) -> List[str]:
    parameters = []
    for entity in spec.values():
        if isinstance(entity, dict) and "parameters" in entity:
            parameters.extend(entity["parameters"])
    return list(set(parameters))


def generate_examples(spec: Dict[str, Any], num_examples: int = 5) -> List[str]:
    examples = []
    syntax_patterns = spec["Syntax"]

    for _ in range(num_examples):
        pattern = random.choice(syntax_patterns)["pattern"]
        examples.append(generate_sentence(pattern, spec))

    return examples


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate DSL sentences based on YAML specification.")
    parser.add_argument("yaml_file", help="Path to the YAML specification file")
    parser.add_argument("-n", "--num_examples", type=int, default=5, help="Number of examples to generate (default: 5)")
    args = parser.parse_args()

    try:
        spec = load_yaml_spec(args.yaml_file)
        examples = generate_examples(spec, num_examples=args.num_examples)

        print(f"Generated {args.num_examples} examples:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
    except FileNotFoundError:
        print(f"Error: The file '{args.yaml_file}' was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")