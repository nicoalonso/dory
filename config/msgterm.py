#!/usr/bin/python3
# Show messages on the terminal
# 
# Options:
#   type: TEXT | INFO
#   label: +
#   bold: False
#   reverse: False
#   hr: False
#   paragraph: False
#   nl: False
#   

from termcolor import colored, cprint

# Message in Terminal
class MsgTerm:

    # Type messages constants
    DEBUG    = 0
    INFO     = 1
    TEXT     = 2
    SUCCESS  = 3
    WARNING  = 4
    ALERT    = 5
    ERROR    = 6
    FATAL    = 7
    # Message colors
    COLORS   = ['grey', 'blue', 'white', 'green', 'yellow', 'cyan', 'red', 'magenta']
    LABELS   = ['d', 'i', ' ', '+', 'w', '*', '!', '!!']

    # Verbose level, default: hide debug messages
    verbose_level = 1

    # Constructor
    def __init__(self, msg, **kwargs):
        self.type = self.TEXT
        self.label = None
        self.bold = False
        self.reverse = False
        self.hr = False
        self.paragraph = False
        self.nl = False  # new line
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
            else:
                if key == 'par':
                    self.paragraph = kwargs['par']
                elif key == 'p':
                    self.paragraph = kwargs['p']
                elif key == 'lbl':
                    self.label = kwargs['lbl']

        if self.type < self.DEBUG:
            self.type = self.DEBUG
        elif self.type > self.FATAL:
            self.type = self.FATAL

    # Print message on the terminal
    def show(self):
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

    # Transform to string
    def __str__(self):
        return ', '.join(self.msgs)

    # Static methods
    
    @staticmethod
    def verbosity(level):
        MsgTerm.verbose_level = level

    # Generic
    @staticmethod
    def message(msg, **kwargs):
        MsgTerm(msg, **kwargs).show()

    # show text
    @staticmethod
    def text(msg, **kwargs):
        kwargs['type'] = MsgTerm.TEXT
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.TEXT]

        MsgTerm(msg, **kwargs).show()

    # Show debug
    @staticmethod
    def debug(msg, **kwargs):
        kwargs['type'] = MsgTerm.DEBUG
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.DEBUG]

        MsgTerm(msg, **kwargs).show()

    # show information
    @staticmethod
    def info(msg, **kwargs):
        kwargs['type'] = MsgTerm.INFO
        kwargs['bold'] = True
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.INFO]

        MsgTerm(msg, **kwargs).show()

    # show success
    @staticmethod
    def success(msg, **kwargs):
        kwargs['type'] = MsgTerm.SUCCESS
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.SUCCESS]

        MsgTerm(msg, **kwargs).show()

    # show warning
    @staticmethod
    def warning(msg, **kwargs):
        kwargs['type'] = MsgTerm.WARNING
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.WARNING]

        MsgTerm(msg, **kwargs).show()

    # show alert
    @staticmethod
    def alert(msg, **kwargs):
        kwargs['type'] = MsgTerm.ALERT
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.ALERT]

        MsgTerm(msg, **kwargs).show()

    # show error
    @staticmethod
    def error(msg, **kwargs):
        kwargs['type'] = MsgTerm.ERROR
        kwargs['bold'] = True
        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.ERROR]

        MsgTerm(msg, **kwargs).show()

    # show Fatal Error
    @staticmethod
    def fatal(msg, **kwargs):
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


# Text messages and colors
if __name__ == '__main__':
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

    # Printa a list of messages in paragraph style
    MsgTerm.message('Paragraph Style', label='#', bold=True, hr=True, type=MsgTerm.SUCCESS)
    msgs = ['This is a message', 'that to show in multiple lines', 'like as a paragraph style']
    MsgTerm.message(msgs, paragraph=True, label=' ', bold=True, type=MsgTerm.INFO)
