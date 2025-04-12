# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught

import os
import base64
import json
import time
from typing import List, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
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

    def get_password(self, service: str, username: str) -> Optional[str]:
        if service in self.passwords and username in self.passwords[service]:
            return self.passwords[service][username]['password']
        return None

    def list_services(self) -> List[str]:
        return list(self.passwords.keys())

    def list_usernames(self, service: str) -> List[str]:
        if service in self.passwords:
            return list(self.passwords[service].keys())
        return []

    def delete_password(self, service: str, username: str) -> bool:
        if service in self.passwords and username in self.passwords[service]:
            del self.passwords[service][username]

            # Remove the service if no usernames left
            if not self.passwords[service]:
                del self.passwords[service]

            print(f"Password for {service} ({username}) deleted successfully.")
            return True

        print(f"Password for {service} ({username}) not found.")
        return False
    