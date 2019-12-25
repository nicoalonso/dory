#!/usr/bin/python3
# Dory project

import sys
from argparse import ArgumentParser

from msgterm import MsgTerm
from configurize import Configurize
from calendars import getCalendar
from registers import getRegister

# Version
VERSION='v0.1'

class Dory:
    '''
    Dory App
    
    Attributes:
        args (ArgumentParser): Object to parse the user input
        cfg  (Configurize)   : This object is used for get the user configuration
        cal  (CalendarBase)  : Object for get the user calendar
    '''

    def wellcome(self):
        '''Show wellcome message'''

        msgs = ['', 'Dory %s' % VERSION, '', 'Wellcome to dory', 'The utility for people with fish memory', '']
        MsgTerm.success(msgs, par=True, label='#', bold=True)


    def bye(self):
        '''Show the goodbye message'''

        MsgTerm.info('See you, Bye!!', hr=True, nl=True, label='#')


    def arguments(self):
        '''Parse input arguments'''

        parser = ArgumentParser()
        parser.add_argument('-v', '--verbose', action="store_true", help="Add more verbose to output")
        parser.add_argument('--config', help="Config command")
        parser.add_argument('-c', '--calendar', help="Calendar command")
        parser.add_argument('-r', '--register', help="Register command")
        parser.add_argument('-d', '--daemon', action="store_true", help="Daemon Mode")
        parser.add_argument('-j', '--journal', action="store_true", help="Journal Mode")
        self.args = parser.parse_args()


    def cmdCalendar(self):
        '''Calendar command
        
        Actions:
            [ help ][ check ][ list ][ debug ]
        
        Returns:
            bool: Command result
        '''

        self.cal = getCalendar(self.cfg)

        result = True
        action = self.args.calendar.lower()
        if action == 'check':
            result = self.cal.check()
        elif action == 'list':
            result = self.cal.list()
        elif action == 'debug':
            result = self.cal.list( True )
        elif action == 'help':
            info = [
                'list of commands:',
                '',
                ' - check: Check connection with calendar',
                ' - list : Get list of events',
                ' - help : Show this help'
            ]
            MsgTerm.help(info, section='Calendar')
        else:
            MsgTerm.alert('[Calendar] Unknown action: %s' % self.args.calendar, nl=True)
            MsgTerm.help('use the command { help } for more information', section='Calendar', nl=True)
            result = False

        return result


    def cmdRegister(self):
        '''Register command
        
        Actions:
            [ help ][ check ][ list ]
        
        Returns:
            bool: Command result
        '''
        result = True
        self.register = getRegister(self.cfg)
        action = self.args.register.lower()

        if action == 'check':
            result = self.register.check()
        elif action == 'list':
            result = self.register.list()

        elif action == 'help':
            info = [
                'List of commands:',
                '',
                ' - check: Check connection with register',
                ' - list : Get list of records',
                ' - help : Show this help'
            ]
            MsgTerm.help(info, section='Register')
        else:
            MsgTerm.alert('[Register] Unknown action: %s' % self.args.register, nl=True)
            MsgTerm.help('use the command { help } for more information', section='Register', nl=True)
            result = False

        return result


    def run(self):
        '''Execute application'''

        self.wellcome()
        # Parse arguments
        self.arguments()
        # Set verbosity
        if self.args.verbose:
            MsgTerm.verbosity(MsgTerm.DEBUG)

        # Load config file
        self.cfg = Configurize('dory')
        if not self.cfg.load():
            sys.exit(1)

        # Execute commands
        result = True
        if self.args.config:
            result = self.cfg.command( self.args.config )
        elif self.args.calendar:
            result = self.cmdCalendar()
        elif self.args.register:
            result = self.cmdRegister()

        # TODO: ...

        if not result:
            sys.exit(1)

        # bye
        self.bye()


if __name__ == '__main__':  # pragma: no cover
    # main
    dory = Dory()
    dory.run()
