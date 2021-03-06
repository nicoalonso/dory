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


    @patch.object(MsgTerm, 'alert')
    @patch.object(MsgTerm, 'help')
    def test_command(self, _msgHelp, _msgAlert):
        # [ Given ]
        self.cal.check = Mock()
        self.cal.list = Mock()

        # [ When ]
        self.cal.command('check')
        self.cal.command('list')
        self.cal.command('debug')
        self.cal.command('help')
        self.cal.command('dummy')

        # [ Then ]
        self.assertTrue( self.cal.check.called )
        self.assertTrue( self.cal.list.called )
        self.assertEqual( 2, self.cal.list.call_count )
        self.assertTrue( MsgTerm.help.called )
        self.assertEqual( 2, MsgTerm.help.call_count )
        self.assertTrue( MsgTerm.alert.called )
