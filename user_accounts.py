###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################

import numpy as np

class User_Account:
    """User account information"""
    def __init__(self, name, acc_number, card_number, pin_num, balance):
        """Initialization

        Args:
            name (string): Name of user
            acc_number (string): 6 characer alphanumeric account number
            card_number (string): 6 digit card number
            pin_num (string): 4 digit pin number
            balance (int): account balance in USD
        """
        self.name = name
        self.acc_no = acc_number
        self.card_no = card_number
        self._pin_no = pin_num
        self.rem_attempts = 3
        self.history = []
        self.balance = balance
        self.min_balance = 1000

    def __eq__(self, value):
        """Equality operator overriding

        Args:
            value (same class or string): value to be compared

        Returns:
            bool: result of equality
        """
        if type(value) == str:
            return self.card_no == value
        else:
            return self.card_no == value.card_no

    def __ne__(self, value):
        """Non-equality operator overriding

        Args:
            value (same class or string): value to be compared

        Returns:
            bool: result of non-equality
        """
        if type(value) == str:
            return self.card_no != value
        else:
            return self.card_no != value.card_no

    def deposit(self, amount):
        """Update balance for depositing cash to user account

        Args:
            amount (int): Cash deposited
        """
        self.balance += amount

    def withdraw(self, amount):
        """Update balance for withdrawing cash form user account

        Args:
            amount (int): Cash withdrawn
        """
        self.balance -= amount

    def reset_pin(self, pin):
        """Reset access PIN

        Args:
            pin (str): 4 digit PIN
        """
        self._pin_no = pin

    def chk_pin(self, pin):
        """Check for correct pin to give access to user. Pin number is a private member

        Args:
            pin (str): 4 digit PIN

        Returns:
            bool: result of equality
        """
        return self._pin_no == pin

    def wrong_pin(self):
        """Update remaining attempts for wrong pin
        """
        self.rem_attempts -= 1

    def reset_attempts(self):
        """Reset number of wrong attempts
        """
        self.rem_attempts = 3

    def is_min_balance(self):
        """Check if current balance is less than minimum balance

        Returns:
            bool: true if balance is less than min
        return self.balance < self.min_balance
        """
        return self.balance < self.min_balance
    
    def get_info(self):
        """Generate accopunt information string
        """
        return f"""
Name: {self.name} \n
Account Number: {self.acc_no[0:2] + '****' + self.acc_no[-2:]} \n
Card Number: {self.card_no[0:2] + '****' + self.card_no[-2:]} \n
"""


def get_user_accounts():
    """Generate sample user accounts

    Returns:
        list: user account list
    """
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
    """Read user accounts from csv file

    Returns:
        list: user account list
    """
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
