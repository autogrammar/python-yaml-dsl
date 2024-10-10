class Message:
    def create(self, sender, summary, subject):
        print(f"Creating message:")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Content: {summary}")
        # Tutaj można dodać rzeczywistą logikę tworzenia wiadomości