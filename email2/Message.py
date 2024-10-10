class Message:
    def create(self, sender, content, subject):
        print(f"Creating message:")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Content: {content}")
        # Tutaj można dodać rzeczywistą logikę tworzenia wiadomości