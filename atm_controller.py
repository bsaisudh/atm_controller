###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################

import random
import copy
from datetime import datetime

from utils import Queue
from user_accounts import User_Account, get_user_accounts, read_accounts_from_file


class ATM_Controller:
    """ATM controller class
    """
    def __init__(self, user_accounts):
        """Initialization

        Args:
            user_accounts (list): user account details from bank
        """
        self.user_accounts = user_accounts

        self.options = None
        self.option_states = []

        self.q = Queue()
        self.q.enqueue(self.init)

        self.curr_acc = None

    def run_state_machine(self):
        """State machine loop
        """
        while self.q.len() > 0:
            # if type(self.q.peek(0)) == tuple:
            #     print(f"----------- {self.q.peek(0)[0].__name__} -----------")
            #     print(f"----------- {self.q.peek(0)[1]} -----------")
            # else:
            #     print(f"----------- {self.q.peek(0).__name__} -----------")

            state_info = self.q.dequeue()
            if type(state_info) == tuple:
                state_info[0](*state_info[1])
            else:
                state_info()

    def update_user_accounts_data(self, usr_accounts):
        """API to update user details

        Args:
            user_accounts (list): user account details from bank
        """
        self.user_accounts = usr_accounts
        
    def get_user_accounts_data(self):
        """API to get updated user details from ATM

        Returns:
            user_accounts (list): user account details from ATM
        """
        return copy.deepcopy(self.user_accounts)
    
    ######################
    #       STATES       #
    ######################
    def init(self):
        """Initializing ATM controller
        """
        self.atm_print("Initializing ATM Machine...\n")
        self.q.enqueue(self.transaction_init)

    def transaction_init(self):
        """Initialize transaction
        """
        self.options = ["Press to enter"]
        self.option_states = [self.transaction_start]
        self.q.enqueue([self.disp_options, self.get_option])

    def transaction_start(self):
        """Start a transaction
        """
        self.atm_print("\nWelcome\n")
        self.options = ["Swipe card", "Cancel"]
        self.option_states = [self.swipe_card_menu, self.cancel_transaction]
        self.q.enqueue([self.disp_options, self.get_option])

    def swipe_card_menu(self):
        """Menu options when card is swiped
        """
        self.q.enqueue((self.get_input,
                        [["Enter 6 digit card number (Enter 'Q/q' to cancel): ",
                          "Enter 4 digit pin (Enter 'Q/q' to cancel): "],
                         self.swipe_card]), front=True)

    def swipe_card(self, c_no, pin):
        """Process swiped card information and check input validity

        Args:
            c_no (str): Card number 6 digits
            pin (str): PIN - 4 digits
        """
        c_no = str(c_no)
        pin = str(pin)
        c_u_acc = None
        # check if card number is valid
        for usr_acc in self.user_accounts:
            if usr_acc == c_no:
                c_u_acc = usr_acc
                break
        #Check if pin number is correct
        if c_u_acc is not None:
            # Card is locked or if there are available attempts
            if c_u_acc.rem_attempts > 0:
                if c_u_acc.chk_pin(pin):
                    c_u_acc.reset_attempts()
                    self.curr_acc = c_u_acc
                    self.atm_print("Login success")
                    self.q.enqueue(self.disp_acc_info)
                else:
                    self.atm_print("Invalid pin number try again")
                    c_u_acc.rem_attempts -= 1
                    self.atm_print(f"Number of attempts remaining : {c_u_acc.rem_attempts}")
                    if c_u_acc.rem_attempts <= 0:
                        self.atm_print(
                            "Number of wrong pin attempts exceeded. Contact bank to retrive the card.")
                    self.q.enqueue(self.cancel_transaction, front=True)
            else:
                self.atm_print(
                    "Number of wrong pin attempts exceeded. Contact bank to retrive the card.")
                self.q.enqueue(self.cancel_transaction, front=True)
        else:
            self.atm_print("Invalid card number try again")
            self.q.enqueue(self.cancel_transaction, front=True)

    def disp_acc_info(self, discard=None):
        """Display account infomation and availalbe options

        Args:
            discard (None, optional): Not used. Defaults to None. necessary when calling through get_inputs function
        """
        self.atm_print("\n")
        self.atm_print(self.curr_acc.get_info())
        self.options = ["Balance enqiry",
                        "Withdraw Money",
                        "Deposit Money",
                        "Change Pin",
                        "View Transaction History",
                        "Cancel Transaction"]
        self.option_states = [self.disp_bal,
                              self.withdraw_menu,
                              self.deposit_menu,
                              self.change_pin_menu,
                              [self.disp_transac_history, self.disp_acc_info],
                              self.cancel_transaction]
        self.q.enqueue([self.disp_options, self.get_option])

    def disp_bal(self):
        """Display balance
        """
        self.atm_print("\nAccount Balance: \n")
        self.atm_print(f"{self.curr_acc.balance} \n\n")
        self.options = ["Back to account menu", "Cancel"]
        self.option_states = [self.disp_acc_info, self.cancel_transaction]
        self.q.enqueue([self.disp_options, self.get_option])

    def withdraw_menu(self):
        """Withdrawal menu options
        """
        disp_str = "Enter amount to withdraw in USD (Enter 'Q/q' to cancel) : "
        next_state = self.withdraw
        self.q.enqueue((self.get_input, [disp_str, next_state]), front=True)

    def withdraw(self, amt):
        """withdraw cash"""
        amt = str(amt)
        # allow user to cancel transaction
        if amt == "q" or amt == "Q":
            self.q.enqueue(self.cancel_transaction, front=True)
        else:
            amt = int(amt)
            # check if amount can be withdrawn
            if amt > self.curr_acc.balance:
                self.atm_print(
                    f"Not enough funds in account \nEnter amount less than {self.curr_acc.balance}")
                self.q.enqueue(self.disp_acc_info)
            else:
                if self.is_cash_avaialbe(amt):
                    self.q.enqueue((self.update_balance, [-amt]))
                    self.q.enqueue((self.update_transac_history, [-amt]))
                    self.q.enqueue((self.get_input, ["Take cash out and press 'Enter' to continue",
                                                     self.disp_acc_info]))
                else:
                    self.atm_print("Cash not availalbe in atm")
                    self.q.enqueue(self.disp_acc_info)

    def is_cash_avaialbe(self, amt):
        """API for checking if cash is avaialbe in the atm bin

        Args:
            amt (int): amount to check

        Returns:
            bool: avaiability of amount
        """
        return True

    def deposit_menu(self):
        """Cash deposit menu
        """
        disp_str = "Enter amount to deposit in USD (Pess 'Q/q' to cancel) : "
        next_state = self.deposit
        self.q.enqueue((self.get_input, [disp_str, next_state]), front=True)

    def deposit(self, amt):
        """Deposit cash to user account

        Args:
            amt (int): amount to be deposited
        """
        amt = str(amt)
        # Allow user to cancel transaction
        if amt == "q" or amt == "Q":
            self.q.enqueue(self.cancel_transaction, front=True)
        else:
            amt = int(amt)
            self.q.enqueue((self.get_input, ["Press Q/q to cancel or deposit cash in tray and press 'Enter' to continue : ",
                                             self.cash_deposit_tray]))
            self.q.enqueue((self.update_balance, [amt]))
            self.q.enqueue((self.update_transac_history, [amt]))
            self.q.enqueue(self.disp_acc_info)

    def cash_deposit_tray(self, discard=None):
        """Wait function to allow user to place cash in tray and press enter

        Args:
            discard (None, optional): Not used. Defaults to None. necessary when calling through get_inputs function
        """
        self.atm_print("Cash Collected")

    def update_balance(self, amt):
        """Update balance after successgul transaction

        Args:
            amt (int): amount deposited (positive) or withdrawn (negative)
        """
        self.curr_acc.balance += amt
        self.atm_print(f"\n\nCurrent balance: {self.curr_acc.balance}\n\n")

    def update_transac_history(self, amt):
        """Track transaction history

        Args:
            amt (int): amount deposited (positive) or withdrawn (negative)
        """
        transac_id = random.randint(100000, 999999)
        date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        self.curr_acc.history.append(
            [date, transac_id, amt, self.curr_acc.balance])

    def disp_transac_history(self):
        """Display transaction in reverse cronological order
        """
        self.atm_print("\n\n Previous Transactions: \n\n")
        self.atm_print("Date     Transaction ID      Amount      Final Balance")
        transac_history = self.curr_acc.history
        for i in range(len(transac_history)-1, -1, -1):
            self.atm_print(transac_history[i])
        self.atm_print("\n\n\n")

    def change_pin_menu(self):
        """Menu to change pin
        """
        self.q.enqueue((self.get_input,
                        [["Enter old pin (Enter 'Q/q' to cancel): ",
                          "Enter new pin (Enter 'Q/q' to cancel): ",
                          "Confirm pin (Enter 'Q/q' to cancel): "],
                         self.change_pin]), front=True)
        self.q.enqueue(self.disp_acc_info)

    def change_pin(self, old_pin, new_pin, confirm_pin):
        """Check validity and change the pin number

        Args:
            old_pin (str): PIN - 4 digits
            new_pin (str): PIN - 4 digits
            confirm_pin (str): PIN - 4 digits
        """
        if self.curr_acc.chk_pin(old_pin):
            if len(new_pin) == 4 and new_pin == confirm_pin:
                self.curr_acc.reset_pin(new_pin)
                self.atm_print("New pin updated")
            else:
                self.atm_print(
                    "New pin and confirm pin are different and pin number should be 4 digits")
                self.atm_print("Try again \n\n")
        else:
            self.atm_print("incorrect pin")

    def cancel_transaction(self):
        """Cancel ongoing transaction and logout
        """
        if self.curr_acc is not None:
            self.curr_acc = None
            self.atm_print("Logging out of current account")
        self.atm_print("Thank you for visiting our services")
        self.q.flush()
        self.q.enqueue(self.transaction_start)

    def exit(self):
        """Exit handling
        """
        self.atm_print("exit")

    def disp_options(self):
        """Display options available to user
        """
        for ndx, op in enumerate(self.options):
            self.atm_print(f"{ndx+1} -> {op}")
        self.atm_print("\n")

    def get_option(self):
        """get user input and go to corresponding state
        """
        selection = int(input("Select an option: ")) - 1
        if not(0 <= selection < len(self.options)):
            self.atm_print("Invalid option, cancelling transaction...")
            self.q.enqueue([self.cancel_transaction], front=True)
        else:
            self.q.enqueue(self.option_states[selection])

    def get_input(self, disp_str, next_state):
        """get user input and send the data to next state

        Args:
            disp_str (list of str): string to be displayed to user
            next_state (list or state): state to which user input has to be sent
        """
        self.atm_print("\n")
        if type(disp_str) != list:
            usr_input = input(disp_str)
            if str(usr_input) == "q" or str(usr_input) == "Q":
                self.q.enqueue(self.cancel_transaction, front=True)
                return
            else:
                self.q.enqueue((next_state, [usr_input]), front=True)
        else:
            if next_state != list:
                inputs = []
                for string in disp_str:
                    usr_input = input(string)
                    if str(usr_input) == "q" or str(usr_input) == "Q":
                        self.q.enqueue(self.cancel_transaction, front=True)
                        return
                    else:
                        inputs.append(usr_input)
                self.q.enqueue((next_state, inputs), front=True)
            else:
                inputs = []
                for string in disp_str:
                    usr_input = input(string)
                    if str(usr_input) == "q" or str(usr_input) == "Q":
                        self.q.enqueue(self.cancel_transaction, front=True)
                        return
                    else:
                        inputs.append(usr_input)
                for i in range(len(inputs)-1, -1, -1):
                    self.q.enqueue((next_state[i], inputs[i]), front=True)
    
    def atm_print(self, string):
        """Print info to user

        Args:
            string (str): string to display
        """
        print(string)


if __name__ == "__main__":
    atm = ATM_Controller(read_accounts_from_file())
    atm.run_state_machine()
