class Transaction:
    def __init__(owner, sender, receiver, amount):
        owner.sender = sender
        owner.receiver = receiver
        owner.amount = amount


class Bank:
    def __init__(owner):
        owner.total_bal = 0
        owner.total_loanAmount = 0
        owner.loan_enable = True
        owner.transaction_history = []

    def get_total_bal(owner):
        return owner.total_bal

    def get_total_loanAmount(owner):
        return owner.total_loanAmount

    def enable_loan(owner):
        owner.loan_enable = True

    def disable_loan(owner):
        owner.loan_enable = False

    def add_transaction(owner, transaction):
        owner.transaction_history.append(transaction)


class Admin:
    def __init__(owner, bank):
        owner.bank = bank

    def create_account(owner, name, initial_deposit):
        user = User(name)
        if user.create_account(initial_deposit):
            owner.bank.total_bal += initial_deposit
            return user
        return None

    def get_total_bal(owner):
        return owner.bank.get_total_bal()

    def get_total_loanAmount(owner):
        return owner.bank.get_total_loanAmount()

    def enable_loan_feature(owner):
        owner.bank.enable_loan()

    def disable_loan_feature(owner):
        owner.bank.disable_loan()

    def get_transaction_history(owner):
        return owner.bank.transaction_history


class User:
    def __init__(owner, name):
        owner.name = name
        owner.balance = 0
        owner.loanLimit = 0
        owner.transaction_history = []

    def create_account(owner, initial_deposit):
        if initial_deposit > 0:
            owner.balance = initial_deposit
            owner.loanLimit = initial_deposit * 2
            return True
        return False

    def deposit(owner, bank, amount):
        if amount > 0:
            owner.balance += amount
            bank.total_bal += amount
            owner.loanLimit = owner.balance * 2
            transaction = Transaction(owner.name, owner.name, amount)
            owner.transaction_history.append(transaction)
            return True
        return False

    def withdraw(owner, bank, amount):
        if amount > 0 and amount <= owner.balance and amount <= bank.total_bal:
            owner.balance -= amount
            bank.total_bal -= amount
            transaction = Transaction(owner.name, owner.name, -amount)
            owner.transaction_history.append(transaction)
            return True
        elif amount > bank.total_bal:
            print("It's a Bankrupt Bank. Not possible to withdraw.")
        return False

    def transfer(owner, recipient, amount):
        if amount > 0 and amount <= owner.balance:
            owner.balance -= amount
            recipient.balance += amount
            transaction = Transaction(owner.name, recipient.name, amount)
            owner.transaction_history.append(transaction)
            recipient.transaction_history.append(transaction)
            return True
        return False

    def check_balance(owner):
        return owner.balance

    def take_loan(owner, bank, amount):
        if bank.loan_enable and amount <= owner.loanLimit and amount > 0 and amount <= bank.total_bal:
            owner.balance += amount
            bank.total_loanAmount += amount
            bank.total_bal -= amount
            transaction = Transaction(owner.name, owner.name, amount)
            owner.transaction_history.append(transaction)
            bank.add_transaction(transaction)
            return True
        return False

    def get_transaction_history(owner):
        return owner.transaction_history


bank = Bank()

admin = Admin(bank)

Kasfi = admin.create_account('Kasfi', 2000)

Nahiyan = admin.create_account('Nahiyan', 1000)

Kasfi.deposit(bank, 5000)

print(Kasfi.check_balance())
print(Nahiyan.check_balance())

Kasfi.withdraw(bank, 1000)
Kasfi.transfer(Nahiyan, 500)

admin.enable_loan_feature()

Kasfi.take_loan(bank, 1000)

print(Kasfi.check_balance())

print(admin.get_total_loanAmount())
print(admin.get_total_bal())

transaction_history = Kasfi.get_transaction_history()
for transaction in transaction_history:
    print(
        f"Sender: {transaction.sender}, Receiver: {transaction.receiver}, Amount: {transaction.amount}")