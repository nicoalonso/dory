#!/usr/bin/python3
# Dory project

import sys
from argparse import ArgumentParser

from config import MsgTerm
from config import Configurize
from calendars import CalendarBase, GoogleCalendar


# Version
VERSION='v0.1'

# App class
class Dory:

    # Constructor
    def __init__(self):
        pass

    # Bienvenida y despedida
    def wellcome(self):
        msgs = ['', 'Dory %s' % VERSION, '', 'Wellcome to dory', 'The utility for people with fish memory', '']
        MsgTerm.success(msgs, par=True, label='#', bold=True)

    def bye(self):
        MsgTerm.info('See you, Bye!!', hr=True, nl=True, label='#')

    # Parse arguments
    def arguments(self):
        parser = ArgumentParser()
        parser.add_argument('-v', '--verbose', action="store_true", help="Add more verbose to output")
        parser.add_argument('--config', help="Set value to parameter in config file. Ex: calendar.user=root")
        parser.add_argument('-c', '--calendar', help="Commands calendar: check, list")
        self.args = parser.parse_args()

    # Configure
    def config(self):
        if self.args.config.lower() == 'list':
            MsgTerm.info('Show config file:', par=True)
            self.cfg.display()
            return True
        elif '=' in self.args.config:
            parts = self.args.config.split('=')
            if len(parts) == 2:
                value = parts.pop()
                parameter = parts.pop()
                MsgTerm.debug('Update parameter [ %s ] with value "%s"' % (parameter, value))
                section = parameter.split('.')
                name = section.pop()

                self.cfg.set(section, name, value)
                MsgTerm.success('Parameter updated { %s }' % parameter)
                self.cfg.save()
                MsgTerm.success('Config file updated')
                return True

        # Show error
        MsgTerm.fatal("Expected: 'section.name=value' or 'list'")
        return False

    # Get Calendar
    def getCalendar(self):
        typeCalendar = self.cfg.get('calendar', 'type', None)
        if typeCalendar == 'google':
            self.cal = GoogleCalendar(self.cfg)
        else:
            self.cal = Calendar(self.cfg)

    # Calendar
    def cmdCalendar(self):
        self.getCalendar()

        if self.args.calendar.lower() == 'check':
            result = self.cal.check()

        return result

    # Execute application
    def run(self):
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

        # Modify configuration
        result = True
        if self.args.config:
            result = self.config()
        elif self.args.calendar:
            result = self.cmdCalendar()

        # TODO: ...

        if not result:
            sys.exit(1)

        # Despedida
        self.bye()


# Execute
if __name__ == '__main__':
    dory = Dory()
    dory.run()
