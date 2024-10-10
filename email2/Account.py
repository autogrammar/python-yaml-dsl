import yaml

class Account:
    def __init__(self):
        self.private_data = self.load_private_data()

    def load_private_data(self):
        with open('private.yaml', 'r') as file:
            return yaml.safe_load(file)['Account']['email']

    def connect(self, email):
        if email in self.private_data:
            account_data = self.private_data[email]
            print(f"Connecting to account: {email}")
            print(f"Server: {account_data['server']}")
            print(f"Username: {account_data['username']}")
            print(f"Port: {account_data['port']}")
            # Tutaj można dodać rzeczywistą logikę połączenia
        else:
            print(f"No data found for email: {email}")

    def disconnect(self, email):
        if email in self.private_data:
            print(f"Disconnecting from account: {email}")
            # Tutaj można dodać rzeczywistą logikę rozłączenia
        else:
            print(f"No data found for email: {email}")