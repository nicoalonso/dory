# Class for parser html form

from html.parser import HTMLParser

# Parser Form
# @see https://docs.python.org/3/library/html.parser.html
# 
class FormHtmlParser(HTMLParser):
    # Form inputs
    INPUTS = ['input', 'select', 'textarea']

    # Constructor
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_form = False
        self.current_form = ''
        self.forms = {}

    # Get Form
    def getForm(self, name):
        if name in self.forms:
            return self.forms[name]
        return None

    # new form
    def addForm(self, attrs):
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

    # Add inputs to form
    def addInput(self, attrs):
        field = { name: value for (name, value) in attrs }
        
        if 'name' in field:
            self.forms[self.current_form]['inputs'][field['name']] = field

    # Handlers
    def handle_starttag(self, tag, attrs):
        if self.in_form and tag in self.INPUTS:
            self.addInput(attrs)
        elif tag == 'form':
            self.in_form = True
            self.addForm(attrs)

    def handle_endtag(self, tag):
        if self.in_form and tag=='form':
            self.in_form = False
            self.current_form = ''

    def handle_startendtag(self, tag, attrs):
        if self.in_form and tag in self.INPUTS:
            self.addInput(attrs)
