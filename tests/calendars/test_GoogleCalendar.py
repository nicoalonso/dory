#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from msgterm import MsgTerm
from configurize import Configurize
from calendars import GoogleCalendar


class TestGoogleCalendar(TestCase):
    '''Test Google Calendar API
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.cfg = Configurize('test')
        self.cal = GoogleCalendar(self.cfg)


    @patch('googleapiclient.discovery.build')
    def test_check(self, _build):
        # [ Given ]
        self.cal.getCredentials = Mock()
        service = Mock()
        _build.return_value = service



        # [ When ]  TODO: ...
        # self.cal.check()

        # [ Then ]

