import pickle
import os
import pathlib


''' this is the demo project in these project we are not added any UI part the output showing only command prompt
you want see the original project goto main.py this is original project'''

class BankAccount:
    def __init__(self, accNo=0, name='', deposit=0, type='', password=''):
        self.accNo = accNo
        self.name = name
        self.deposit = deposit
        self.type = type
        self.password = password

    def create_account(self):
        try:
            self.accNo = int(input("Enter the account no: "))
            self.name = input("Enter the account holder name: ")

            self.type = input("Enter the type of account [C/S]: ").upper()
            while self.type not in ('C', 'S'):
                print("Invalid account type. Please enter 'C' for Current or 'S' for Savings.")
                self.type = input("Enter the type of account [C/S]: ").upper()

            while True:
                self.deposit = int(input("Enter the Initial deposit (>=1000 for Savings, >=2000 for Current): "))
                if (self.type == 'S' and self.deposit >= 1000) or (self.type == 'C' and self.deposit >= 2000):
                    break
                print("Error: Minimum deposit for Savings is 1000 and for Current is 2000.")

            self.password = input("Set a password for the account: ")

            print("Account Created Successfully!")
        except ValueError:
            print("Invalid input. Please enter numeric values for account number and deposit.")

    def show_account(self):
        print(f"Account Number: {self.accNo}")
        print(f"Account Holder Name: {self.name}")
        print(f"Type of Account: {self.type}")
        print(f"Balance: {self.deposit}")

    def modify_account(self):
        self.name = input("Modify Account Holder Name: ")
        self.type = input("Modify type of Account [C/S]: ").upper()
        while self.type not in ('C', 'S'):
            print("Invalid account type. Please enter 'C' for Current or 'S' for Savings.")
            self.type = input("Modify type of Account [C/S]: ").upper()
        self.deposit = int(input("Modify Balance: "))

    def deposit_amount(self, amount):
        self.deposit += amount

    def withdraw_amount(self):
        while True:
            amount = int(input("Enter the amount to withdraw: "))
            if amount <= self.deposit:
                self.deposit -= amount
                print("Withdrawal successful. Your new balance is:", self.deposit)
                break
            else:
                print("Insufficient funds. Please enter a valid amount.")

    def check_password(self):
        entered_password = input("Enter your account password: ")
        return entered_password == self.password

    def report(self):
        print(self.accNo, self.name, self.type, self.deposit)

def intro():
    print("\t\t\t\t==========================")
    print("\t\t\t\tBANK MANAGEMENT SYSTEM")
    print("\t\t\t\t===========================")
    input("Press Enter To Continue: ")

def write_account():
    account = BankAccount()
    account.create_account()
    write_accounts_file(account)

def write_accounts_file(account):
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            oldlist = pickle.load(infile)
        oldlist.append(account)
    else:
        oldlist = [account]
    
    with open('accounts.data', 'wb') as outfile:
        pickle.dump(oldlist, outfile)

def display_all():
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as file1:
                mylist = pickle.load(file1)
            for item in mylist:
                item.show_account()
        except (FileNotFoundError, EOFError) as e:
            print("Error reading file:", e)
    else:
        print("No records available.")

def display_balance(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                mylist = pickle.load(infile)
            found = False
            for item in mylist:
                if item.accNo == num:
                    print("Your account balance is =", item.deposit)
                    found = True
                    break
            if not found:
                print("No existing record with this number.")
        except (FileNotFoundError, EOFError) as e:
            print("Error reading file:", e)
    else:
        print("No records to search.")

def deposit_and_withdraw(num1, action):
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                mylist = pickle.load(infile)

            account_found = False
            for item in mylist:
                if item.accNo == num1:
                    if item.check_password():
                        account_found = True
                        if action == 1:  # Deposit
                            while True:
                                amount = int(input("Enter the amount to deposit: "))
                                if (item.type == 'S' and amount >= 1000) or (item.type == 'C' and amount >= 2000):
                                    item.deposit_amount(amount)
                                    print("Deposit successful. Your new balance is:", item.deposit)
                                    break
                                else:
                                    print("Error: Minimum deposit for Savings is 1000 and for Current is 2000.")
                        elif action == 2:  # Withdraw
                            item.withdraw_amount()
                    else:
                        print("Invalid password. Access denied.")

            if not account_found:
                print("No existing record with this account number.")
        except (FileNotFoundError, EOFError) as e:
            print("Error reading file:", e)

def modify_account(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        try:
            with open('accounts.data', 'rb') as infile:
                oldlist = pickle.load(infile)

            account_found = False
            for item in oldlist:
                if item.accNo == num:
                    if item.check_password():
                        account_found = True
                        item.modify_account()
                        print("Account details have been updated.")
                    else:
                        print("Invalid password. Access denied.")

            if not account_found:
                print("No existing record with this account number.")
        except (FileNotFoundError, EOFError) as e:
            print("Error reading file:", e)

        save_accounts(oldlist)
    else:
        print("No records to modify.")

def save_accounts(accounts):
    with open('accounts.data', 'wb') as outfile:
        pickle.dump(accounts, outfile)

# Start of the program
ch = ''
num = 0
intro()

while ch != '7':
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. DEPOSIT AMOUNT")
    print("\t3. WITHDRAW AMOUNT")
    print("\t4. BALANCE ENQUIRY")
    print("\t5. ALL ACCOUNT HOLDER LIST")
    print("\t6. MODIFY AN ACCOUNT")
    print("\t7. EXIT")
    ch = input("Select Your Option (1-7): ")

    if ch == '1':
        write_account()
    elif ch == '2':
        num = int(input("\tEnter The account No.: "))
        deposit_and_withdraw(num, 1)
    elif ch == '3':
        num = int(input("\tEnter The account No.: "))
        deposit_and_withdraw(num, 2)
    elif ch == '4':
        num = int(input("\tEnter The account No.: "))
        display_balance(num)
    elif ch == '5':
        display_all()
    elif ch == '6':
        num = int(input("\tEnter The account No.: "))
        modify_account(num)
    elif ch == '7':
        print("\tThanks for using the our Bank  System")
    else:
        print("Invalid choice. Please try again.")
