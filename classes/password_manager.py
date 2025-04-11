import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import time

from functions.password_functions import analyse_password_strength

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

    def _generate_key(self, password: str) -> bytes:
        password_bytes = password.encode()
        # Use a static salt for demo (in production, to use a secure random salt)
        salt = b'staticSalt123456'  # Note: In a real senarios, generate and store a unique salt

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def _load_passwords(self) -> None:
        try:
            with open(self.data_file, 'rb') as file:
                encrypted_data = file.read()

            if encrypted_data:
                # Decrypt the data
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self.passwords = json.loads(decrypted_data.decode())
                print("Passwords loaded successfully.")
            else:
                self.passwords = {}
                print("No passwords found. Starting with an empty password vault.")

        except Exception as e:
            print(f"Error loading passwords: {str(e)}")
            print("This may be due to an incorrect master password.")
            self.passwords = {}

    def save_passwords(self) -> None:
        try:
            # Convert passwords dictionary to JSON
            json_data = json.dumps(self.passwords)

            # Encrypt the JSON data
            encrypted_data = self.fernet.encrypt(json_data.encode())

            # Save to file
            with open(self.data_file, 'wb') as file:
                file.write(encrypted_data)

            print("Passwords saved successfully.")

        except Exception as e:
            print(f"Error saving passwords: {str(e)}")

    def add_password(self, service: str, username: str, password: str) -> None:
        if service not in self.passwords:
            self.passwords[service] = {}

        self.passwords[service][username] = {
            'password': password,
            'created_at': time.time(),
            'strength': analyse_password_strength(password)
        }

        print(f"Password for {service} ({username}) added successfully.")
