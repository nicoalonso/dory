#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from msgterm import MsgTerm
from configurize import Configurize
from registers import RegisterBase


class TestRegisterBase(TestCase):
    '''
    Register Base Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.cfg = Configurize('test')
        self.reg = RegisterBase( self.cfg )


    @patch.object(MsgTerm, 'error')
    def test_check(self, _msgError):
        # [ When ]
        res = self.reg.check()

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue( _msgError.called )


    @patch.object(MsgTerm, 'error')
    def test_list(self, _msgError):
        # [ When ]
        res = self.reg.list()

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue( _msgError.called )


    @patch.object(MsgTerm, 'alert')
    @patch.object(MsgTerm, 'help')
    def test_command(self, _msgHelp, _msgAlert):
        # [ Given ]
        self.reg.check = Mock()
        self.reg.list = Mock()

        # [ When ]
        self.reg.command('check')
        self.reg.command('list')
        self.reg.command('help')
        self.reg.command('dummy')

        # [ Then ]
        self.assertTrue( self.reg.check.called )
        self.assertTrue( self.reg.list.called )
        self.assertTrue( MsgTerm.help.called )
        self.assertEqual( 2, MsgTerm.help.call_count )
        self.assertTrue( MsgTerm.alert.called )
