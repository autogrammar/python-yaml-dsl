import importlib
import inspect
import yaml
import sys

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def list_classes_and_objects():
    modules = ['Account', 'Message']  # Dodaj tutaj nazwy wszystkich modułów
    classes_and_objects = {}

    for module_name in modules:
        module = importlib.import_module(module_name)
        classes_and_objects[module_name] = {
            'classes': {},
            'objects': {},
            'variables': {}
        }

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes_and_objects[module_name]['classes'][name] = obj
            elif not name.startswith('__'):
                if callable(obj):
                    classes_and_objects[module_name]['objects'][name] = obj
                else:
                    classes_and_objects[module_name]['variables'][name] = obj

    return classes_and_objects

def execute_command(command, classes_and_objects):
    parts = command.split()
    module_name, class_name, method_name = parts[0], parts[1], parts[2]
    args = parts[3:]

    if module_name not in classes_and_objects:
        print(f"Error: Module {module_name} not found.")
        return

    if class_name not in classes_and_objects[module_name]['classes']:
        print(f"Error: Class {class_name} not found in module {module_name}.")
        return

    class_obj = classes_and_objects[module_name]['classes'][class_name]
    instance = class_obj()

    if not hasattr(instance, method_name):
        print(f"Error: Method {method_name} not found in class {class_name}.")
        return

    method = getattr(instance, method_name)
    method_args = {}
    for arg in args:
        key, value = arg.split('=')
        method_args[key] = value

    result = method(**method_args)
    print(f"Result of {module_name}.{class_name}.{method_name}: {result}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python runner.py commands.yaml")
        sys.exit(1)

    commands_file = sys.argv[1]
    commands_data = load_yaml(commands_file)

    classes_and_objects = list_classes_and_objects()

    print("Available modules, classes, objects, and variables:")
    for module_name, module_info in classes_and_objects.items():
        print(f"\nModule: {module_name}")
        print("  Classes:")
        for class_name in module_info['classes']:
            print(f"    - {class_name}")
        print("  Objects:")
        for object_name in module_info['objects']:
            print(f"    - {object_name}")
        print("  Variables:")
        for variable_name in module_info['variables']:
            print(f"    - {variable_name}")

    print("\nExecuting commands:")
    for command in commands_data['commands']:
        print(f"\nRUN: {command}")
        execute_command(command, classes_and_objects)

if __name__ == "__main__":
    main()