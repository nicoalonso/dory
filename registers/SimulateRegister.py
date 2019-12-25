#!/usr/bin/python3

from msgterm import MsgTerm

from .RegisterBase import RegisterBase


class SimulateRegister(RegisterBase):
    '''Simulate register
    
    Use this to simulate the register
    Use only for development purposes
    
    Extends:
        RegisterBase

    Args:
        config (Configurize): User configuration
    '''

    def __init__(self, config):
        RegisterBase.__init__(self, config)


    def check(self):
        '''Check
        
        Check if the connection to the register is successfully
        
        Returns:
            bool: check result
        '''

        MsgTerm.text('Simulate check register')
        MsgTerm.success('Simulate result: Ok')
        return True


    def list(self):
        '''Get list
        
        Show on the terminal the list of current records
        Use for debugging
        
        Returns:
            bool: list result
        '''

        MsgTerm.text('Simulate list register')
        MsgTerm.success('Simulate result: Ok')
        return True
