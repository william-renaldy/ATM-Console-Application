
import pandas as pd
from datetime import datetime
import os

class ATM:
    def __init__(self, atm_name: str, atm_number: int) -> None:
        self.atm_name = atm_name
        self.atm_number = atm_number
        self.balance_amount = 0.0

    def bank_deposit(self, bank: 'Bank', amount: float) -> bool:
        if amount > 0:
            self.balance_amount += amount
            return bank.deposit(self.atm_number, amount)
        else:
            return False
        
    def user_deposit(self, user: 'User', amount: float) -> bool:
        if amount > 0:
            self.balance_amount += amount
            return user.deposit(amount)
        else:
            return False

    def withdraw(self, user: 'User', amount: float) -> bool:
        if self.balance_amount >= amount > 0:
            self.balance_amount -= amount
            return user.withdraw(amount)
        else:
            return False

    def download_all_bank_transactions(self) -> pd.DataFrame:
        return pd.read_csv('bank_transactions.csv')

    def download_all_user_transactions(self, user: 'User') -> pd.DataFrame:
        return pd.read_csv(f'user_{user.acc_number}_transactions.csv')


class Bank:
    def __init__(self, bank_name: str, bank_number: int) -> None:
        self.bank_name = bank_name
        self.bank_number = bank_number

    def deposit(self, atm_number: int, amount: float) -> bool:

        transaction_data = pd.DataFrame({
            'Date': [datetime.now()],
            'ATM Number': [atm_number],
            'Transaction Type': ['Deposit'],
            'Amount': [amount]
        })
        transaction_data.to_csv('bank_transactions.csv', mode='a', index=False, header=False)
        return True

    def download_user_transactions(self, atm: ATM, start_time: datetime, end_time: datetime) -> pd.DataFrame:

        return pd.read_csv('bank_transactions.csv')

    def download_bank_details(self) -> pd.DataFrame:

        return pd.DataFrame({
            'Bank Name': [self.bank_name],
            'Bank Number': [self.bank_number],
            'Timestamp': [datetime.now()]
        })

class User:
    def __init__(self, acc_number: int, user_name: str, initial_balance: float, pin_number: int) -> None:
        self.acc_number = acc_number
        self.user_name = user_name
        self.pin_number = pin_number
        self.transactions_csv = f'user_{self.acc_number}_transactions.csv'
        
        if not os.path.exists(self.transactions_csv):

            with open(self.transactions_csv, 'w'):
                pass

            initial_transaction = pd.DataFrame({
                'Date': [datetime.now()],
                'Transaction Type': ['Initial Balance'],
                'Amount': [initial_balance]
            })
            initial_transaction.to_csv(self.transactions_csv, mode='a', index=False)

    def set_pin(self, pin_number: int) -> None:
        self.pin_number = pin_number

    def change_pin(self, old_pin: int, new_pin: int) -> bool:
        if self.pin_number == old_pin:
            self.pin_number = new_pin
            return True
        else:
            return False

    def login(self, acc_number: int, pin_number: int) -> bool:

        return self.acc_number == acc_number and self.pin_number == pin_number
    
    def deposit(self, amount: float) -> bool:
        if amount > 0:

            transaction_data = pd.DataFrame({
                'Date': [datetime.now()],
                'Transaction Type': ['Deposit'],
                'Amount': [amount]
            })
            transaction_data.to_csv(self.transactions_csv, mode='a', index=False, header=False)
            return True
        else:
            return False

    def withdraw(self, amount: float) -> bool:
        if self.get_balance() >= amount > 0:

            transaction_data = pd.DataFrame({
                'Date': [datetime.now()],
                'Transaction Type': ['Withdrawal'],
                'Amount': [-amount]  
            })
            transaction_data.to_csv(self.transactions_csv, mode='a', index=False, header=False)
            return True
        else:
            return False

    def download_statement(self, start_time: datetime, end_time: datetime) -> pd.DataFrame:
        return pd.read_csv(self.transactions_csv)

    def get_balance(self) -> float:

        transactions = pd.read_csv(self.transactions_csv)
        return transactions['Amount'].sum()

    def transfer_amount(self, to_user: 'User', amount: float) -> bool:
        if self.get_balance() >= amount > 0:

            self_transaction_data = pd.DataFrame({
                'Date': [datetime.now()],
                'Transaction Type': ['Transfer'],
                'Amount': [-amount] 
            })
            to_user_transaction_data = pd.DataFrame({
                'Date': [datetime.now()],
                'Transaction Type': ['Transfer'],
                'Amount': [amount]  
            })
            self_transaction_data.to_csv(self.transactions_csv, mode='a', index=False, header=False)
            to_user_transaction_data.to_csv(to_user.transactions_csv, mode='a', index=False, header=False)
            return True
        else:
            return False
        

