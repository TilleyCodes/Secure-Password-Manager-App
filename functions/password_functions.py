# pylint: disable=broad-exception-caught

"""This module provides utility functions for password management, generation, and analysis."""

# Importing os for clearing screen
# Source: Python standard library
# Purpose: To clear the terminal screen for better UI
import os
# Importing random for generating random passwords
# Source: Python standard library
# Purpose: To create secure random passwords with various character sets
import random
# Importing string for character sets
# Source: Python standard library
# Purpose: To access predefined character sets for password generation
import string
# Importing re for regular expressions
# Source: Python standard library
# Purpose: To analyse password patterns and complexity
import re
# Importing hashlib for SHA-1 hashing
# Source: Python standard library
# Purpose: To hash passwords for secure breach checking
import hashlib
# Importing typing for type hints
# Source: Python standard library
# Purpose: To provide clear type information for better code understanding
from typing import Dict, List, Optional, Tuple, Union
# Importing requests for API calls
# Source: requests package - https://docs.python-requests.org/
# Purpose: To check if passwords have been compromised using external API
import requests


def clear_screen() -> None:
    """
    Clear the console screen.
    
    Uses the appropriate command based on the operating system
    to clear the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header() -> None:
    """
    Print the application header.
    
    Clears the screen and displays a formatted header for the application.
    """
    clear_screen()
    print("=" * 60)
    print("           S E C U R E   P A S S W O R D   M A N A G E R           ")
    print("=" * 60)
    print()


def print_menu() -> None:
    """
    Print the main menu options.
    
    Displays all available options for the user to choose from.
    """
    print("\nMAIN MENU:")
    print("1. View all services")
    print("2. Add new password")
    print("3. Retrieve password")
    print("4. Generate secure password")
    print("5. Check password breach")
    print("6. Delete password")
    print("7. Save and exit")
    print()


def generate_password(length: int = 16, include_special: bool = True) -> str:
    """
    Generate a secure random password.
    
    Creates a random password with specified length and character types.
    Ensures the password includes at least one lowercase letter, one
    uppercase letter, one digit, and one special character (if included).
    
    Args:
        length: The length of the password (default: 16)
        include_special: Whether to include special characters (default: True)
        
    Returns:
        A randomly generated password meeting the specified criteria
    """
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation if include_special else ""

    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits)
    ]

    if include_special:
        password.append(random.choice(special))

    # Fill remaining length with random characters from all sets
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(length - len(password)))

    # Shuffle the password characters
    random.shuffle(password)

    return ''.join(password)


def analyse_password_strength(password: str) -> Dict[str, Union[int, str, bool, List[str]]]:
    """
    Analyse the strength of a password.
    
    Evaluates password strength based on:
    - Length
    - Character variety (lowercase, uppercase, digits, special)
    - Common patterns
    - Repeating characters
    
    Args:
        password: The password to analyse
        
    Returns:
        A dictionary containing strength metrics including:
        - score: Numerical score (-3 to 5)
        - strength: Categorical rating (Weak, Medium, Strong)
        - feedback: List of specific feedback points
        - has_lowercase: Boolean indicating if password has lowercase letters
        - has_uppercase: Boolean indicating if password has uppercase letters
        - has_digit: Boolean indicating if password has digits
        - has_special: Boolean indicating if password has special characters
    """
    # Initialize metrics
    score = 0
    feedback = []

    # Check length
    if len(password) < 8:
        score -= 2
        feedback.append("Password is too short (< 8 characters)")
    elif len(password) >= 12:
        score += 2
        feedback.append("Good length")
    else:
        score += 1

    # Check character types
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^A-Za-z0-9]', password))

    char_types = sum([has_lowercase, has_uppercase, has_digit, has_special])

    if char_types == 4:
        score += 3
        feedback.append("Excellent character variety")
    elif char_types == 3:
        score += 2
        feedback.append("Good character variety")
    elif char_types == 2:
        score += 1
        feedback.append("Limited character variety")
    else:
        score -= 1
        feedback.append("Poor character variety")

    # Check for common patterns
    if re.search(r'12345|qwerty|password|admin', password.lower()):
        score -= 3
        feedback.append("Contains common patterns")

    # Check for repeating characters
    if re.search(r'(.)\1\1', password):
        score -= 1
        feedback.append("Contains repeating characters")

    # Determine strength level
    if score >= 4:
        strength = "Strong"
    elif score >= 2:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        'score': score,
        'strength': strength,
        'feedback': feedback,
        'has_lowercase': has_lowercase,
        'has_uppercase': has_uppercase,
        'has_digit': has_digit,
        'has_special': has_special
    }


def check_password_breach(password: str) -> Tuple[bool, Optional[int]]:
    """
    Check if a password has been compromised using the HaveIBeenPwned API.
    
    Uses the k-anonymity model to securely check if a password has appeared
    in known data breaches without sending the full password over the network.
    
    Args:
        password: The password to check
        
    Returns:
        A tuple containing (is_breached, occurrences) where:
            is_breached: True if the password appears in a breach
            occurrences: The number of times the password appears in breaches
                         (None if not breached or if an error occurred)
    """
    # Hash the password with SHA-1
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    hash_prefix = sha1_hash[:5]
    hash_suffix = sha1_hash[5:]

    try:
        # Query the API with the hash prefix
        response = requests.get(f"https://api.pwnedpasswords.com/range/{hash_prefix}", timeout=10)

        if response.status_code == 200:
            # Check if the hash suffix is in the response
            for line in response.text.splitlines():
                if line.split(':')[0] == hash_suffix:
                    occurrences = int(line.split(':')[1])
                    return True, occurrences

            # Password not found in breaches
            return False, None
        else:
            print(f"Error checking password breach: {response.status_code}")
            return False, None

    except Exception as e:
        print(f"Error checking password breach: {str(e)}")
        return False, None
    