import random  # We should import the random module in order to generate different random account numbers and passwords 
import os  # Then we should be Importing the os module to check file existence and to provide a functions for interacting with the operating system

# We should creat a Base Account class
class Account:
    def __init__(self, accountnumber, password, type_of_account, remaining_balance=0):
        self.accountnumber = accountnumber  # For Account number
        self.password = password  # For Password for the given account number provided
        self.type_of_account = type_of_account  # For slecting type of account to be opened that is (Business/Personal)
        self.remaining_balance = float(remaining_balance)  # Finally it is the total account balance left, which will be starting from 0 as default
    
    def deposit(self, amount):
        # Now it is the simpliest method to deposit the amount we want to put into an account
        self.remaining_balance = self.remaining_balance + amount
        print(f"Deposited Ngultrum{amount}. New remaining_balance: Ngultrum{self.remaining_balance}")
    
    def withdraw(self, amount):
        # Then after depositing there is also a method to withdraw the desired amount from an account
        if amount > self.remaining_balance:
            print("Insufficient funds.")# If the fund in the bank is insufficient
        else:
            self.remaining_balance = self.remaining_balance - amount
            print(f"Withdrew Ngultrum{amount}. New remaining_balance: Ngultrum{self.remaining_balance}")
    
    def check_remaining_balance(self):
        # To check the account balnce, it is the method to check account balance
        return self.remaining_balance

    def transfer(self, amount, recipient_account):
        # The way in order to transfer the amount to another account
        if amount > self.remaining_balance:
            print("Insufficient funds.")
        else:
            self.withdraw(amount)
            recipient_account.deposit(amount)
            print(f"Transferred Ngultrum{amount} to account {recipient_account.accountnumber}")

    def change_accountnumber(self, new_accountnumber):
        # if we want to change account number, we can use this Method 
        self.accountnumber = new_accountnumber

    def change_password(self, new_password):
        # Now if we feel unsecure we can change account passwordr using this Method 
        self.password = new_password

# We can add class called BusinessAccount class which is directly derived from the account
class BusinessAccount(Account):
    def __init__(self, accountnumber, password, remaining_balance=0, business_name=""):
        super().__init__(accountnumber, password, "Business", remaining_balance)
        self.business_name = business_name  # Now we can produce business name specific to BusinessAccount

# We can add another class for PersonalAccount, which is automatically derived from Account
class PersonalAccount(Account):
    def __init__(self, accountnumber, password, remaining_balance=0, owner_name=""):
        super().__init__(accountnumber, password, "Personal", remaining_balance)
        self.owner_name = owner_name  # We can give an owner name specific to PersonalAccount

def SAVE_ACCOUNT(account):
    """
    Save account details to file. Load all accounts, we should update the given account,
    and write them back to file.
    """
    accounts = load_accounts()  # Inorder to check the load existing accounts from file
    accounts[account.accountnumber] = account  # Then we have access to update or add the account
    with open('accounts.txt', 'w') as f: # The function with is called inorder to read the account.txt
        for acc in accounts.values():
            f.write(f"{acc.accountnumber},{acc.password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")