def main():
    print("Welcome to the ATM system")
    users = {}

    while True:
        role = input("Are you an ATM, Bank, or User? (Type 'exit' to quit): ").lower()

        if role == 'atm':
            atm_name = input("Enter ATM name: ")
            atm_number = int(input("Enter ATM number: "))
            atm = ATM(atm_name, atm_number)
            while True:
                print("\nSelect an option:")
                print("1. Bank Deposit")
                print("2. User Deposit")
                print("3. Withdraw from User")
                print("4. Download Bank Transactions")
                print("5. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    amount = float(input("Enter the amount to deposit into the bank: "))
                    if atm.bank_deposit(bank, amount):
                        print("Deposit successful.")
                    else:
                        print("Invalid amount.")

                elif choice == "2":
                    acc_number = int(input("Enter user's account number: "))
                    amount = float(input("Enter the amount to deposit: "))
                    if atm.user_deposit(users[acc_number], amount):
                        print("Deposit successful.")
                    else:
                        print("Invalid amount or user not found.")

                elif choice == "3":
                    acc_number = int(input("Enter user's account number: "))
                    amount = float(input("Enter the amount to withdraw: "))
                    if atm.withdraw(users[acc_number], amount):
                        print("Withdrawal successful.")
                    else:
                        print("Invalid amount or insufficient funds.")

                elif choice == "4":
                    print("Downloading bank transactions...")
                    print(bank.download_all_bank_transactions())

                elif choice == "5":
                    print("Exiting...")
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif role == 'bank':
            bank_name = input("Enter bank name: ")
            bank_number = int(input("Enter bank number: "))
            bank = Bank(bank_name, bank_number)
            while True:
                print("\nSelect an option:")
                print("1. Deposit from ATM")
                print("2. Download User Transactions")
                print("3. Download Bank Details")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    atm_number = int(input("Enter ATM number: "))
                    amount = float(input("Enter the amount to deposit: "))
                    if bank.deposit(atm_number, amount):
                        print("Deposit successful.")
                    else:
                        print("Invalid amount or ATM not found.")

                elif choice == "2":
                    atm_number = int(input("Enter ATM number: "))
                    start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
                    end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
                    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                    print("Downloading user transactions...")
                    print(bank.download_user_transactions(atm_number, start_time, end_time))

                elif choice == "3":
                    print("Downloading bank details...")
                    print(bank.download_bank_details())

                elif choice == "4":
                    print("Exiting...")
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif role == 'user':
            acc_number = int(input("Enter your account number: "))
            if acc_number in users:
                user = users[acc_number]
                pin = int(input("Enter your PIN: "))
                if user.login(acc_number, pin):
                    print(f"Login successful. Welcome, {user.user_name}!")
                    while True:
                        print("\nSelect an option:")
                        print("1. Check Balance")
                        print("2. Deposit")
                        print("3. Withdraw")
                        print("4. Transfer")
                        print("5. Download Statement")
                        print("6. Exit")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            print(f"Your current balance is: {user.get_balance()}")

                        elif choice == "2":
                            amount = float(input("Enter the amount to deposit: "))
                            if user.deposit(amount):
                                print("Deposit successful.")

                        elif choice == "3":
                            amount = float(input("Enter the amount to withdraw: "))
                            if user.withdraw(amount):
                                print("Withdrawal successful.")
                            else:
                                print("Insufficient funds.")

                        elif choice == "4":
                            recipient_acc_number = int(input("Enter recipient's account number: "))
                            amount = float(input("Enter the amount to transfer: "))
                            if recipient_acc_number in users:
                                recipient = users[recipient_acc_number]
                                if user.transfer_amount(recipient, amount):
                                    print("Transfer successful.")
                                else:
                                    print("Transfer failed. Insufficient funds.")
                            else:
                                print("Recipient account not found.")

                        elif choice == "5":
                            start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
                            end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
                            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                            print("Downloading statement...")
                            print(user.download_statement(start_time, end_time))

                        elif choice == "6":
                            print("Exiting...")
                            break

                        else:
                            print("Invalid choice. Please try again.")

                else:
                    print("Invalid account number or PIN. Would you like to create a new account?")
                    create_new = input("Enter 'yes' to create a new account, or any other key to continue: ").lower()
                    if create_new == 'yes':
                        user_name = input("Enter your name: ")
                        initial_balance = float(input("Enter initial balance: "))
                        pin = int(input("Set your PIN: "))
                        user = User(acc_number, user_name, initial_balance, pin)
                        users[acc_number] = user
                        print("Account created successfully.")
                    else:
                        continue
            else:
                print("User not found. Would you like to create a new account?")
                create_new = input("Enter 'yes' to create a new account, or any other key to continue: ").lower()
                if create_new == 'yes':
                    user_name = input("Enter your name: ")
                    initial_balance = float(input("Enter initial balance: "))
                    pin = int(input("Set your PIN: "))
                    user = User(acc_number, user_name, initial_balance, pin)
                    users[acc_number] = user
                    print("Account created successfully.")
                else:
                    continue

        elif role == 'exit':
            print("Exiting...")
            break

        else:
            print("Invalid role. Please try again.")


if __name__ == "__main__":
    main()
