import os
import csv
from user_operations import update_user_balance, update_user_pin, User, hash_pin

class ATM:
    def __init__(self, user: User):
        self.__user = user
        self.__transactions = []
        self.__transaction_file = "../data/transactions.csv"

    def authentication(self):
        attempts = 0
        while attempts < 3:
            entered_pin = input("Enter your PIN: ")
            if hash_pin(entered_pin) == self.__user.pin:
                print(f"\nWelcome, {self.__user.name}!")
                return True
            else:
                attempts += 1
                print(f"Incorrect PIN. Attempts left: {3 - attempts}")
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
                self.__check_balance()
            elif opt == 2:
                self.__deposit()
            elif opt == 3:
                self.__withdraw()
            elif opt == 4:
                self.__change_pin()
            elif opt == 5:
                self.__view_transactions()
            elif opt == 6:
                print("Thank you for using our ATM!")
                break
            else:
                print("Invalid option. Please try again.")

    def __check_balance(self):
        print(f"Your current balance is: ${self.__user.balance:.2f}")

    def __deposit(self):
        try:
            amount = float(input("Enter amount to deposit: $"))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                self.__user.balance += amount
                update_user_balance(self.__user.user_id, self.__user.balance)
                self.__log_transaction(f"Deposited ${amount:.2f}")
                print("Deposit successful.")
        except ValueError:
            print("Invalid input.")

    def __withdraw(self):
        try:
            amount = float(input("Enter amount to withdraw: $"))
            if amount <= 0:
                print("Amount must be positive.")
            elif amount > self.__user.balance:
                print("Insufficient balance.")
            else:
                self.__user.balance -= amount
                update_user_balance(self.__user.user_id, self.__user.balance)
                self.__log_transaction(f"Withdrew ${amount:.2f}")
                print("Withdrawal successful.")
        except ValueError:
            print("Invalid input.")

    def __change_pin(self):
        current_pin = input("Enter current PIN: ")
        if hash_pin(current_pin) == self.__user.pin:
            new_pin = input("Enter new PIN: ")
            confirm = input("Confirm new PIN: ")
            if new_pin == confirm:
                self.__user._User__pin = hash_pin(new_pin)
                update_user_pin(self.__user.user_id, new_pin)
                print("PIN changed.")
            else:
                print("PIN confirmation failed.")
        else:
            print("Incorrect current PIN.")

    def __view_transactions(self):
        print("\n------ Transaction History ------")
        found = False
        if os.path.exists(self.__transaction_file):
            with open(self.__transaction_file, newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == self.__user.user_id:
                        print(row[1])
                        found = True
        if not found:
            print("No transactions found.")

    def __log_transaction(self, message):
        self.__transactions.append(message)
        with open(self.__transaction_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.__user.user_id, message])
