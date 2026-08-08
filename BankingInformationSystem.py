"""
Banking Information System
Python Internship Project - UpskillCampus
Student: Marripelly Vikas

A console-based banking application demonstrating:
- Account creation
- Secure PIN-based login
- Deposit
- Withdrawal
- Fund transfer
- Balance inquiry
- Account details
- Transaction history
- Account listing
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
import random


@dataclass
class Transaction:
    transaction_type: str
    amount: float
    description: str
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )


@dataclass
class Account:
    account_number: int
    name: str
    phone: str
    pin: str
    balance: float = 0.0
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction_type: str, amount: float, description: str):
        self.transactions.append(
            Transaction(transaction_type, amount, description)
        )


class BankingInformationSystem:
    def __init__(self):
        self.accounts: Dict[int, Account] = {}
        self.next_account_number = 100001

    def generate_account_number(self) -> int:
        account_number = self.next_account_number
        self.next_account_number += 1
        return account_number

    @staticmethod
    def read_positive_amount(prompt: str) -> float:
        while True:
            try:
                amount = float(input(prompt))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                return amount
            except ValueError:
                print("Please enter a valid numeric amount.")

    def create_account(self):
        print("\n========== CREATE ACCOUNT ==========")
        name = input("Enter full name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        phone = input("Enter phone number: ").strip()
        if not phone.isdigit() or len(phone) < 10:
            print("Please enter a valid phone number.")
            return

        while True:
            pin = input("Create a 4-digit PIN: ").strip()
            if pin.isdigit() and len(pin) == 4:
                break
            print("PIN must contain exactly 4 digits.")

        initial_deposit = self.read_positive_amount(
            "Enter initial deposit (minimum Rs. 500): Rs. "
        )
        if initial_deposit < 500:
            print("Initial deposit must be at least Rs. 500.")
            return

        account_number = self.generate_account_number()
        account = Account(
            account_number=account_number,
            name=name,
            phone=phone,
            pin=pin,
            balance=initial_deposit,
        )
        account.add_transaction(
            "DEPOSIT", initial_deposit, "Initial account deposit"
        )
        self.accounts[account_number] = account

        print("\nAccount created successfully!")
        print(f"Account Number : {account_number}")
        print(f"Account Holder : {name}")
        print(f"Opening Balance: Rs. {initial_deposit:.2f}")

    def authenticate(self):
        try:
            account_number = int(input("Enter account number: "))
        except ValueError:
            print("Invalid account number.")
            return None

        account = self.accounts.get(account_number)
        if account is None:
            print("Account not found.")
            return None

        pin = input("Enter 4-digit PIN: ").strip()
        if pin != account.pin:
            print("Incorrect PIN.")
            return None

        return account

    def deposit(self):
        print("\n========== DEPOSIT ==========")
        account = self.authenticate()
        if account is None:
            return

        amount = self.read_positive_amount("Enter deposit amount: Rs. ")
        account.balance += amount
        account.add_transaction("DEPOSIT", amount, "Cash deposit")
        print(f"Deposit successful. New balance: Rs. {account.balance:.2f}")

    def withdraw(self):
        print("\n========== WITHDRAW ==========")
        account = self.authenticate()
        if account is None:
            return

        amount = self.read_positive_amount("Enter withdrawal amount: Rs. ")
        if amount > account.balance:
            print("Insufficient balance.")
            return

        account.balance -= amount
        account.add_transaction("WITHDRAW", amount, "Cash withdrawal")
        print(f"Withdrawal successful. New balance: Rs. {account.balance:.2f}")

    def transfer(self):
        print("\n========== FUND TRANSFER ==========")
        print("Sender authentication")
        sender = self.authenticate()
        if sender is None:
            return

        try:
            receiver_number = int(input("Enter receiver account number: "))
        except ValueError:
            print("Invalid receiver account number.")
            return

        receiver = self.accounts.get(receiver_number)
        if receiver is None:
            print("Receiver account not found.")
            return

        if sender.account_number == receiver.account_number:
            print("Sender and receiver accounts must be different.")
            return

        amount = self.read_positive_amount("Enter transfer amount: Rs. ")
        if amount > sender.balance:
            print("Insufficient balance for transfer.")
            return

        sender.balance -= amount
        receiver.balance += amount

        sender.add_transaction(
            "TRANSFER",
            amount,
            f"Transfer to account {receiver.account_number}",
        )
        receiver.add_transaction(
            "TRANSFER",
            amount,
            f"Received from account {sender.account_number}",
        )

        print("Transfer completed successfully.")
        print(f"Sender balance  : Rs. {sender.balance:.2f}")
        print(f"Receiver balance: Rs. {receiver.balance:.2f}")

    def balance_inquiry(self):
        print("\n========== BALANCE INQUIRY ==========")
        account = self.authenticate()
        if account:
            print(f"Account Number: {account.account_number}")
            print(f"Available Balance: Rs. {account.balance:.2f}")

    def account_details(self):
        print("\n========== ACCOUNT DETAILS ==========")
        account = self.authenticate()
        if account:
            print(f"Account Number: {account.account_number}")
            print(f"Account Holder: {account.name}")
            print(f"Phone Number  : {account.phone}")
            print(f"Balance       : Rs. {account.balance:.2f}")

    def transaction_history(self):
        print("\n========== TRANSACTION HISTORY ==========")
        account = self.authenticate()
        if account is None:
            return

        if not account.transactions:
            print("No transactions available.")
            return

        print(f"\nTransactions for Account {account.account_number}")
        print("-" * 78)
        for index, transaction in enumerate(account.transactions, start=1):
            print(
                f"{index:>2}. {transaction.timestamp} | "
                f"{transaction.transaction_type:<8} | "
                f"Rs. {transaction.amount:>10.2f} | "
                f"{transaction.description}"
            )

    def list_accounts(self):
        print("\n========== ACCOUNT LIST ==========")
        if not self.accounts:
            print("No accounts have been created.")
            return

        print(f"{'Account No.':<15}{'Name':<25}{'Balance':>15}")
        print("-" * 55)
        for account in self.accounts.values():
            print(
                f"{account.account_number:<15}"
                f"{account.name[:24]:<25}"
                f"Rs. {account.balance:>10.2f}"
            )

    def run(self):
        while True:
            print("\n" + "=" * 60)
            print("          BANKING INFORMATION SYSTEM")
            print("=" * 60)
            print("1. Create New Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. Balance Inquiry")
            print("6. Account Details")
            print("7. Transaction History")
            print("8. List All Accounts")
            print("9. Exit")
            print("=" * 60)

            choice = input("Enter your choice (1-9): ").strip()

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.balance_inquiry()
            elif choice == "6":
                self.account_details()
            elif choice == "7":
                self.transaction_history()
            elif choice == "8":
                self.list_accounts()
            elif choice == "9":
                print("\nThank you for using the Banking Information System.")
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1 to 9.")


if __name__ == "__main__":
    system = BankingInformationSystem()
    system.run()
