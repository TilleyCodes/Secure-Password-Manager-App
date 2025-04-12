# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught

"""This module defines the PasswordManager class for securely managing and storing passwords."""

# Importing os for file operations
# Source: Python standard library
# Purpose: To check if files exist and handle file paths
import os
# Importing base64 for encoding binary data
# Source: Python standard library
# Purpose: To encode encryption keys in a safe format
import base64
# Importing json for data serialisation
# Source: Python standard library
# Purpose: To store password data in a structured format
import json
# Importing time for timestamp creation
# Source: Python standard library
# Purpose: To record when passwords were created or modified
import time

# Importing typing for type hints
# Source: Python standard library
# Purpose: To provide clear type information for better code understanding
from typing import List, Optional

# Importing cryptography components for encryption
# Source: cryptography package - https://cryptography.io/
# Purpose: To securely encrypt and decrypt password data
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Importing password functions
# Source: local module - functions/password_functions.py
# Purpose: To use the password analysis functionality
from functions.password_functions import analyse_password_strength

class PasswordManager:
    """
    Main class for managing passwords with encryption.
    
    This class handles all operations related to password management including
    encryption/decryption, storage, retrieval, and analysis.
    
    Attributes:
        data_file (str): The file path where encrypted passwords are stored
        master_password (str): The password used to generate the encryption key
        passwords (dict): Dictionary containing all password data
        encryption_key (bytes): Generated encryption key from master password
        fernet (Fernet): Encryption/decryption object
    """

    def __init__(self, master_password: str):
        """
        Initialise the password manager with a master password.
        
        Args:
            master_password: The master password used for encryption/decryption
            
        Note:
            If a password file already exists, it will be loaded automatically
        """
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
        """
        Generate an encryption key from the master password.
        
        Uses PBKDF2HMAC to derive a secure key from the password.
        
        Args:
            password: The master password
            
        Returns:
            A bytes object containing the encryption key
        """
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
        """
        Load and decrypt passwords from the encrypted file.
        
        Decrypts the stored password file using the master password.
        If the master password is incorrect, decryption will fail.
        
        Raises:
            Exception: If decryption fails due to incorrect master password
        """
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
        """
        Encrypt and save passwords to the data file.
        
        Converts the passwords dictionary to JSON, encrypts it,
        and saves it to the data file.
        """
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
        """
        Add a new password entry.
        
        Args:
            service: The name of the service or website
            username: The username for the service
            password: The password to store
        """
        if service not in self.passwords:
            self.passwords[service] = {}

        self.passwords[service][username] = {
            'password': password,
            'created_at': time.time(),
            'strength': analyse_password_strength(password)
        }

        print(f"Password for {service} ({username}) added successfully.")

    def get_password(self, service: str, username: str) -> Optional[str]:
        """
        Retrieve a password for a specific service and username.
        
        Args:
            service: The name of the service or website
            username: The username for the service
            
        Returns:
            The password if found, None otherwise
        """
        if service in self.passwords and username in self.passwords[service]:
            return self.passwords[service][username]['password']
        return None

    def list_services(self) -> List[str]:
        """
        Get a list of all stored services.
        
        Returns:
            A list of service names
        """
        return list(self.passwords.keys())

    def list_usernames(self, service: str) -> List[str]:
        """
        Get a list of usernames for a specific service.
        
        Args:
            service: The name of the service or website
            
        Returns:
            A list of usernames
        """
        if service in self.passwords:
            return list(self.passwords[service].keys())
        return []

    def delete_password(self, service: str, username: str) -> bool:
        """
        Delete a password entry.
        
        Args:
            service: The name of the service or website
            username: The username for the service
            
        Returns:
            True if the password was deleted, False otherwise
        """
        if service in self.passwords and username in self.passwords[service]:
            del self.passwords[service][username]

            # Remove the service if no usernames left
            if not self.passwords[service]:
                del self.passwords[service]

            print(f"Password for {service} ({username}) deleted successfully.")
            return True

        print(f"Password for {service} ({username}) not found.")
        return False
    