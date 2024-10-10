import yaml
import sys
from Account import Account
from Message import Message

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_command(command):
    parts = command.split()
    module, action = parts[0], parts[1]
    args = {}
    for i in range(2, len(parts), 2):
        if i + 1 < len(parts):
            key = parts[i].lstrip('--')
            value = parts[i + 1].strip('"')
            args[key] = value
    return module, action, args

def execute_command(module, action, args, private_data):
    if module == 'Account.py':
        account = Account()
        if action == 'connect':
            email = args['email']
            account.connect(email=email)
        elif action == 'disconnect':
            account.disconnect(**args)
    elif module == 'Message.py':
        message = Message()
        if action == 'create':
            required_args = {'sender', 'content', 'subject'}
            if not all(arg in args for arg in required_args):
                missing_args = required_args - set(args.keys())
                print(f"Error: Missing required arguments for Message.create(): {', '.join(missing_args)}")
                return
            message.create(
                sender=args['sender'],
                content=args['content'],
                subject=args['subject']
            )
        elif action == 'read':
            message.read(**args)
        elif action == 'delete':
            message.delete(**args)

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py query.yaml")
        sys.exit(1)

    query_file = sys.argv[1]
    query_data = load_yaml(query_file)
    private_data = load_yaml('private.yaml')

    for command in query_data['query']['python']:
        module, action, args = parse_command(command)
        execute_command(module, action, args, private_data)

if __name__ == "__main__":
    main()