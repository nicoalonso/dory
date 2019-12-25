#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock

from msgterm import MsgTerm
from configurize import Configurize


class TestConfigurize(TestCase):
    '''
    Configurize Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.cfg = Configurize('test')

    def test_init(self):
        self.assertEqual('test', self.cfg.project)
        self.assertEqual('config.json', self.cfg.filename)
        self.assertEqual(None, self.cfg.configFolder)
        self.assertEqual({}, self.cfg.config)

    def test_getHomeFilePath(self):
        # [ Given ]
        pass
        # [ When ]
        # path = self.cfg.getHomeFilePath()

        # [ Then ]


    def test_get_value(self):
        # [ Given ]
        MsgTerm.fatal = Mock()
        self.cfg.config = {
            'section': {
                'subsection': {
                    'key1': 'value1',
                    'key2': 'value2'
                }
            }
        }

        # [ When ]
        value = self.cfg.get('section.subsection.key1')

        # [ Then ]
        self.assertEqual('value1', value)
        self.assertFalse(MsgTerm.fatal.called)

        # [ When ]
        value = self.cfg.get('section.subsection')

        # [ Then ]
        self.assertEqual({'key1': 'value1', 'key2': 'value2'}, value)
        self.assertFalse(MsgTerm.fatal.called)

        # [ When ]
        value = self.cfg.get('section.subsection.dummy', 1111)

        # [ Then ]
        self.assertEqual(1111, value)
        self.assertFalse(MsgTerm.fatal.called)

        # [ When ]
        value = self.cfg.get('not.exists', False)

        # [ Then ]
        self.assertEqual(False, value)
        self.assertTrue(MsgTerm.fatal.called)
        MsgTerm.fatal.assert_called_with('[Config] section not exists not.exists')


    def test_set_value(self):
        # [ Given ]
        self.cfg.config = {
            'section': {}
        }

        # [ When ]
        self.cfg.set('section.test.name', 1234)
        self.cfg.set('dummy.key', True)
        self.cfg.set(['list', 'key', 'name'], 'test')

        # [ Then ]
        self.assertEqual(1234, self.cfg.config['section']['test']['name'])
        self.assertEqual(True, self.cfg.config['dummy']['key'])
        self.assertEqual('test', self.cfg.config['list']['key']['name'])


    def test_get_type_value(self):
        # [ Given ]
        self.cfg.config = {
            'key': {
                'type': {
                    'bool': 1,
                    'int': '123',
                    'float': '123.45',
                    'str': 999,
                    'list': (1,2,3)
                }
            }
        }

        # [ When ]
        v_bool_1 = self.cfg.bool('key.type.bool')
        v_bool_2 = self.cfg.bool('key.type.bool2')
        v_int_1 = self.cfg.int('key.type.int')
        v_int_2 = self.cfg.int('key.type.int2')
        v_float_1 = self.cfg.float('key.type.float')
        v_float_2 = self.cfg.float('key.type.float2')
        v_str_1 = self.cfg.str('key.type.str')
        v_str_2 = self.cfg.str('key.type.str2')
        v_list_1 = self.cfg.list('key.type.list')
        v_list_2 = self.cfg.list('key.type.list2')

        # [ Then ]
        self.assertTrue(v_bool_1)
        self.assertFalse(v_bool_2)
        self.assertEqual(123, v_int_1)
        self.assertEqual(0, v_int_2)
        self.assertEqual(123.45, v_float_1)
        self.assertEqual(0.0, v_float_2)
        self.assertEqual('999', v_str_1)
        self.assertEqual('', v_str_2)
        self.assertEqual([1,2,3], v_list_1)
        self.assertEqual([], v_list_2)





if __name__ == '__main__':
    unittest.main()
