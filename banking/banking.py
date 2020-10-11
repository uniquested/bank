import os
from .Account import *
from .Database import *

current = None


def entry_interface():
    print("1. Create an account\n2. Log into account\n0. Exit")
    case = input()
    if case == "1":
        create_account()
    elif case == "2":
        log_into_account()
    elif case == "0":
        print("Bye!")
        exit()


def account_interface(user_number):
    global logged_out
    print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
    case = input()
    if case == "1":
        with Database() as db:
            db.execute("SELECT balance FROM card WHERE number = \"" + user_number + "\";")
            result = db.cur.fetchone()[0]
            print('\nBalance: ' + str(result) + '\n')
    elif case == "2":
        income = input("\nEnter income: ")
        with Database() as db:
            db.execute("UPDATE card SET balance = balance + " + str(income) + " WHERE number = \"" + user_number + "\";")
        print("Income was added!\n")
    elif case == "3":
        print("\nTransfer")
        transfer_card_number = input("Enter card number: ")
        number_validation(user_number, transfer_card_number)

    elif case == "4":
        logged_out = True
        with Database() as db:
            db.execute("DELETE  FROM card WHERE number = \"" + user_number + "\";")
            print("\nThe account has been closed!")

    elif case == "5":
        logged_out = True
        print("\nYou have successfully logged out!\n")
    elif case == "0":
        print("Bye!")
        exit()


def create_account():
    global current
    current = Account()
    current.add_to_db()
    print("Your card number:")
    print(current.card.get_card_number())
    print("Your card PIN:")
    print(current.card.get_PIN() + "\n")


def log_into_account():
    global current
    global logged_out
    user_number = input("\nEnter your card number: ")
    user_PIN = input("Enter your PIN: ")
    with Database() as db:
        db.execute("SELECT balance FROM card WHERE number = \"" + user_number + "\" AND pin = \"" + user_PIN + "\"")
        current = db.cur.fetchone()
    if current is not None:
        print("\nYou have successfully logged in!\n")
        while not logged_out:
            account_interface(user_number)
    else:
        print("\nWrong card number or PIN!\n")


def number_validation(user_number, transfer_number):
    with Database() as db:
        db.execute("SELECT balance FROM card WHERE number = \"" + user_number + "\"")
        user_balance = db.cur.fetchone()[0]
        db.execute("SELECT COUNT(*) FROM card WHERE number = \"" + transfer_number + "\"")
        row_count = db.cur.fetchone()[0]
    if user_number == transfer_number:
        print("You can't transfer money to the same account!\n")
    elif row_count > 0 and transfer_number == luhn_algorithm(transfer_number):
        transfer_balance = input("Enter how much money you want to transfer: ")
        if int(transfer_balance) > int(user_balance):
            print("Not enough money!\n")
        else:
            with Database() as db:
                db.execute("UPDATE card SET balance = balance - " + str(transfer_balance) + " WHERE number = \"" + user_number + "\";")
                db.execute("UPDATE card SET balance = balance + " + str(transfer_balance) + " WHERE number = \"" + transfer_number + "\";")
                print("Success!\n")
    elif transfer_number != luhn_algorithm(transfer_number):
        print("Probably you made a mistake in the card number. Please try again!\n")
    elif row_count == 0:
        print("Such a card does not exist.\n")


while True:
    logged_out = False
    if not os.path.exists('card.s3db'):
        open('card.s3db', 'w').close()
    with Database() as db:
        db.create_table()
    entry_interface()
