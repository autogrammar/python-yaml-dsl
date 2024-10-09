import yaml
import random
from typing import List, Dict, Any
import itertools


def load_yaml_spec(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def save_examples(examples: List[str], file_path: str):
    with open(file_path, 'w') as file:
        yaml.dump({"examples": examples}, file, default_flow_style=False)


def generate_patterns(spec: Dict[str, Any]) -> List[str]:
    patterns = []

    for entity, details in spec.items():
        # Basic patterns for each entity
        if "actions" in details:
            for action in details["actions"]:
                patterns.append(f"{{{action}}} {entity}")

                # Add patterns with prefixes
                if "prefix" in details:
                    for prefix in details["prefix"]:
                        patterns.append(f"{{{action}}} {prefix} {entity}")

                # Add patterns with suffixes
                if "suffix" in details:
                    for suffix in details["suffix"]:
                        patterns.append(f"{{{action}}} {entity} {suffix}")

                # Add patterns with properties
                if "properties" in details:
                    for prop in details["properties"]:
                        patterns.append(f"{{{action}}} {entity} from {{{prop}}}")

                # Add patterns with modifiers and parameters
                if "modifiers" in details:
                    for modifier in details["modifiers"]:
                        patterns.append(f"{{{action}}} {{{modifier}}} {entity}")

                if "parameters" in details:
                    for param in details["parameters"]:
                        patterns.append(f"{{{action}}} {{{param}}} {entity}")

                # Add patterns with combinations of modifiers/parameters and properties
                if "properties" in details and ("modifiers" in details or "parameters" in details):
                    modifiers_params = details.get("modifiers", {}).keys() | set(details.get("parameters", []))
                    for mod_param, prop in itertools.product(modifiers_params, details["properties"]):
                        patterns.append(f"{{{action}}} {{{mod_param}}} {entity} from {{{prop}}}")

        # Patterns for relationships
        if "hasMany" in details:
            for related_entity in details["hasMany"]:
                patterns.append(f"{{{related_entity}}} from {entity}")

    # Patterns for entities with 'prefix' attribute
    entities_with_prefix = [entity for entity, details in spec.items() if "prefix" in details]
    for entity1, entity2 in itertools.permutations(entities_with_prefix, 2):
        prefix = random.choice(spec[entity1]["prefix"])
        patterns.append(f"{{{entity2}}} {prefix} {entity1}")

    return list(set(patterns))  # Remove duplicates


def generate_sentence(pattern: str, spec: Dict[str, Any]) -> str:
    parts = pattern.split()
    result = []

    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            key = part[1:-1]
            if key in spec:
                result.append(key)
            else:
                for entity, details in spec.items():
                    if key in details.get("actions", []):
                        result.append(key)
                        break
                    elif key in details.get("properties", {}):
                        result.append(f"{key}:{random.choice(list(details['properties'].keys()))}")
                        break
                    elif key in details.get("modifiers", {}):
                        result.append(f"{key}:{random.randint(1, 10)}")
                        break
                    elif key in details.get("parameters", []):
                        result.append(key)
                        break
                else:
                    result.append(key)
        else:
            result.append(part)

    return " ".join(result)


def generate_examples(spec: Dict[str, Any], num_examples: int = 5) -> List[str]:
    patterns = generate_patterns(spec)
    examples = []

    for _ in range(num_examples):
        pattern = random.choice(patterns)
        examples.append(generate_sentence(pattern, spec))

    return examples


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate DSL sentences based on YAML specification.")
    parser.add_argument("yaml_file", help="Path to the YAML specification file")
    parser.add_argument("-n", "--num_examples", type=int, default=5, help="Number of examples to generate (default: 5)")
    parser.add_argument("-o", "--output", default="examples.yaml",
                        help="Output file for generated examples (default: examples.yaml)")
    args = parser.parse_args()

    try:
        spec = load_yaml_spec(args.yaml_file)
        examples = generate_examples(spec, num_examples=args.num_examples)

        print(f"Generated {args.num_examples} examples:")
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")

        save_examples(examples, args.output)
        print(f"\nExamples saved to {args.output}")

    except FileNotFoundError:
        print(f"Error: The file '{args.yaml_file}' was not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")