###############################################################################
# Author        : Bala Murali Manoghar
# License       : "MIT"
# Copyright       :"Copyright 2020, ATM Machine project"
# Version       : 1.0
# Email         : bsaisudh@terpmail.edu
###############################################################################

import numpy as np
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

from user_accounts import read_accounts_from_file
from atm_controller import ATM_Controller


if __name__ == "__main__":
    atm = ATM_Controller(read_accounts_from_file())
    atm.run_state_machine()
