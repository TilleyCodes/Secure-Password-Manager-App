import os
import random
import string
import re
from typing import Dict, List, Union


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header() -> None:
    clear_screen()
    print("=" * 60)
    print("           S E C U R E   P A S S W O R D   M A N A G E R           ")
    print("=" * 60)
    print()

def print_menu() -> None:
    print("\nMAIN MENU: \n")
    print("1. View all services")
    print("2. Add new password")
    print("3. Retrieve password")
    print("4. Generate secure password")
    print("5. Check password breach")
    print("6. Delete password")
    print("7. Save and exit")
    print()
    
def generate_password(length: int = 16, include_special: bool = True) -> str:
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
    # Initialise metrics
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