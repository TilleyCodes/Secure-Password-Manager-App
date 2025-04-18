# Secure Password Manager CLI Application

## Table Of Contents

1. [Blog Link](#blog-link)
2. [Overview](#overview)
3. [Features and Functions](#features-and-functions)
4. [System Requirements](#system-requirements)
5. [Set Up](#set-up)
6. [Application Help](#application-help)
7. [Dependencies and Licences](#dependencies-and-licences)
8. [Application Architecture](#application-architecture)
9. [References](#references)

---

## Blog Link

[Secure Password Manager Blog](https://tilleycodes.github.io/Secure_Password_Manager_Blog/secure-password-manager-blog/)

---

## Overview

This command line interface (CLI) application is a Secure Password Manager that helps users safely store, generate, and manage passwords for various services and accounts.

The application encrypts all password data using strong cryptographic methods to ensure sensitive information remains protected. It also provides tools for generating strong passwords and analysing existing ones for security vulnerabilities.

---

## Features and Functions

- **Secure Password Storage**
  - Store passwords for various services with usernames
  - All data is encrypted using Fernet symmetric encryption
  - Passwords are protected by a single master password

- **Password Generation**
  - Create strong random passwords with customisable length and character sets
  - Passwords include a mix of lowercase, uppercase, digits, and special characters

- **Password Strength Analysis**
  - Analyse password strength based on length, character variety, and common patterns
  - Get specific feedback on how to improve weak passwords

- **Password Breach Checking**
  - Check if passwords have been exposed in known data breaches
  - Uses k-anonymity to securely check without sending the full password

- **Password Management**
  - View all stored services and usernames
  - Add, retrieve, and delete password entries
  - Save all changes securely

---

## System Requirements

- **Operating System**: 
  - macOS, Windows, or Linux
- **Python**:
  - Python 3.7 or higher
- **Storage**:
  - Minimum 10 MB free space
- **Dependencies**:
  - See [Dependencies and Licences](#dependencies-and-licences) section

---

## Set Up

This application runs in a terminal CLI and requires Python 3.7 or later installed.

### Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/TilleyCodes/Secure-Password-Manager-App
   cd secure-password-manager
   ```

2. **Set up a virtual environment (recommended)**
   
   For macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
   For Windows:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **First time setup**
   - When you first run the application, you'll be prompted to create a master password
   - This master password will be used to encrypt and decrypt your password vault
   - **Important**: Remember your master password! If lost, there's no way to recover your stored passwords

---

## Application Help

To run the application:

```bash
python main.py
```
or

```bash
python3 main.py
```

### Using the Application

When you start the application, you'll see a welcome screen and will be prompted to enter your master password. After authentication, you'll be presented with the main menu:

1. **View all services**
   - Displays a list of all saved services and their associated usernames
   - If no passwords are stored yet, you'll see a message indicating this

2. **Add new password**
   - Enter a service name (e.g., "Gmail", "Facebook")
   - Enter the username for that service
   - Choose to enter your own password or generate a secure one
   - The password will be analysed for strength and checked for breaches
   - The password will be encrypted and saved to your vault

3. **Retrieve password**
   - Enter the service name and username
   - The application will decrypt and display the password

4. **Generate secure password**
   - Specify length (default: 16 characters)
   - Choose whether to include special characters
   - View the generated password and its strength analysis
   - Optionally save the generated password for a service

5. **Check password breach**
   - Enter any password to check if it has appeared in known data breaches
   - The application uses k-anonymity to check securely

6. **Delete password**
   - Enter the service name and username to delete
   - The entry will be removed from your password vault

7. **Save and exit**
   - Save any changes and exit the application

### Tips for Secure Use

- Choose a strong master password that you don't use anywhere else
- Regularly check your passwords for breaches
- Use the password generator to create strong, unique passwords for each service
- Don't share your master password or the passwords.enc file with anyone

---

## Dependencies and Licences

The application depends on the following Python packages:

- **cryptography==44.0.2**
  - Licence: Apache Licence 2.0
  - Purpose: Provides Fernet encryption for secure password storage
  - ```pip install cryptography==44.0.2```

- **requests==2.32.3**
  - Licence: Apache Licence 2.0
  - Purpose: Used for API calls to check password breaches
  - ```pip install requests==2.32.3```

- **pycparser==2.22**
  - Licence: BSD Licence
  - Purpose: C parser in Python, dependency for cryptography
  - ```pip install pycparser==2.22```

- **cffi==1.17.1**
  - Licence: MIT Licence
  - Purpose: Foreign Function Interface for Python, dependency for cryptography
  - ```pip install cffi==1.17.1```

- **charset-normalizer==3.4.1**
  - Licence: MIT Licence
  - Purpose: Character encoding detector, dependency for requests
  - ```pip install charset-normalizer==3.4.1```

- **idna==3.10**
  - Licence: BSD Licence
  - Purpose: Internationalised Domain Names, dependency for requests
  - ```pip install idna==3.10```

- **urllib3==1.26.15**
  - Licence: MIT Licence
  - Purpose: HTTP client for Python, dependency for requests
  - ```pip install urllib3==1.26.15```

- **certifi==2025.1.31**
  - Licence: Mozilla Public Licence 2.0
  - Purpose: Provides Mozilla's CA Bundle, dependency for requests
  - ```pip install certifi==2025.1.31```

All dependencies can be installed at once using the requirements.txt file:
```bash
pip install -r requirements.txt
```

---

## Application Architecture

The application is structured with a modular design to separate concerns and enhance maintainability:

### Main Module (`main.py`)
- Entry point for the application
- Handles the main application loop and user interaction
- Orchestrates calls to the password manager class and utility functions

### Password Manager Class (`classes/password_manager.py`)
- Core functionality for password encryption, storage, and retrieval
- Uses Fernet symmetric encryption from the cryptography library
- Manages the password file and provides CRUD operations

### Password Functions (`functions/password_functions.py`)
- Utility functions for password management
- Includes password generation, strength analysis, and breach checking
- Handles UI elements like clearing the screen and displaying menus

### Data Storage
- Passwords are stored in an encrypted file `data/passwords.enc`
- The file is encrypted using a key derived from the master password
- The master password itself is never stored

### Security Features
- **Key Derivation**: Uses PBKDF2HMAC with SHA-256 and 100,000 iterations
- **Encryption**: Fernet symmetric encryption (AES-128 in CBC mode with PKCS7 padding)
- **Breach Checking**: Uses the "Have I Been Pwned" API with k-anonymity for secure checking

---

## References

- Australian Financial Review. (2025, April 4). Cyberattack launched on major Australian superannuation funds. https://www.afr.com/companies/financial-services/cyberattack-launched-on-major-australian-superannuation-funds-20250404-p5lp4l

- Corbado. (2024). Data Breaches in Australia: Statistics and Facts for 2024. https://www.corbado.com/blog/data-breaches-australia

- Cryptography.io. (2023). Fernet (symmetric encryption). [online] Available at: https://cryptography.io/en/latest/fernet/

- Cybersecurity Ventures. (2025). Intrusion Daily Cyber Threat Alert. https://cybersecurityventures.com/intrusion-daily-cyber-threat-alert/

- Hunt, T. (2022). Have I Been Pwned: API. [online] Available at: https://haveibeenpwned.com/API/v3

- OWASP. (2023). Password Storage Cheat Sheet. [online] Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

- Python Software Foundation. (2023). secrets — Generate secure random numbers for managing secrets. [online] Available at: https://docs.python.org/3/library/secrets.html

- Python Software Foundation. (2023). hashlib — Secure hashes and message digests. [online] Available at: https://docs.python.org/3/library/hashlib.html

- Python Software Foundation. (2023). getpass — Portable password input. [online] Available at: https://docs.python.org/3/library/getpass.html

- Stack Overflow. (2023). How to securely store and retrieve passwords in Python. [online] Available at: https://stackoverflow.com/questions/2490334/how-to-securely-store-password-in-python

