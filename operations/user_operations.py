import os
import uuid
import csv
import hashlib

__USERS_FILE = "../data/users.csv"

class User:
    def __init__(self, user_id, name, pin, balance=0.0):
        self.user_id = user_id
        self.name = name
        self.__pin = pin  # already hashed
        self.balance = float(balance)

    @property
    def pin(self):
        return self.__pin

    @classmethod
    def create_user(cls, name, pin):
        user_id = str(uuid.uuid4())[:8]
        hashed_pin = hash_pin(pin)
        user = cls(user_id, name, hashed_pin, 0.0)
        _save_user_to_file(user)
        print(f"Account created successfully! Your User ID is: {user.user_id}")
        return user

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def _save_user_to_file(user: User):
    write_header = not os.path.exists(__USERS_FILE) or os.path.getsize(__USERS_FILE) == 0
    with open(__USERS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["user_id", "name", "pin", "balance", "status"])
        writer.writerow([user.user_id, user.name, user.pin, user.balance, "active"])

def load_user_by_id(user_id):
    if not os.path.exists(__USERS_FILE):
        return None
    with open(__USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id and row["status"] == "active":
                return User(
                    user_id=row["user_id"],
                    name=row["name"],
                    pin=row["pin"],
                    balance=float(row["balance"])
                )
    return None

def update_user_pin(user_id, new_pin):
    new_hashed_pin = hash_pin(new_pin)
    if not os.path.exists(__USERS_FILE):
        return
    updated_rows = []
    with open(__USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id:
                row["pin"] = new_hashed_pin
            updated_rows.append(row)
    with open(__USERS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "pin", "balance", "status"])
        writer.writeheader()
        writer.writerows(updated_rows)

def update_user_balance(user_id, new_balance):
    if not os.path.exists(__USERS_FILE):
        return
    updated_rows = []
    with open(__USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id:
                row["balance"] = str(new_balance)
            updated_rows.append(row)
    with open(__USERS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "pin", "balance", "status"])
        writer.writeheader()
        writer.writerows(updated_rows)

def soft_delete_user(user_id):
    if not os.path.exists(__USERS_FILE):
        return False
    updated_rows = []
    deleted = False
    with open(__USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id and row["status"] == "active":
                row["status"] = "deleted"
                deleted = True
            updated_rows.append(row)
    if deleted:
        with open(__USERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "name", "pin", "balance", "status"])
            writer.writeheader()
            writer.writerows(updated_rows)
    return deleted

def restore_user(user_id):
    if not os.path.exists(__USERS_FILE):
        return False
    updated_rows = []
    restored = False
    with open(__USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id and row["status"] == "deleted":
                row["status"] = "active"
                restored = True
            updated_rows.append(row)
    if restored:
        with open(__USERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "name", "pin", "balance", "status"])
            writer.writeheader()
            writer.writerows(updated_rows)
    return restored
