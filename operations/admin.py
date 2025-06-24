import csv
import os
from user_operations import soft_delete_user, restore_user

USERS_FILE = "../data/users.csv"

def view_all_users():
    if not os.path.exists(USERS_FILE):
        print("No user data found.")
        return

    with open(USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        print("\n--- All Users ---")
        for row in reader:
            print(f"ID: {row['user_id']}, Name: {row['name']}, Status: {row['status']}, Balance: ${row['balance']}")
    print("------------------")

def admin_menu():
    while True:
        print("\n====== Admin Panel ======")
        print("1. Soft delete a user")
        print("2. Restore a user")
        print("3. View all users")
        print("4. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            uid = input("Enter User ID to soft delete: ").strip()
            if soft_delete_user(uid):
                print("User soft-deleted successfully.")
            else:
                print("User not found or already deleted.")
        elif choice == "2":
            uid = input("Enter User ID to restore: ").strip()
            if restore_user(uid):
                print("User restored successfully.")
            else:
                print("User not found or already active.")
        elif choice == "3":
            view_all_users()
        elif choice == "4":
            print("Exiting admin panel.")
            break
        else:
            print("Invalid option. Please choose from 1–4.")

if __name__ == "__main__":
    admin_menu()
