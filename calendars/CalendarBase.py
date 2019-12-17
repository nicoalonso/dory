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

    def getListEvents(self, debug=False):
        MsgTerm.alert('List events is not implemented', nl=True)
        return False

    # Return today's event
    def getTodayEvent(self):
        MsgTerm.alert('Today event is not implemented', nl=True)
        return False