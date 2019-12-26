#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from io import StringIO

from msgterm import MsgTerm


class TestMsgTerm(TestCase):
    '''
    MsgTerm Test
    
    Extends:
        TestCase
    '''

    @patch('sys.stdout', new_callable=StringIO)
    def test_message(self, _stdout):
        # [ When ]
        MsgTerm.message('test')

        # [ Then ]
        self.assertIn('test', _stdout.getvalue())

        # [ When ]
        MsgTerm.message(['test1', 'test2'], bold=True, par=True, lbl='+')

        # [ Then ]
        self.assertIn('test1', _stdout.getvalue())
        self.assertIn('test2', _stdout.getvalue())
        self.assertIn('[+]', _stdout.getvalue())

        # [ When ]
        MsgTerm.message('reverse', reverse=True, type=11, hr=True)

        # [ Then ]
        self.assertIn('reverse', _stdout.getvalue())

        # [ Given ]
        MsgTerm.verbosity(2)

        # [ When ]
        MsgTerm.message('debug', type=-1)

        # [ Then ]
        self.assertNotIn('debug', _stdout.getvalue())

        # [ Given ]
        msg = MsgTerm('test9')

        # [ When ]
        val = '%s' % msg

        # [ Then ]
        self.assertEqual('test9', val)

        # [ When]
        with self.assertRaises(ValueError):
            MsgTerm.message(111)


    @patch('sys.stdout', new_callable=StringIO)
    def test_msg_defined(self, _stdout):
        # [ Given ]
        MsgTerm.verbosity(0)

        # [ When ]
        MsgTerm.text('text')
        MsgTerm.debug('debug')
        MsgTerm.info('info')
        MsgTerm.success('success')
        MsgTerm.warning('warning')
        MsgTerm.alert('alert')
        MsgTerm.error('error')
        MsgTerm.fatal('fatal')
        MsgTerm.help('help')

        # [ Then ]
        self.assertIn('text', _stdout.getvalue())
        self.assertIn('debug', _stdout.getvalue())
        self.assertIn('info', _stdout.getvalue())
        self.assertIn('success', _stdout.getvalue())
        self.assertIn('warning', _stdout.getvalue())
        self.assertIn('alert', _stdout.getvalue())
        self.assertIn('error', _stdout.getvalue())
        self.assertIn('fatal', _stdout.getvalue())
        self.assertIn('help', _stdout.getvalue())

        # [ When ]
        MsgTerm.fatal( ('fatal2', 'fatal3') )
        MsgTerm.help( ('help1', 'help2'), section='Config' )

        # [ Then ]
        self.assertIn('fatal2', _stdout.getvalue())
        self.assertIn('help1', _stdout.getvalue())
        self.assertIn('Help :: Config', _stdout.getvalue())


    @patch('sys.stdout', new_callable=StringIO)
    def test_jsonPrint(self, _stdout):
        # [ When ]
        MsgTerm.jsonPrint({'test': 'dummy'})

        # [ Then ]
        self.assertIn('dummy', _stdout.getvalue())




