#!/usr/bin/python3

from msgterm import MsgTerm


class CalendarBase:
    '''Calendar base class
    
    Args:
        config (Configurize): The config is used for get the user configuration

    Attributes:
        cfg    (Configurize): Configuration object
    '''

    def __init__(self, config):
        self.cfg = config


    def check(self):
        '''Check calendar connection
        
        Returns:
            bool: result check
        '''
        MsgTerm.error('Error: Check is not implemented', nl=True)
        return False


    def list(self, debug=False):
        '''Show events list
        
        Keyword Arguments:
            debug {bool}: only for development (default: {False})
        
        Returns:
            bool: result
        '''
        MsgTerm.error('Error: List events is not implemented', nl=True)
        return False


    def getTodayEvent(self):
        '''Return today's event
        
        Returns:
            None|event
        '''
        MsgTerm.error('Error: Today event is not implemented', nl=True)
        return None


    def command(self, action):
        '''Calendar command
        
        Args:
            action {string}
        
        Returns:
            bool: Command result
        '''
        result = True
        action = action.lower()
        if action == 'check':
            result = self.check()
        elif action == 'list':
            result = self.list()
        elif action == 'debug':
            result = self.list( True )
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
            MsgTerm.alert('[Calendar] Unknown action: %s' % action, nl=True)
            MsgTerm.help('use the command { help } for more information', section='Calendar', nl=True)
            result = False

        return result