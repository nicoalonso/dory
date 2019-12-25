#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock

from dory import Dory
from msgterm import MsgTerm


class TestDory(unittest.TestCase):
    '''
    Dory Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.dory = Dory()

    def test_wellcome(self):
        # [ Given ]
        MsgTerm.success = Mock()

        # [ When ]
        self.dory.wellcome()

        # [ Then ]
        self.assertTrue( MsgTerm.success.called )

    def test_wellcome2(self):
        # [ Given ]
        MsgTerm.success = Mock()
        
        # [ When ]
        # self.dory.wellcome()

        # [ Then ]
        self.assertFalse( MsgTerm.success.called )



if __name__ == '__main__':
    unittest.main()
