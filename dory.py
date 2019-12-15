#!/usr/bin/python3
# Dory project

from config/msgterm import MsgTerm
from config/configurize import Configurize


class Dory:

    # Constructor
    def __init__(self):
        # Set verbosity
        MsgTerm.verbosity(MsgTerm.DEBUG)
        # Load config file
        self.cfg = Configurize('dory')
        self.cfg.load()



# Execute
if __name__ == '__main__':
    dory = Dory()
