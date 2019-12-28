#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from datetime import date

from msgterm import MsgTerm
from calendars import GoogleCalendarEvent


class TestGoogleCalendarEvent(TestCase):
    '''Test Google Calendar Event
    
    Extends:
        TestCase
    '''

    @patch.object(MsgTerm, 'jsonPrint')
    @patch.object(MsgTerm, 'info')
    def test_event_parse(self, _msgInfo, _msgPrint):
        # [ Given ]
        today = date.today().strftime('%Y-%m-%d')
        calEvent = {
            "created": "%sT13:20:22.000Z" % today,
            "creator": {
                "displayName": "Nico Alonso",
                "email": "nicoxxxxxx@gmail.com",
                "self": True
            },
            "end": {
                "dateTime": "%sT17:00:00+01:00" % today,
                "timeZone": "Europe/Madrid"
            },
            "etag": "\"3146221445386000\"",
            "htmlLink": "",
            "iCalUID": "",
            "id": "td4t0lip05461fmekerje472ub_20200107T070000Z",
            "kind": "calendar#event",
            "location": "Vigo",
            "organizer": {
                "displayName": "Nico Alonso",
                "email": "nicoxxxxxx@gmail.com",
                "self": True
            },
            "originalStartTime": {
                "dateTime": "%sT08:00:00+01:00" % today,
                "timeZone": "Europe/Madrid"
            },
            "recurringEventId": "td4t0lip05461fmekerje472ub",
            "reminders": {
                "useDefault": True
            },
            "sequence": 1,
            "start": {
                "dateTime": "%sT08:00:00+01:00" % today,
                "timeZone": "Europe/Madrid"
            },
            "status": "confirmed",
            "summary": "Work",
            "updated": "%sT07:12:02.693Z" % today
        }

        # [ When ]
        event = GoogleCalendarEvent(calEvent)
        event.print( True )
        event.debug()

        # [ Then ]
        self.assertTrue( event.validate )
        self.assertIsNotNone( event.start )
        self.assertIsNotNone( event.end )
        self.assertIsNotNone( event.delta )
        self.assertEqual( 9, event.hours )
        self.assertEqual('Work', event.summary)
        self.assertTrue( event.isToday() )
        self.assertTrue( _msgInfo.called )
        self.assertTrue( _msgPrint.called )
