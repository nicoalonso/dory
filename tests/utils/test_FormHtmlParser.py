#!/usr/bin/python3

import unittest
from unittest import TestCase
from unittest.mock  import Mock, MagicMock, patch, create_autospec

from utils import FormHtmlParser


class TestFormHtmlParser(TestCase):
    '''From Html Parser Test
    
    Extends:
        TestCase
    '''

    def setUp(self):
        self.parser = FormHtmlParser()


    def test_parse_html(self):
        # [ Given ]
        response = """
        <html>
            <body>
                <header></header>
                <div class='row'>
                    <form action='test/login'>
                        <div class='col'>
                            <input type='hidden' value='Not' />
                            <input type='text' name='user' />
                            <input type='text' name='password' />
                            <select name='type_user'>
                                <option>Default</option>
                            </select>
                            <textarea name='obs'></textarea>
                        </div>
                    </form>
                </div>
                <div>
                    <form name='test2'>
                        <input type='hidden' name='test' />
                    </form>
                </div>
                <div>
                    <form>
                        <input type='hidden' name='dummy' />
                    </form>
                </div>
            </body>
        </html>
        """

        # [ When ]
        self.parser.feed(response)
        loginFrm = self.parser.getForm('login')
        dummyFrm = self.parser.getForm('dummy')
        test2Frm = self.parser.getForm('test2')
        defaultFrm = self.parser.getForm('default')

        # [ Then ]
        self.assertIsNotNone( loginFrm )
        self.assertIsNone( dummyFrm )
        self.assertIsNotNone( test2Frm )
        self.assertIsNotNone( defaultFrm )
        self.assertFalse( 'Not' in loginFrm['inputs'] )
        self.assertTrue( 'user' in loginFrm['inputs'] )
        self.assertTrue( 'password' in loginFrm['inputs'] )
        self.assertTrue( 'type_user' in loginFrm['inputs'] )
        self.assertTrue( 'obs' in loginFrm['inputs'] )