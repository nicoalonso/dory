# Calendar from google

import pickle
from datetime import datetime, date
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .CalendarBase import CalendarBase
from .GoogleCalendarEvent import GoogleCalendarEvent
from config import MsgTerm

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# @see: https://developers.google.com/calendar/quickstart/python#notes

# sync with google calendar
class GoogleCalendar(CalendarBase):
    
    # Constructor
    def __init__(self, config):
        CalendarBase.__init__(self, config)
        self.creds = None

    # Get credentials
    def getCredentials(self):
        if self.creds:
            return self.creds

        # Search token file
        tokenFile = self.cfg.configFolder / 'token.pickle'
        MsgTerm.debug('Token file: %s' % tokenFile)

        # Read credentials for token
        if tokenFile.exists():
            MsgTerm.debug('Load the token file')
            with tokenFile.open('rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                appFolder = Path(__file__).parents[1]
                MsgTerm.debug('Application folder %s' % appFolder)
                credentialsFile = appFolder / 'credentials.json'
                MsgTerm.debug('Credentials file: %s' % credentialsFile)

                if credentialsFile.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(str(credentialsFile), SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    MsgTerm.fatal('The credentials file not exists: %s' % credentialsFile)
                    return False

            # Save the credentials
            with tokenFile.open('wb') as token:
                pickle.dump(self.creds, token)

        return self.creds

    # Check connection to Google Calendar
    def check(self):
        # Credentials
        self.getCredentials()

        service = build('calendar', 'v3', credentials=self.creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        MsgTerm.info('Getting the upcoming 10 events', hr=True, nl=True)
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            MsgTerm.warning('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            MsgTerm.info('%s %s' % (start, event['summary']))

        return True

    # Get Events from Google Calendar
    def getEvents(self):
        self.eventName = self.cfg.get('calendar.google', 'event_name')
        if not self.eventName:
            MsgTerm.error('[Calendar] Error: calendar.google.event_name is not defined')
            info = [
                'Check the configuration',
                'for more information execute the command:',
                'dory --config help'
            ]
            MsgTerm.help(info, par=True)
            return None

        # Get Credentials
        self.getCredentials()

        # service
        service = build('calendar', 'v3', credentials=self.creds)
        
        # Search events
        MsgTerm.info(["Search events: [ %s ]" % self.eventName, 'Limit to first 10 events'], hr=True, nl=True)
        today = datetime.combine(date.today(), datetime.min.time()).isoformat() + 'Z'
        MsgTerm.debug("Search for %s" % today)
        events_result = service.events().list(
            q            = self.eventName,
            calendarId   = 'primary',
            timeMin      = today,
            maxResults   = 10,
            singleEvents = True,
            orderBy      = 'startTime'
        ).execute()

        listEvents = events_result.get('items', [])
        MsgTerm.debug('Events found %d' % len(listEvents))
        events = []
        for calEvent in listEvents:
            event = GoogleCalendarEvent(calEvent)
            if event.valid:
                events.append( event )
            else:
                MsgTerm.debug('Event not valid: %s', event['summary'])
        MsgTerm.debug('Valid events: %d' % len(events))

        return events

    # Return the list of events
    # 
    # @param  debug  - show the first event for debug
    # 
    def getListEvents(self, debug=False):
        events = self.getEvents()

        if not events:
            MsgTerm.alert('No found events for name: %s' % self.eventName)
        elif debug:
            events[0].debug()
        else:
            for event in events:
                event.print(True)

        return True

    # Return today's event
    def xgetTodayEvent(self):
        events = self.getEvents()

        if not events:
            MsgTerm.alert('No found events for name: %s' % self.eventName)
        else:
            for event in events:
                if event.isToday():
                    return event

        return None
