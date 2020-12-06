###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################

import numpy as np

class User_Account:
    def __init__(self, name, acc_number, card_number, pin_num, balance):
        self.name = name
        self.acc_no = acc_number
        self.card_no = card_number
        self._pin_no = pin_num
        self.rem_attempts = 3
        self.history = []
        self.balance = balance
        self.min_balance = 1000

    def __eq__(self, value):
        if type(value) == str:
            return self.card_no == value
        else:
            return self.card_no == value.card_no

    def __ne__(self, value):
        if type(value) == str:
            return self.card_no != value
        else:
            return self.card_no != value.card_no

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def reset_pin(self, pin):
        self._pin_no = pin

    def chk_pin(self, pin):
        return self._pin_no == pin

    def wrong_pin(self):
        self.rem_attempts -= 1

    def correct_pin(self):
        self.rem_attempts = 3

    def is_min_balance(self):
        return self.balance < self.min_balance

    def get_info(self):
        return f"""
Name: {self.name} \n
Account Number: {self.acc_no[0:2] + '****' + self.acc_no[-2:]} \n
Card Number: {self.card_no[0:2] + '****' + self.card_no[-2:]} \n
"""


def get_user_accounts():
    user_accounts = []
    user_accounts.append(User_Account(
        "John Doe", "A20201", "120201", "1221", 5000))
    user_accounts.append(User_Account(
        "Doe John", "A20202", "120202", "1222", 7000))
    user_accounts.append(User_Account(
        "Apple Doe", "A20203", "120203", "1223", 15000))
    user_accounts.append(User_Account(
        "Banana Doe", "A20204", "120204", "1224", 1500))
    return user_accounts


def read_accounts_from_file():
    details = np.genfromtxt('./user_accounts_data.csv',
                            delimiter=',',
                            skip_header=True,
                            dtype=None)
    user_accounts = []
    for usr in details:
        user_accounts.append(User_Account(usr[0].decode("utf-8"),
                                          usr[1].decode("utf-8"),
                                          str(usr[2]),
                                          str(usr[3]),
                                          int(usr[4])))
    return user_accounts


if __name__ == "__main__":
    print(read_accounts_from_file())
    print(get_user_accounts())
