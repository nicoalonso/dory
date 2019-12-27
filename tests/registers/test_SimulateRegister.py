#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from msgterm import MsgTerm
from configurize import Configurize
from registers import SimulateRegister


class TestSimulateRegister(TestCase):
    '''
    Simulate Register Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.cfg = Configurize('test')
        self.reg = SimulateRegister( self.cfg )


    @patch.object(MsgTerm, 'success')
    @patch.object(MsgTerm, 'text')
    def test_check(self, _msgTest, _msgSuccess):
        # [ When ]
        res = self.reg.check()

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( _msgTest.called )
        self.assertTrue( _msgSuccess.called )

    
    @patch.object(MsgTerm, 'success')
    @patch.object(MsgTerm, 'text')
    def test_list(self, _msgTest, _msgSuccess):
        # [ When ]
        res = self.reg.list()

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( _msgTest.called )
        self.assertTrue( _msgSuccess.called )    
