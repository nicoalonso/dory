#!/usr/bin/python3

from config import MsgTerm

from .CalendarBase import CalendarBase
from .GoogleCalendar import GoogleCalendar
from .GoogleCalendarEvent import GoogleCalendarEvent

# List of calendars defined
calendarTypes = {
    'google': GoogleCalendar,
    'default': CalendarBase
}

# Get calendar
def getCalendar(cfg):
    '''get calendar
    
    Returs the class instance of calendar defined by the user
    
    Args:
        cfg {Configurize}: Configuration
    
    Returns:
        CalendarBase: Instance inherit from CalendarBase
    '''

    typeCal = cfg.get('calendar', 'type', None)
    MsgTerm.debug('Calendar type: %s' % typeCal)
    if typeCal in calendarTypes:
        targetClass = calendarTypes[ typeCal ]
        return targetClass(cfg)
    else:
        return CalendarBase(cfg)
