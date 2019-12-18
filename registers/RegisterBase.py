# Register Base Class

from config import MsgTerm

class RegisterBase:

    # Constructor
    def __init__(self, config):
        self.cfg = config

    # Check
    def check(self):
        MsgTerm.error('Error: Check is not implemented', nl=True)
        return False

    # Get the list of records in register
    def list(self):
        MsgTerm.error('Error: List is not implemented', nl=True)
        return False
