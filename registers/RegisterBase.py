#!/usr/bin/python3

from msgterm import MsgTerm


class RegisterBase:
    '''Register base class
    
    Args:
        config (Configurize): User configuration

    Attributes:
        cfg (Configurize): User configuration
    '''

    def __init__(self, config):
        self.cfg = config


    def check(self):
        '''Check
        
        Method to override for inherit class
        Check if the connection to the register is successfully
        
        Returns:
            bool: check result
        '''

        MsgTerm.error('Error: Check is not implemented', nl=True)
        return False


    def list(self):
        '''Get list
        
        Method to override for inherit class
        Show on the terminal the list of current records
        Use for debugging
        
        Returns:
            bool: list result
        '''

        MsgTerm.error('Error: List is not implemented', nl=True)
        return False
