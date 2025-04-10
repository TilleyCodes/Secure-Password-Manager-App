import os
import random
import string

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