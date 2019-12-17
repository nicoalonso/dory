# Google Calendar Event

from datetime import datetime, date
from dateutil import parser

from config import MsgTerm

# Class Calendar Event
class GoogleCalendarEvent:

    # Constructor
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


    # Check if is an event valid
    # The event valid have datetime in start and end keys
    # 
    # @return boolean
    # 
    def validate(self):
        start = self.calEvent.get('start')
        end = self.calEvent.get('end')
        if start and end:
            startDate = start.get('dateTime')
            endDate = end.get('dateTime')

            self.valid = startDate and endDate

        return self.valid

    # Parse event
    def parse(self):
        if self.valid:
            self.start = parser.parse(self.calEvent['start']['dateTime'])
            self.end = parser.parse(self.calEvent['end']['dateTime'])
            self.delta = self.end - self.start
            self.hours = self.delta.seconds / 3600
            self.summary = self.calEvent['summary']

    # Check if the day is today
    def isToday(self):
        return (date.today() == self.start.date())

    # Print event in terminal
    def print(self, showToday=False):
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

    # Debug
    def debug(self):
        MsgTerm.jsonPrint( self.calEvent )

    