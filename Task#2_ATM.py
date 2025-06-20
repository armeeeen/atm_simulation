import os    # To check file Existence
import uuid  #for unique user identity
import sys

USERS_FILE = "users.txt"

class User:
    def __init__(self, user_id, name, pin, balance=0.0):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.balance = float(balance)

def save_user_to_file(user: User):
    with open(USERS_FILE, "a") as f:
        f.write(f"{user.user_id}::{user.name}::{user.pin}::{user.balance}\n")

def load_user_by_id(user_id):
    if not os.path.exists(USERS_FILE):
        return None

    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("::")
            if parts[0] == user_id:
                return User(user_id=parts[0], name=parts[1], pin=parts[2], balance=float(parts[3]))
    return None

def update_user_pin(user_id, new_pin):
    if not os.path.exists(USERS_FILE):
        return

    lines = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("::")
            if parts[0] == user_id:
                parts[2] = new_pin
            lines.append("::".join(parts) + "\n")

    with open(USERS_FILE, "w") as f:
        f.writelines(lines)

def update_user_balance(user_id, new_balance):
    if not os.path.exists(USERS_FILE):
        return

    lines = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("::")
            if parts[0] == user_id:
                parts[3] = str(new_balance)
            lines.append("::".join(parts) + "\n")

    with open(USERS_FILE, "w") as f:
        f.writelines(lines)

# ATM class
class ATM:
    def __init__(self, user: User):
        self.user = user
        self.__transactions = []
        self.transaction_file = "transactions.txt"

    def authentication(self):
        attempts = 0
        while attempts < 3:
            entered_pin = input("Enter your PIN: ")
            if entered_pin == self.user.pin:
                print(f"\nWelcome, {self.user.name}!")
                return True
            else:
                attempts += 1
                rem_attempts = 3 - attempts
                print(f"Incorrect PIN. Attempts left: {rem_attempts}")
        print("Limit Reached! Exiting.")
        return False

    def mainMenu(self):
        while True:
            print("\n------- Main Menu --------")
            print("1. Check Balance")
            print("2. Deposit Funds")
            print("3. Withdraw Funds")
            print("4. Change PIN")
            print("5. View Transactions")
            print("6. Exit")

            try:
                opt = int(input("Select (1-6): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if opt == 1:
                self.checkBalance()
            elif opt == 2:
                self.deposit()
            elif opt == 3:
                self.withdraw()
            elif opt == 4:
                self.changePin()
            elif opt == 5:
                self.viewTransactions()
            elif opt == 6:
                print("Thank you for using our ATM!")
                break
            else:
                print("Invalid option. Please try again.")

    def checkBalance(self):
        print(f"Your current balance is: ${self.user.balance:.2f}")

    def deposit(self):
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Deposit amount must be positive.")
            else:
                self.user.balance += amount
                update_user_balance(self.user.user_id, self.user.balance)
                record = f"Deposited ${amount:.2f}"
                self.__log_transaction(record)
                print(record)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("Withdrawal amount must be positive.")
            elif amount > self.user.balance:
                print("Insufficient balance.")
            else:
                self.user.balance -= amount
                update_user_balance(self.user.user_id, self.user.balance)
                record = f"Withdrew ${amount:.2f}"
                self.__log_transaction(record)
                print(record)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def changePin(self):
        currentPin = input("Enter your current PIN: ")
        if currentPin == self.user.pin:
            newPin = input("Enter new PIN: ")
            confirmPin = input("Confirm new PIN: ")
            if newPin == confirmPin:
                self.user.pin = newPin
                update_user_pin(self.user.user_id, newPin)
                print("PIN changed successfully.")
            else:
                print("PIN confirmation does not match.")
        else:
            print("Incorrect current PIN entered.")

    def viewTransactions(self):
        print("\n------ Transaction History ------")
        found = False
        if os.path.exists(self.transaction_file):
            with open(self.transaction_file, "r") as f:
                for line in f:
                    if line.startswith(self.user.user_id):
                        print(line.strip().split("::")[1])
                        found = True
        if not found:
            print("Transaction File is Empty")

    def __log_transaction(self, message):
        entry = f"{self.user.user_id}::{message}"
        self.__transactions.append(message)
        with open(self.transaction_file, "a") as file:
            file.write(entry + "\n")

# Main
if __name__ == "__main__":
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

        user_id = str(uuid.uuid4())[:8]
        user = User(user_id, name, pin, 0.0)
        save_user_to_file(user)
        print(f"Account created successfully! Your User ID is: {user.user_id}")

        atm = ATM(user)
        if atm.authentication():
            atm.mainMenu()

    elif choice == 2:
        user_id = input("Enter your User ID: ")
        user = load_user_by_id(user_id)

        if user is None:
            print("User not found.")
            sys.exit()

        atm = ATM(user)
        if atm.authentication():
            atm.mainMenu()
    else:
        print("Invalid selection. Please choose 1 or 2.")
