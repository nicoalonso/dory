#!/usr/bin/python3
# Project configuration

from msgterm import MsgTerm

# Configurize class
class Configurize:

    # Constructor
    # 
    # @param  string   project      Project Name
    # @param  string   filename     Config file name
    # 
    def __init__(self, project, filename='config'):
        self.project = project
        self.filename = filename + '.py'

    # Load project config
    def load(self):
        pass




if __name__ == '__main__':

    MsgTerm.message('message')
    MsgTerm.text('text')
    MsgTerm.debug('debug')
    MsgTerm.info('info')
    MsgTerm.warning('warning')
    MsgTerm.alert('alert')
    MsgTerm.error('error')
    MsgTerm.fatal('fatal')

    # cfg = Configurize('Test')
    # cfg.load()
