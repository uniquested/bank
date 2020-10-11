from .Card import *
from .Database import *


class Account:

    def __init__(self):
        self.balance = 0
        self.card = Card()

    def check_balance(self):
        return self.balance

    def add_to_db(self):
        with Database() as db:
            db.execute("INSERT INTO card (number, pin) VALUES (" + self.card.get_card_number() + ", " + self.card.get_PIN() + ");")
            db.commit()

    def is_equal(self, card_number, PIN_number):
        if card_number == self.card.get_card_number() and PIN_number == self.card.get_PIN():
            return True
