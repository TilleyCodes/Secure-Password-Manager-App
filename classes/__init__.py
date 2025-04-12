"""
Initialisation file for the classes package.

This file makes the directory a Python package and allows importing from it.
"""

# Importing os for file operations
# Source: Python standard library
# Purpose: To check if files exist and handle file paths
import os
# Importing cryptography components for encryption
# Source: cryptography package - https://cryptography.io/
# Purpose: To securely encrypt and decrypt password data
from cryptography.fernet import Fernet

def __init__(self, master_password: str):
    """
    Initialie the password manager with the master password.
    
    Args:
        master_password: The master password to encrypt/decrypt the password file
    """
    # Generate a key from the master password
    self.key = self.generate_key(master_password)

    # Create Fernet cipher with the key
    self.fernet = Fernet(self.key)

    # Set up file paths
    self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(self.data_dir, exist_ok=True)
    self.data_file = os.path.join(self.data_dir, 'passwords.enc')

    # Initialise passwords dictionary
    self.passwords = {}

    # Load passwords if the file exists
    if os.path.exists(self.data_file):
        self.load_passwords()
    else:
        print("No password file found. Creating a new password vault.")
