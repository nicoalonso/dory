#!/usr/bin/python3

from html.parser import HTMLParser


class FormHtmlParser(HTMLParser):
    '''Form parser
    
    Parse html to get the forms
    @doc https://docs.python.org/3/library/html.parser.html
    
    Extends:
        HTMLParser
    
    Constants:
        INPUTS {list}: form tags to find

    Attributes:
        in_form {bool}: flag to know if we are in a form
        current_form {string}: name of the current form
        forms {dict}: store forms and their inputs
    '''
    INPUTS = ['input', 'select', 'textarea']

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_form = False
        self.current_form = ''
        self.forms = {}


    def getForm(self, name):
        '''Get form by name
        
        Arguments:
            name {string}: form name
        
        Returns:
            dict|None
        '''
        if name in self.forms:
            return self.forms[name]
        return None


    def _add_form(self, attrs):
        '''add form
        
        private method, add form to dictionary
        
        Arguments:
            attrs {dict}: form attributes
        '''
        frm = { name: value for (name, value) in attrs }
        frm['inputs'] = {}

        name = None
        if 'name' in frm:
            name = frm['name']
        elif 'action' in frm:
            parts = frm['action'].split('/')
            name = parts.pop()

        if not name:
            name = 'default'

        self.forms[name] = frm
        self.current_form = name


    def _add_input(self, attrs):
        '''Add input to form

        private method
        
        Arguments:
            attrs {dict}: input attributes
        '''
        field = { name: value for (name, value) in attrs }
        
        if 'name' in field:
            self.forms[self.current_form]['inputs'][field['name']] = field

    # Handlers inherit from HTMLParser
    def handle_starttag(self, tag, attrs):
        if self.in_form and tag in self.INPUTS:
            self._add_input(attrs)
        elif tag == 'form':
            self.in_form = True
            self._add_form(attrs)

    def handle_endtag(self, tag):
        if self.in_form and tag=='form':
            self.in_form = False
            self.current_form = ''

    def handle_startendtag(self, tag, attrs):
        if self.in_form and tag in self.INPUTS:
            self._add_input(attrs)
