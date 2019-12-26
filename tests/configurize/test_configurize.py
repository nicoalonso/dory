#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from pathlib import Path

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


    @patch.object(MsgTerm, 'debug')
    @patch.object(Path, 'home')
    def test_getHomeFilePath(self, _folder, _msgDebug):
        # [ When ]
        self.cfg.getHomeFilePath()

        # [ Then ]
        self.assertFalse( _msgDebug.called )


    @patch.object(MsgTerm, 'debug')
    @patch('json.load', return_value={'test': True})
    def test_load_ok(self, _jsonLoad, _msgDebug):
        # [ Given ]
        self.cfg.getHomeFilePath = Mock()
        _filePath = create_autospec(Path)
        filePathCfg = {
            'exists.return_value': True,
            'is_file.return_value': True,
            '__str__': Mock(return_value='/tmp/test')
        }
        _filePath.configure_mock( **filePathCfg )
        self.cfg.filepath = _filePath

        # [ When ]
        res = self.cfg.load()

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( self.cfg.getHomeFilePath.called )
        self.assertTrue( _msgDebug.called )
        _msgDebug.assert_called_with('[Config] load config: /tmp/test')

        self.assertTrue( self.cfg.filepath.exists.called )
        self.assertTrue( self.cfg.filepath.is_file.called )
        self.assertTrue( _jsonLoad.called )
        self.assertEqual({'test': True}, self.cfg.config)


    @patch.object(MsgTerm, 'fatal')
    @patch.object(MsgTerm, 'warning')
    @patch.object(MsgTerm, 'debug')
    @patch('json.load', return_value={'test': False})
    def test_load_not_exists(self, _jsonLoad, _msgDebug, _msgWarning, _msgFatal):
        # [ Given ]
        self.cfg.getHomeFilePath = Mock()
        _filePath = create_autospec(Path)
        filePathCfg = {
            'exists.return_value': False,
            'is_file.return_value': False,
            '__str__': Mock(return_value='/tmp/test')
        }
        _filePath.configure_mock( **filePathCfg )
        self.cfg.filepath = _filePath

        # [ When ]
        res = self.cfg.load()

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( self.cfg.getHomeFilePath.called )
        self.assertTrue( _msgWarning.called )
        _msgWarning.assert_called_with('[Config] Configuration file not found: config.json')
        self.assertTrue( _msgDebug.called )
        _msgDebug.assert_called_with('[Config] load local configuration: config.json')

        self.assertTrue( self.cfg.filepath.exists.called )
        self.assertFalse( self.cfg.filepath.is_file.called )
        self.assertTrue( _jsonLoad.called )
        self.assertEqual({'test': False}, self.cfg.config)


    @patch('json.dump')
    def test_save_ok(self, _jsonDump):
        # [ Given ]
        def mockGetHome():
            self.cfg.filepath = Path('/tmp/test')

        self.cfg.getHomeFilePath = Mock(side_effect=mockGetHome)

        # [ When ]
        self.cfg.save()

        # [ Then ]
        self.assertTrue( self.cfg.getHomeFilePath.called )
        self.assertTrue( _jsonDump.called )


    @patch('msgterm.MsgTerm.fatal')
    def test_get_value(self, _MsgFatal):
        # [ Given ]
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
        self.assertFalse(_MsgFatal.called)

        # [ When ]
        value = self.cfg.get('section.subsection')

        # [ Then ]
        self.assertEqual({'key1': 'value1', 'key2': 'value2'}, value)
        self.assertFalse(_MsgFatal.called)

        # [ When ]
        value = self.cfg.get('section.subsection.dummy', 1111)

        # [ Then ]
        self.assertEqual(1111, value)
        self.assertFalse(_MsgFatal.called)

        # [ When ]
        value = self.cfg.get('not.exists', False)

        # [ Then ]
        self.assertEqual(False, value)
        self.assertTrue(_MsgFatal.called)
        _MsgFatal.assert_called_with('[Config] section not exists not.exists')


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


    @patch('msgterm.MsgTerm.fatal')
    def test_remove_value(self, _msgFatal):
        # [ Given ]
        self.cfg.config = {
            'section': {
                'name': 123
            }
        }

        # [ When ]
        res = self.cfg.remove('section.name')

        # [ Then ]
        self.assertTrue( res )
        self.assertEqual({'section': {}}, self.cfg.config)
        self.assertFalse(_msgFatal.called)

        # [ When ] + name not exists
        res = self.cfg.remove('section.name')

        # [ Then ]
        self.assertFalse( res )
        self.assertEqual({'section': {}}, self.cfg.config)
        self.assertTrue(_msgFatal.called)
        _msgFatal.assert_called_with('[Config] parameter not exists { section.name }')

        # [ When ] + section not exists
        res = self.cfg.remove('dummy.name')

        # [ Then ]
        self.assertFalse( res )
        self.assertEqual({'section': {}}, self.cfg.config)
        self.assertTrue(2, _msgFatal.call_count)
        _msgFatal.assert_called_with('[Config] parameter not exists { dummy.name }')


    @patch('msgterm.MsgTerm.jsonPrint')
    def test_display(self, _msgPrint):
        # [ When ]
        self.cfg.display()

        # [ Then ]
        self.assertTrue(_msgPrint.called)


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


    @patch('msgterm.MsgTerm.help')
    def test_command_help(self, _msgHelp):
        # [ When ]
        res = self.cfg.command('help')

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( _msgHelp.called )


    @patch('msgterm.MsgTerm.info')
    def test_command_list(self, _msgInfo):
        # [ Given ]
        self.cfg.display = Mock()

        # [ When ]
        res = self.cfg.command('list')

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( _msgInfo.called )
        _msgInfo.assert_called_with('Show config file:', par=True)
        self.assertTrue( self.cfg.display.called )


    @patch('msgterm.MsgTerm.error')
    @patch('msgterm.MsgTerm.success')
    @patch('msgterm.MsgTerm.debug')
    def test_command_set_ok(self, _msgDebug, _msgSuccess, _msgError):
        # [ Given ]
        self.cfg.set = Mock()
        self.cfg.save = Mock()
        self.cfg.display = Mock()

        # [ When ]
        res = self.cfg.command('section.name=value')

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( self.cfg.set.called )
        self.assertTrue( self.cfg.save.called )
        self.assertTrue( self.cfg.display.called )
        self.assertTrue( _msgDebug.called )
        self.assertTrue( _msgSuccess.called )
        self.assertEqual(2, _msgSuccess.call_count)
        self.assertFalse( _msgError.called )
        _msgDebug.assert_called_with('Update parameter [ section.name ] with value "value"')


    @patch('msgterm.MsgTerm.error')
    @patch('msgterm.MsgTerm.success')
    @patch('msgterm.MsgTerm.debug')
    def test_command_set_error(self, _msgDebug, _msgSuccess, _msgError):
        # [ Given ]
        self.cfg.set = Mock()
        self.cfg.save = Mock()
        self.cfg.display = Mock()

        # [ When ]
        res = self.cfg.command('section.name=value=test')

        # [ Then ]
        self.assertFalse( res )
        self.assertFalse( self.cfg.set.called )
        self.assertFalse( self.cfg.save.called )
        self.assertFalse( self.cfg.display.called )
        self.assertFalse( _msgDebug.called )
        self.assertFalse( _msgSuccess.called )
        self.assertTrue( _msgError.called )


    @patch('msgterm.MsgTerm.error')
    @patch('msgterm.MsgTerm.success')
    @patch('msgterm.MsgTerm.debug')
    def test_command_remove(self, _msgDebug, _msgSuccess, _msgError):
        # [ Given ]
        self.cfg.remove = Mock(return_value=True)
        self.cfg.save = Mock()
        self.cfg.display = Mock()

        # [ When ]
        res = self.cfg.command('section.name-')

        # [ Then ]
        self.assertTrue( res )
        self.assertTrue( self.cfg.remove.called )
        self.assertTrue( self.cfg.save.called )
        self.assertTrue( self.cfg.display.called )
        self.assertTrue( _msgDebug.called )
        self.assertTrue( _msgSuccess.called )
        self.assertFalse( _msgError.called )

        # [ Given ]
        self.cfg.remove.return_value = False

        # [ When ]
        res = self.cfg.command('section.name-')

        # [ Then ]
        self.assertFalse( res )


    @patch('msgterm.MsgTerm.help')
    @patch('msgterm.MsgTerm.alert')
    def test_command_unknown(self, _msgHelp, _msgAlert):
        # [ When ]
        res = self.cfg.command('dummy')

        # [ Then ]
        self.assertFalse( res )
        self.assertTrue(_msgHelp.called)
        self.assertTrue(_msgAlert.called)


if __name__ == '__main__':
    unittest.main()
