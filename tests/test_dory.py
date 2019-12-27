#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, patch

from argparse import ArgumentParser

from dory import Dory
from msgterm import MsgTerm
from configurize import Configurize
from calendars import CalendarBase


class TestDory(TestCase):
    '''
    Dory Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.dory = Dory()


    @patch.object(MsgTerm, 'success')
    def test_wellcome(self, _msgSuccess):
        # [ When ]
        self.dory.wellcome()

        # [ Then ]
        self.assertTrue( _msgSuccess.called )


    @patch.object(MsgTerm, 'info')
    def test_bye(self, _msgInfo):
        # [ When ]
        self.dory.bye()

        # [ Then ]
        self.assertTrue( _msgInfo.called )


    @patch.object(ArgumentParser, 'parse_args', return_value={'test': True})
    def test_arguments(self, _argParser):
        # [ When ]
        self.dory.arguments()

        # [ Then ]
        self.assertTrue( _argParser.called )
        self.assertEqual({'test': True}, self.dory.args)


    @patch.object(Configurize, 'load', return_value=True)
    def test_run_ok(self, _cfgLoad):
        # [ Given ]
        self.dory.wellcome = Mock()
        self.dory.arguments = Mock()
        self.dory.bye = Mock()
        self.dory.args = Mock()
        self.dory.args.verbose = True
        self.dory.args.config = None
        self.dory.args.calendar = None
        self.dory.args.register = None

        # [ When ]
        self.dory.run()

        # [ Then ]
        self.assertTrue( self.dory.wellcome.called )
        self.assertTrue( self.dory.arguments.called )
        self.assertTrue( _cfgLoad.called )
        self.assertTrue( self.dory.bye.called )


    @patch.object(Configurize, 'command', return_value=True)
    @patch.object(Configurize, 'load', return_value=True)
    def test_run_config(self, _cfgLoad, _cfgCommand):
        # [ Given ]
        self.dory.wellcome = Mock()
        self.dory.arguments = Mock()
        self.dory.bye = Mock()
        self.dory.args = Mock()
        self.dory.args.verbose = True
        self.dory.args.config = 'help'
        self.dory.args.calendar = None
        self.dory.args.register = None

        # [ When ]
        self.dory.run()

        # [ Then ]
        self.assertTrue( self.dory.wellcome.called )
        self.assertTrue( self.dory.arguments.called )
        self.assertTrue( _cfgLoad.called )
        self.assertTrue( _cfgCommand.called )
        self.assertTrue( self.dory.bye.called )


    @patch.object(CalendarBase, 'command', return_value=True)
    @patch.object(Configurize, 'load', return_value=True)
    def test_run_config(self, _cfgLoad, _calCommand):
        # [ Given ]
        self.dory.wellcome = Mock()
        self.dory.arguments = Mock()
        self.dory.bye = Mock()
        self.dory.args = Mock()
        self.dory.args.verbose = True
        self.dory.args.config = None
        self.dory.args.calendar = 'Help'
        self.dory.args.register = None
        # TODO: ver esto
        self.dory.cfg.set('calendar.type', 'base')

        # [ When ]
        self.dory.run()

        # [ Then ]
        self.assertTrue( self.dory.wellcome.called )
        self.assertTrue( self.dory.arguments.called )
        self.assertTrue( _cfgLoad.called )
        self.assertTrue( _calCommand.called )
        self.assertTrue( self.dory.bye.called )


if __name__ == '__main__':
    unittest.main()
