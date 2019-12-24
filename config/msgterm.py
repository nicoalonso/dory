#!/usr/bin/python3

import json
from termcolor import colored, cprint


class MsgTerm:
    '''Show messages on the Terminal
    
    It is used for show information to the user
    Depends on termcolor library
    
    Constants:
        DEBUG   {0}: display debug messages
        INFO    {1}: display information messages
        TEXT    {2}: display test messages
        SUCCESS {3}: display success messages
        WARNING {4}: display warning messages
        ALERT   {5}: display alert messages
        ERROR   {6}: display error messages
        FATAL   {7}: display fatal error messages
        HELP    {8}: display help messages
        COLORS  {list}: List of colors used for show the different messages
        LABELS  {list}: List of labes to show the differentent messages

    Static Attributes:
        verbose_level {number}: verbose level, hide messages that the level is lower than message value
                                (default: {1}) - hide debug messages

    Args:
        msg {str|list}: Message to show
        kwargs {dict}: List of options, each option in the dict must exist as an attribute in the class

    Attributes:
        type {number}: type of message, must be one of constants defined on the class, example: INFO, (default: {TEXT})
        label {string|None}: label to show before the message in the box, example: + >> [+], (default: {None})
        bold {bool}: bold style, (default: {False})
        reverse (bool): reverse style, (default: {False})
        hr (bool): like as <HR> tag in html, print '---', (default: {False})
        paragraph (bool): like as <P> tag in html, (defaul: {False})
        nl (bool): New line, print new line after the message, (default: {False})
        msgs (list): List of messages to display, each list item print in a single line
    '''

    # Constants
    DEBUG    = 0
    INFO     = 1
    TEXT     = 2
    SUCCESS  = 3
    WARNING  = 4
    ALERT    = 5
    ERROR    = 6
    FATAL    = 7
    HELP     = 8
    # Colors and Labels
    COLORS   = ['grey', 'blue', 'white', 'green', 'yellow', 'yellow', 'red', 'magenta', 'cyan']
    LABELS   = ['d', 'i', ' ', '+', 'w', '*', '!', '!!', '?']

    # Verbose level
    verbose_level = 1

    def __init__(self, msg, **kwargs):
        self.type = self.TEXT
        self.label = None
        self.bold = False
        self.reverse = False
        self.hr = False
        self.paragraph = False
        self.nl = False
        self.msgs = []

        if isinstance(msg, list) or isinstance(msg, tuple):
            self.msgs = msg
        elif isinstance(msg, str):
            self.msgs.append( msg )
        else:
            raise ValueError('msg')

        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
            else:  # alias
                if key == 'par' or key == 'p':
                    self.paragraph = kwargs[key]
                elif key == 'lbl':
                    self.label = kwargs['lbl']

        # Force that the type is of the allow types
        if self.type < self.DEBUG:
            self.type = self.DEBUG
        elif self.type > self.HELP:
            self.type = self.HELP


    def show(self):
        '''Show message
        
        Print message on the terminal with the styles was defined
        '''
        if self.type < self.verbose_level:
            return

        color = self.COLORS[ self.type ]
        attrs = []
        if self.bold:
            attrs.append('bold')
        if self.reverse:
            attrs.append('reverse')

        # Print line to separate text
        if self.hr:
            cprint('\n -- \n', color, attrs=['bold'])
        elif self.paragraph:
            print('')

        # Message
        box = ''
        if self.label:
            box = colored('[%s]', color) % self.label

        for item in self.msgs:
            text = colored(item, color, attrs=attrs)
            if box:
                print(box, text)
            else:
                print(text)

        if self.paragraph or self.nl:
            print('')


    def __str__(self):
        '''Transfrom to string
        
        Returns:
            str
        '''

        return ', '.join(self.msgs)

    # Static methods

    @staticmethod
    def verbosity(level):
        '''Set verbosity level
        
        Arguments:
            level {number}: verbosity level
        '''

        MsgTerm.verbose_level = level


    @staticmethod
    def message(msg, **kwargs):
        '''Show generic message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def text(msg, **kwargs):
        '''Show text message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.TEXT
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.TEXT]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def debug(msg, **kwargs):
        '''Show debug message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.DEBUG
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.DEBUG]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def info(msg, **kwargs):
        '''Show info message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.INFO
        if not 'bold' in kwargs:
            kwargs['bold'] = True
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.INFO]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def success(msg, **kwargs):
        '''Show success message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.SUCCESS
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.SUCCESS]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def warning(msg, **kwargs):
        '''Show warning message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.WARNING
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.WARNING]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def alert(msg, **kwargs):
        '''Show alert message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['bold'] = True
        kwargs['type'] = MsgTerm.ALERT
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.ALERT]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def error(msg, **kwargs):
        '''Show error message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.ERROR
        kwargs['bold'] = True
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.ERROR]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def fatal(msg, **kwargs):
        '''Show fatal error message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.FATAL
        kwargs['bold'] = True
        kwargs['sep'] = True
        kwargs['hr'] = True
        kwargs['paragraph'] = True
        kwargs['reverse'] = True

        if isinstance(msg, tuple):
            msg = list(msg)
        if isinstance(msg, list):
            msg.insert(0, '[ Fatal Error ]')
        else:
            msg = ['[ Fatal Error ]', msg]

        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.FATAL]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def help(msg, **kwargs):
        '''Show help message
        
        Arguments:
            msg {string|list}: Message or list of messages
            **kwargs {dict}: List of message options
        '''

        kwargs['type'] = MsgTerm.HELP
        kwargs['bold'] = True

        title = '[ Help ]'
        if 'section' in kwargs:
            title = '[ Help :: %s ]' % kwargs['section']

        if isinstance(msg, tuple):
            msg = list(msg)
        if isinstance(msg, list):
            msg.insert(0, title)
            msg.insert(1, '')
        else:
            msg = [title, '', msg]

        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.HELP]

        MsgTerm(msg, **kwargs).show()


    @staticmethod
    def jsonPrint(obj):
        '''Helper for print JSON objects to terminal
        
        Arguments:
            obj (dict): object to print
        '''

        cprint(json.dumps(obj, indent=4, sort_keys=True), 'cyan')
        print('')


if __name__ == '__main__':
    # Test messages and colors
    MsgTerm.verbosity(MsgTerm.DEBUG)  # Set level of verbosity
    MsgTerm.message('Text messages')
    MsgTerm.debug('debug')
    MsgTerm.info('info')
    MsgTerm.text('text')
    MsgTerm.success('success')
    MsgTerm.warning('warning')
    MsgTerm.alert('alert')
    MsgTerm.error('error')
    MsgTerm.fatal('fatal')
    MsgTerm.help('help')

    # Print a list of messages in paragraph style
    MsgTerm.message('Paragraph Style', label='#', bold=True, hr=True, type=MsgTerm.SUCCESS)
    msgs = ['This is a message', 'that to show in multiple lines', 'like as a paragraph style']
    MsgTerm.message(msgs, paragraph=True, label=' ', bold=True, type=MsgTerm.INFO)
