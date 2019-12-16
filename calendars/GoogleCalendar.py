# Calendar from google

import pickle
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import CalendarBase
from config import MsgTerm

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# @see: https://developers.google.com/calendar/quickstart/python#notes

# sync with google calendar
class GoogleCalendar(CalendarBase):
    
    # Get credentials
    def getCredentials(self):
        # File paths
        credentialsFile = self.cfg.configFolder / self.cfg.get('calendar.google', 'credentials', 'credentials.json')
        tokenFile = self.cfg.configFolder / 'token.pickle'
        MsgTerm.debug('Credentials file: %s' % credentialsFile)
        MsgTerm.debug('Token file: %s' % tokenFile)

        self.creds = None
        if tokenFile.exists():
            MsgTerm.debug('Load the token file')
            with tokenFile.open('rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                creds.refresh(Request())
            else:
                if credentialsFile.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(str(credentialsFile), SCOPES)
                    self.creds = flow.run_local_server(port=0)
                else:
                    MsgTerm.fatal('The credentials file not exists: %s' % credentialsFile)
                    return False

            # Save the credentials
            with tokenFile.open('wb') as token:
                pickle.dump(self.creds, token)


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
