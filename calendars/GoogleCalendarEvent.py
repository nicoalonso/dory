# Google Calendar Event

from datetime import datetime, date
from dateutil import parser

from config import MsgTerm

# Class Calendar Event
class GoogleCalendarEvent:
    '''Class Google Calendar Event
    
    Use this to parse and store the google calendar information

    Args:
        calEvent (dict): Google Calendar Event from API

    Attributes:
        calEvent (dict): Store a copy of Google Calendar Event
        valid (bool): The event is valid. An event is valid when have start and end datetime
        start (datetime): event start
        end (datetime): event end
        delta (timedelta): Used for calc event time
        hours (int): Duration of the event
    '''

    def __init__(self, calEvent):
        self.calEvent = calEvent
        self.valid = False
        self.start = None
        self.end = None
        self.delta = None
        self.hours = 0
        # Methods
        self.validate()
        self.parse()


    def validate(self):
        '''Validate
        
        Check if the event is valid
        An event is valid when have start and end datetime
        
        Returns:
            bool -- Returns if the event is valid
        '''

        start = self.calEvent.get('start')
        end = self.calEvent.get('end')
        if start and end:
            startDate = start.get('dateTime')
            endDate = end.get('dateTime')

            self.valid = startDate and endDate

        return self.valid


    def parse(self):
        '''Parse event
        
        Parse event and store the relevant information
        '''

        if self.valid:
            self.start = parser.parse(self.calEvent['start']['dateTime'])
            self.end = parser.parse(self.calEvent['end']['dateTime'])
            self.delta = self.end - self.start
            self.hours = self.delta.seconds / 3600
            self.summary = self.calEvent['summary']


    def isToday(self):
        '''isToday
        
        Check if the event is today
        '''

        return (date.today() == self.start.date())


    def print(self, showToday=False):
        '''Print event
        
        Print event on the terminal
        
        Args:
            showToday {bool} -- highlight of today's event (default: {False})
        '''

        bold = False
        asterisk = ''
        if showToday and self.isToday():
            bold = True
            asterisk = '* Today *'

        msg = '%s, %s to %s : %d hours [ %s ] %s' % (
            self.start.date().strftime('%d/%m/%Y'),
            self.start.strftime('%H:%M'),
            self.end.strftime('%H:%M'),
            self.hours,
            self.summary,
            asterisk
        )
        MsgTerm.info(msg, bold=bold, label='-')


    def debug(self):
        '''Debug
        
        Use only development purposes
        '''
        MsgTerm.jsonPrint( self.calEvent )