def load_accounts():
    """
    Load all accounts from file and return them as a dictionary.
    """#To Return them and to store in the dictionary
    accounts = {}
    if os.path.exists('accounts.txt'):  # Check if required files is exist in account.txt 
        with open('accounts.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(',')  # By using the fuction strip() and split() in order to Split line into parts
                accountnumber, password, type_of_account, remaining_balance = parts[:4]
                remaining_balance = float(remaining_balance)
                if type_of_account == "Business": #if we want to create the business purposes
                    business_name = parts[4] # Naming the bussiness account  
                    accounts[accountnumber] = BusinessAccount(accountnumber, password, remaining_balance, business_name)
                elif type_of_account == "Personal":
                    owner_name = parts[5] #Now making account for personal usage
                    accounts[accountnumber] = PersonalAccount(accountnumber, password, remaining_balance, owner_name)
    return accounts

def create_account():
    """
    Create a new account based on user input and save it to file.
    """
    accountnumber = str(random.randint(10000, 99999))  # In order to generate the random account number that once the random was called
    password = str(random.randint(1000, 9999))  # to generate the random password that once the random function was called
    type_of_account = input("Enter account type (Business/Personal): ") #Entering the account you want to open
    
    if type_of_account == "Business":#If we want to open the bussiness account
        business_name = input("Enter business name: ")#name of the bussiness
        account = BusinessAccount(accountnumber, password, business_name=business_name)
    else:
        owner_name = input("Enter owner name: ")#If we want to open the personal account
        account = PersonalAccount(accountnumber, password, owner_name=owner_name)
    #For the name of the personal account to be created
    SAVE_ACCOUNT(account)  # Now after all we can Save the new account to file that is stored in accounts.txt
    print(f"Account created! Your account number is {accountnumber} and password is {password}")

def login(accounts):#After creating an account we can logint the account to do digital banking works
    """
    Log in to an account by verifying the account number and password.
    """
    accountnumber = input("Enter account number: ")
    password = input("Enter password: ")# Using the given account number and the password
    
    account = accounts.get(accountnumber)
    if account and account.password == password:
        print(f"Welcome, {account.type_of_account} account holder!")# the given account number and password should be matched in order to login in the account
        return account
    else:
        print("Invalid account number or password.")# if it is incorrect, we will be redirected
        return None

def delete_account(account):#If the account is to be deleted
    """
    Delete an account from file by removing it from the accounts dictionary
    and writing the updated dictionary back to file.
    """
    accounts = load_accounts()  # In oder to delete the account we should Load existing accounts
    if account.accountnumber in accounts:
        del accounts[account.accountnumber]  # Then we can Remove the account from the stored or load existing account
        with open('accounts.txt', 'w') as f:
            for acc in accounts.values():#reading the accounts.txt  if the account is deleted
                f.write(f"{acc.accountnumber},{acc.password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")
        print("Account deleted successfully.")# account removed seccessfully
    else:
        print("Account not found.")

def change_account_details(account):# in order to change the account number and the password on our own
    """
    Change account details like account number or password based on user choice.
    """
    print("\n1. Change Account Number\n2. Change Password")
    choice = input("Enter choice: ")
    
    if choice == '1':#To change the account number
        new_accountnumber = input("Enter new account number: ")#new account number to be implemmended
        accounts = load_accounts()
        if new_accountnumber in accounts:
            print("Account number already exists.")
        else:
            old_accountnumber = account.accountnumber
            account.change_accountnumber(new_accountnumber)#account number should be matched with given account number
            SAVE_ACCOUNT(account)  # then need to save the account with the new account number which was changed earlier
            if old_accountnumber in accounts:
                del accounts[old_accountnumber]  # Then we can be able to remove the old account entry
                with open('accounts.txt', 'w') as f:
                    for acc in accounts.values():#For reading the accounts.txt
                        f.write(f"{acc.accountnumber},{acc.password},{acc.type_of_account},{acc.remaining_balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")
            print("Account number was changed successfully.")
    elif choice == '2':
        new_password = input("Enter new password: ")#After changing account number, if we want to change the password, we can use following code
        account.change_password(new_password)
        SAVE_ACCOUNT(account)  # Then after Saving,  the account with the new password is also saved
        print("Password was changed successfully.")
    else:
        print("Invalid choice.")#password given to be changed should be perfectly matched

def main():#Main function
    """
    Main function to display menu and handle user choices.
    """
    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':# Now new account is going to be produced
            create_account()
        elif choice == '2':
            accounts = load_accounts()  # After the account is being produced, Load existing accounts can be opened
            account = login(accounts)
            if account:#after the account is being logged in, we can used the banking services facilities
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check remaining_balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout")
                    CHOICES = input("Enter choice: ")
                    
                    if CHOICES == '1':#Now we can deposite the desired amount of money
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        SAVE_ACCOUNT(account)  # Then we should Save account after the money has been deposited
                    elif CHOICES == '2':#We can also withdraw the deposited money back
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        SAVE_ACCOUNT(account)  # As usual we should Save account after withdrawal
                    elif CHOICES == '3':#Then we can also check the remaining balance after deposition or withdrawal of money
                        print(f"remaining_balance: Ngultrum {account.check_remaining_balance()}")
                    elif CHOICES == '4':#In order to transfer the money, we should check the existing account number
                        recipient_number = input("Enter recipient account number: ")#Entering the recipent account number
                        recipient = accounts.get(recipient_number)
                        if recipient:#Recipent account number should be exactly matched
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, recipient)
                            SAVE_ACCOUNT(account)  # then we should Save sender account
                            SAVE_ACCOUNT(recipient)  # And also we should Save the recipient account
                        else:
                            print("Recipient account does not exist.")#If wrong account number is entered
                    elif CHOICES == '5':
                        delete_account(account)  # We can also delete the existing account and able to exit to main menu
                        break
                    elif CHOICES == '6':#We can also change the details of the account selecting this choices
                        change_account_details(account)
                    elif CHOICES == '7':
                        SAVE_ACCOUNT(account)  # Now if we want to logout the song, the account will be Saved before logging out
                        print("Logged out.")#Logging out
                        break
        elif choice == '3':#In order to exit the banking system
            break
        else:
            print("Invalid choice. Try again.")#any other wrong input

if __name__ == "__main__":#Calling of the mainfunction 
    main()
