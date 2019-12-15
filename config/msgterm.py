#!/usr/bin/python3
# Show messages on the terminal

from termcolor import colored

# Message in Terminal
class MsgTerm:

    # Type messages constants
    TEXT     = 0
    DEBUG    = 1
    INFO     = 2
    SUCCESS  = 3
    WARNING  = 4
    ALERT    = 5
    ERROR    = 6
    FATAL    = 7
    # Message colors
    COLORS   = ['white', 'grey', 'blue', 'green', 'yellow', 'cyan', 'red', 'magenta']
    LABELS   = [' ', '-', 'i', '+', 'w', '*', '!', '!!']

    # Constructor
    def __init__(self, msg, **kwargs):
        self.type = self.TEXT
        self.label = None
        self.separation = False
        self.bold = False
        self.reverse = False
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
                if key == 'sep':
                    self.separation = kwargs['sep']
                elif key == 'lbl':
                    self.label = kwargs['lbl']

        if self.type < self.TEXT:
            self.type = self.TEXT
        elif self.type > self.FATAL:
            self.type = self.FATAL

    # Print message on the terminal
    def show(self):
        if self.separation:
            print('')

        color = self.COLORS[ self.type ]
        attrs = []
        if self.bold:
            attrs.append('bold')
        if self.reverse:
            attrs.append('reverse')

        box = ''
        if self.label:
            box = colored('[%s]', color) % self.label

        for item in self.msgs:
            text = colored(item, color, attrs=attrs)
            if box:
                print(box, text)
            else:
                print(text)

        if self.separation:
            print('')

    # Transform to string
    def __str__(self):
        return ', '.join(self.msgs)

    # Static methods
    
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
        kwargs['reverse'] = True

        if not ('label' in kwargs or 'lbl' in kwargs):
            kwargs['label'] = MsgTerm.LABELS[MsgTerm.FATAL]

        MsgTerm(msg, **kwargs).show()


# Text messages and colors
if __name__ == '__main__':
    MsgTerm.message('Text messages')
    MsgTerm.text('text')
    MsgTerm.debug('debug')
    MsgTerm.info('info')
    MsgTerm.success('success')
    MsgTerm.warning('warning')
    MsgTerm.alert('alert')
    MsgTerm.error('error')
    MsgTerm.fatal('fatal')
