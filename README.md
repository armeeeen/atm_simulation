# ATM Simulation in Python

This is a console-based ATM simulation system implemented in Python. It allows users to interact with a virtual bank account and perform operations like balance inquiry, deposit, withdrawal, PIN change, and view transaction history.

## 📁 Project Structure

- `operations/user_operations.py` – User model, user creation, file I/O (users.csv)
- `operations/atm_machine.py` – ATM class with all functionalities
- `operations/admin.py` – Admin-related utilities (optional)
- `operations/main.py` – Main entry point to start the ATM system
- `data/users.csv` – Stores user data
- `data/transactions.csv` – Stores transaction history

## 🛠️ Features

- User authentication (with PIN and UUID)
- Create account (assigns unique user ID)
- Deposit & Withdraw with validation
- Check balance
- Change PIN (with validation)
- View transaction history (from CSV)
- Data persistence using CSV files

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/atm-simulation-updated.git
   cd atm-simulation-updated/operations

2. Run the Program:

python main.py
