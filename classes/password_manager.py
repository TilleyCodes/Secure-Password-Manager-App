import os

class PasswordManager:
    def __init__(self, master_password: str):
        self.data_file = 'data/passwords.enc'
        self.master_password = master_password
        self.passwords = {}
        self.encryption_key = self._generate_key(master_password)
        self.fernet = Fernet(self.encryption_key)

        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        # Load existing passwords if file exists
        if os.path.exists(self.data_file):
            self._load_passwords()