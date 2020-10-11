import random


def luhn_algorithm(account_indefier):
    account_indefier = account_indefier[:15]
    digits = [int(x) for x in account_indefier]
    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] = digits[i]*2
    for i in range(len(account_indefier)):
        if digits[i] > 9:
            digits[i] -= 9
    digits_sum = sum(digits)
    checksum = 10 - (digits_sum % 10)
    if checksum < 10:
        return account_indefier + str(checksum)
    else:
        return account_indefier + str(0)


class Card:

    def __init__(self):
        account_indefier = '400000' + str("%09d" % random.randint(0, 9999999999))
        self.card_number = luhn_algorithm(account_indefier)
        self.PIN = "%04d" % random.randint(0, 9999)
        print("\nYour card has been created")

    def get_card_number(self):
        return self.card_number

    def get_PIN(self):
        return self.PIN
