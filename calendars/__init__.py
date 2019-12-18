# Package calendar

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
    typeCal = cfg.get('calendar', 'type', None)
    MsgTerm.debug('Calendar type: %s' % typeCal)
    if typeCal in calendarTypes:
        targetClass = calendarTypes[typeCal]
        return targetClass(cfg)
    else:
        return CalendarBase(cfg)
