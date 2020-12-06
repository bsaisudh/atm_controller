# ATM - Machine

![APM](https://img.shields.io/apm/l/vim-mode)
![PYT](https://img.shields.io/badge/Language-Python-blue)
![VER](https://img.shields.io/badge/Version-v1.0-yellowgreen)

## Overview

A simple and secure ATM controller built using **Queued State Machine** architecture on python. The design pattern is a unique implementation from scratch and is highly scalable. It is easy to add unit tests for this architecture.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/bsaisudh/atm_controller/blob/master/LICENSE) file for details

## Features

1. Read account information from the file
2. View account information
3. Withdraw money
4. Deposit money
5. Change PIN
6. Transaction history

## Prerequisites

The code is implemented in Python and has the following dependency:

* python3
  * NumPy
  * random
  * copy
  * warnings
  * DateTime

Note: All dependencies come with the default installation of python3

## Before running the code

### User accounts

The **ATM Controller** reads the user account information from the [user_accounts_data.csv](https://github.com/bsaisudh/atm_controller/blob/master/user_accounts_data.csv) file. The default file has 4 user accounts listed below. Once the controller starts running the user doesn't have permissions to update the user accounts through UI. but can be done through API Calls. The *card number* should be strictly 6 digits and the *account number* should be strictly 6 alphanumeric characters. The *PIN* should be strictly 4 digits.

```bash
Name         acc_number     card_number     pin_num     balance
John Doe     A20201         120201          1221        5000
Doe John     A20202         120202          1222        7000
Apple Doe    A20203         120203          1223        15000
Banana Doe   A20204         120204          1224        1500
```

## Running the code

* Clone the repository

```bash
git clone --recursive https://github.com/bsaisudh/atm_controller.git
```

* Go to the cloned location and run [*main.py*](https://github.com/bsaisudh/atm_controller/blob/master/main.py) file

```bash
python main.py
```

## State Diagram Overview

<div align="center">
  <img src="https://github.com/bsaisudh/atm_controller/blob/master/misc/State_dig_overview.PNG"/>
</div>

### Updating UI

The module takes input and displays text using 4 functions namely:

* disp_options
* get_option
* get_input

These four functions can either be changed or overridden by a wrapper class and it is enough to add UI hooks to the above-mentioned functions alone.

### Updating cash bin

Cash bin API has to be added to *is_cash_avaialbe()* function. The ATM Controller checks before the user can withdraw cash.

### Updating bank information

There is no option for the user to update the user account details through UI. The developer can call *update_user_accounts_data( )* API whenever user details have to be updated. To read the account details from ATM controller call *get_user_accounts_data()* API.

## Sample Output

<div align="center">
  <img src="https://github.com/bsaisudh/atm_controller/blob/master/misc/sample.PNG"/>
</div>

## Contact authors

Bala Murali Manoghar Sai Sudhakar <bsaisudh@terpmail.edu>