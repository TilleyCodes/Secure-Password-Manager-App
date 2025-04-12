# pylint: disable=line-too-long

"""This module is the main file to run the Secure Password Manager Application."""

# Importing getpass for secure password input
# Source: Python standard library
# Purpose: To hide password input from the screen while typing
import getpass
# Importing sys for handling program exit
# Source: Python standard library
# Purpose: To exit the program gracefully on keyboard interrupt
import sys
# Importing PasswordManager class
# Source: local module - classes/password_manager.py
# Purpose: To provide core password management functionality including encryption and storage
from classes.password_manager import PasswordManager
# Importing password manager functions
# Source: local module - functions/password_functions.py
# Purpose: To provide utility functions for password generation, analysis, breach checking, and UI
from functions.password_functions import (print_header, print_menu, generate_password, analyse_password_strength, check_password_breach)


def main() -> None:
    """
    Main function to run the password manager application.
    
    Handles the login process, displays the main menu, and processes user input.
    All core functionality is accessed through this function.
    
    Returns:
        None
    """
    print_header()
    print("Welcome to the Secure Password Manager!")
    print("\nPlease enter your master password to continue.")

    # Get master password securely (input not visible on screen)
    master_password = getpass.getpass("Master Password: ")

    # Initialise password manager with the master password
    pm = PasswordManager(master_password)

    while True:
        print_header()
        print_menu()

        user_selection = input("Please enter your selection (1-7): ")

        if user_selection == '1':
            # View all services
            print("\n===== ALL STORED SERVICES =====")

            # Direct access to check if passwords dictionary exists and has content
            if not hasattr(pm, 'passwords') or not pm.passwords:
                print("No passwords stored yet.")
            else:
                # Direct iteration through the passwords dictionary
                count = 1
                for service in pm.passwords:
                    usernames = list(pm.passwords[service].keys())
                    user_count = len(usernames)
                    print(f"{count}. {service} ({user_count} username{'s' if user_count != 1 else ''})")
                    for username in usernames:
                        print(f"   - {username}")
                    count += 1

            print("==============================\n")
            input("Press Enter to continue...")

        elif user_selection == '2':
            # Add new password
            service = input("\nEnter service name: ")
            username = input("Enter username: ")

            password_choice = input("Do you want to (1) Enter a password or (2) Generate a password? ")

            if password_choice == '2':
                try:
                    length = int(input("Enter password length (default 16): ") or "16")
                    include_special = input("Include special characters? (y/n, default y): ").lower() != 'n'
                    password = generate_password(length, include_special)
                    print(f"\nGenerated password: {password}")
                except ValueError:
                    print("Invalid input. Using default values.")
                    password = generate_password()
                    print(f"\nGenerated password: {password}")
            else:
                password = getpass.getpass("Enter password: ")

            # Analyse password strength
            strength_info = analyse_password_strength(password)
            print(f"\nPassword strength: {strength_info['strength']}")
            for feedback in strength_info['feedback']:
                print(f"- {feedback}")

            # Check for breaches
            print("\nChecking if password has been compromised...")
            is_breached, occurrences = check_password_breach(password)

            if is_breached:
                print(f"WARNING: This password appears in {occurrences} data breaches!")
                confirm = input("Do you still want to save this password? (y/n): ").lower()
                if confirm != 'y':
                    print("Password not saved.")
                    input("Press Enter to continue...")
                    continue
            else:
                print("Good news! This password hasn't been found in any known data breaches.")

            pm.add_password(service, username, password)
            pm.save_passwords()

            input("Press Enter to continue...")

        elif user_selection == '3':
            # Retrieve password
            service = input("\nEnter service name: ")
            username = input("Enter username: ")

            password = pm.get_password(service, username)

            if password:
                print(f"\nPassword for {service} ({username}): {password}")
            else:
                print(f"\nNo password found for {service} ({username}).")

            input("Press Enter to continue...")

        elif user_selection == '4':
            # Generate secure password
            try:
                length = int(input("\nEnter password length (default 16): ") or "16")
                include_special = input("Include special characters? (y/n, default y): ").lower() != 'n'

                password = generate_password(length, include_special)
                print(f"\nGenerated password: {password}")

                # Analyse password strength
                strength_info = analyse_password_strength(password)
                print(f"Password strength: {strength_info['strength']}")
                for feedback in strength_info['feedback']:
                    print(f"- {feedback}")

                # Check for breaches
                print("\nChecking if password has been compromised...")
                is_breached, occurrences = check_password_breach(password)

                if is_breached:
                    print(f"WARNING: This password appears in {occurrences} data breaches!")
                else:
                    print("Good news! This password hasn't been found in any known data breaches.")

                save_choice = input("\nDo you want to save this password? (y/n): ").lower()

                if save_choice == 'y':
                    service = input("Enter service name: ")
                    username = input("Enter username: ")
                    pm.add_password(service, username, password)
                    pm.save_passwords()
                    print(f"Password saved for {service} ({username}).")

            except ValueError:
                print("Invalid input. Please enter a valid number for password length.")

            input("Press Enter to continue...")

        elif user_selection == '5':
            # Check password breach
            password = getpass.getpass("\nEnter password to check: ")

            print("Checking if password has been compromised...")
            is_breached, occurrences = check_password_breach(password)

            if is_breached:
                print(f"WARNING: This password appears in {occurrences} data breaches!")
                print("It is highly recommended to change this password immediately.")
            else:
                print("Good news! This password hasn't been found in any known data breaches.")

            input("Press Enter to continue...")

        elif user_selection == '6':
            # Delete password
            service = input("\nEnter service name: ")
            username = input("Enter username: ")

            if pm.delete_password(service, username):
                pm.save_passwords()

            input("Press Enter to continue...")

        elif user_selection == '7':
            # Save and exit
            pm.save_passwords()
            print("\nThank you for using the Secure Password Manager. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 7.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
        sys.exit(0)
        