# Base Class for Calendars

from config import MsgTerm

class CalendarBase:
    
    # Constructor
    def __init__(self, config):
        self.cfg = config

    # Check connection to Calendar
    def check(self):
        MsgTerm.alert('Check is not implemented', nl=True)
        return False