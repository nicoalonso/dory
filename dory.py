#!/usr/bin/python3
# Dory project

import sys
from argparse import ArgumentParser

from config import MsgTerm
from config import Configurize
from calendars import getCalendar
from registers import getRegister

# Version
VERSION='v0.1'

# App class
class Dory:
    # Wellcome
    def wellcome(self):
        msgs = ['', 'Dory %s' % VERSION, '', 'Wellcome to dory', 'The utility for people with fish memory', '']
        MsgTerm.success(msgs, par=True, label='#', bold=True)

    # Goodbye
    def bye(self):
        MsgTerm.info('See you, Bye!!', hr=True, nl=True, label='#')

    # Parse arguments
    def arguments(self):
        parser = ArgumentParser()
        parser.add_argument('-v', '--verbose', action="store_true", help="Add more verbose to output")
        parser.add_argument('--config', help="Config command")
        parser.add_argument('-c', '--calendar', help="Calendar command")
        parser.add_argument('-r', '--register', help="Register command")
        parser.add_argument('-d', '--daemon', action="store_true", help="Daemon Mode")
        parser.add_argument('-j', '--journal', action="store_true", help="Journal Mode")
        self.args = parser.parse_args()

    # Configure
    def config(self):
        result = True
        action = self.args.config.lower()
        if action == 'help':
            info = [
                'list of commands:',
                '',
                ' - list:  List of configuration',
                ' - help:  Show this help',
                ' - section.name=value   : Set a value for a key'
            ]
            MsgTerm.help(info, section='Config')
        elif action == 'list':
            MsgTerm.info('Show config file:', par=True)
            self.cfg.display()
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
                self.cfg.display()
            else:
                MsgTerm.error("[Config] Error: expected 'section.name=value'")
                result = False
        else:
            MsgTerm.alert('[Config] Unknown action: %s' % self.args.config, nl=True)
            MsgTerm.help('use the command { help } for more information', section='Config', nl=True)
            result = False

        # Show error
        return result

    # Calendar
    def cmdCalendar(self):
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

    # Register
    def cmdRegister(self):
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

        # Execute commands
        result = True
        if self.args.config:
            result = self.config()
        elif self.args.calendar:
            result = self.cmdCalendar()
        elif self.args.register:
            result = self.cmdRegister()

        # TODO: ...

        if not result:
            sys.exit(1)

        # Despedida
        self.bye()


# Execute
if __name__ == '__main__':
    dory = Dory()
    dory.run()
