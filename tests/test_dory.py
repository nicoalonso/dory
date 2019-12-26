#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, patch

from dory import Dory
from msgterm import MsgTerm


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



if __name__ == '__main__':
    unittest.main()
