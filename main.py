import getpass
import sys
from classes.password_manager import PasswordManager
from functions.password_functions import (print_header, print_menu, generate_password)

def main() -> None:
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
            services = pm.list_services()
            if not services:
                print("\nNo passwords stored yet.")
            else:
                print("\nStored services:")
                for idx, service in enumerate(services, 1):
                    usernames = pm.list_usernames(service)
                    user_count = len(usernames)
                    print(f"{idx}. {service} ({user_count} username{'s' if user_count != 1 else ''})")

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
        