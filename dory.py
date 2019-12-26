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
    Dory Application
    
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


    def run(self):
        '''Run application'''

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
            self.cal = getCalendar( self.cfg )
            result = self.cal.command( self.args.calendar )

        elif self.args.register:
            self.register = getRegister( self.cfg )
            result = self.register.command( self.args.register )

        # TODO: ...

        if not result:
            sys.exit(1)

        # bye
        self.bye()


if __name__ == '__main__':  # pragma: no cover
    # main
    dory = Dory()
    dory.run()
