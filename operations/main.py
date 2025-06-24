import os
import sys



if not os.path.exists("../data"):
    os.makedirs("../data")

from user_operations import User, load_user_by_id
from operations.atm_machine import ATM


def main():
    print("------ Welcome to ATM ------")
    try:
        choice = int(input("Press 1 to create account, press 2 to log in for transactions: "))
    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        sys.exit()

    if choice == 1:
        name = input("Enter your name: ")
        pin = input("Set your 4-digit PIN: ")
        if not (pin.isdigit() and len(pin) == 4):
            print("PIN must be exactly 4 digits.")
            sys.exit()
        user = User.create_user(name, pin)
        atm = ATM(user)
        if atm.authentication():
            atm.mainMenu()

    elif choice == 2:
        user_id = input("Enter your User ID: ")
        user = load_user_by_id(user_id)
        if user is None:
            print("User not found or inactive.")
            sys.exit()
        atm = ATM(user)
        if atm.authentication():
            atm.mainMenu()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
