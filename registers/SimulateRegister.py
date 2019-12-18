# Simulate Register Class

from config import MsgTerm

from .RegisterBase import RegisterBase

class SimulateRegister(RegisterBase):
    # Constructor
    def __init__(self, config):
        RegisterBase.__init__(self, config)

    # Check
    def check(self):
        MsgTerm.text('Simulate check register')
        MsgTerm.success('Simulate result: Ok')
        return True

    # list
    def list(self):
        MsgTerm.text('Simulate list register')
        MsgTerm.success('Simulate result: Ok')
        return True
