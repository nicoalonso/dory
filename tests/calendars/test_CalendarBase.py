#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from msgterm import MsgTerm
from configurize import Configurize
from calendars import CalendarBase


class TestCalendarBase(TestCase):
    '''
    Calendar Base Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.cfg = Configurize('test')
        self.cal = CalendarBase( self.cfg )


    @patch.object(MsgTerm, 'error')
    def test_check(self, _msgError):
        # [ When ]
        res = self.cal.check()

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue( _msgError.called )


    @patch.object(MsgTerm, 'error')
    def test_list(self, _msgError):
        # [ When ]
        res = self.cal.list()

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue( _msgError.called )


    @patch.object(MsgTerm, 'error')
    def test_getTodayEvent(self, _msgError):
        # [ When ]
        res = self.cal.getTodayEvent()

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue( _msgError.called )
