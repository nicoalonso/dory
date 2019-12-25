#!/usr/bin/python3

from msgterm import MsgTerm


class CalendarBase:
    '''Calendar base class
    
    Args:
        config (Configurize): The config is used for get the user configuration

    Attributes:
        cfg    (Configurize): Configuration object
    '''

    def __init__(self, config):
        self.cfg = config

    # Check connection to Calendar
    def check(self):
        MsgTerm.error('Error: Check is not implemented', nl=True)
        return False

    def list(self, debug=False):
        MsgTerm.error('Error: List events is not implemented', nl=True)
        return False

    # Return today's event
    def getTodayEvent(self):
        MsgTerm.error('Error: Today event is not implemented', nl=True)
        return False
