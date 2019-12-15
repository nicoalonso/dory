#!/usr/bin/python3
# Project configuration

import json
from pathlib import Path

from . import MsgTerm


# Folder to contains projects config
FOLDER_PROJECTS = '.nk'


# Configurize class
class Configurize:

    # Constructor
    # 
    # @param  string   project      Project Name
    # @param  string   filename     Config file name
    # 
    def __init__(self, project, filename='config'):
        self.project = project
        self.filename = filename + '.json'
        self.filepath = ''
        self.config = {}

    # Get the home config file path
    def getHomeFilePath(self):
        folder = Path.home() / FOLDER_PROJECTS;
        # Create folder if not exists
        if not folder.exists():
            folder.mkdir()
            MsgTerm.debug('[Config] create folder %s' % str(folder))

        projectFolder = folder / self.project
        # Create project folder if not exists
        if not projectFolder.exists():
            projectFolder.mkdir()
            MsgTerm.debug('[Config] create folder %s' % str(projectFolder))

        # Config file path
        self.filepath = projectFolder / self.filename

    # Load project config
    # 
    # @return Boolean
    # 
    def load(self):
        self.getHomeFilePath()

        # Check if config file exists
        MsgTerm.debug('[Config] Search config file %s' % self.filepath)
        if self.filepath.exists() and self.filepath.is_file():
            MsgTerm.debug('[Config] load config %s' % self.filepath)
            with self.filepath.open() as json_file:
                self.config = json.load(json_file)
        else:
            MsgTerm.warning('[Config] Configuration file not found: %s' % self.filename)
            localConfig = Path('.') / self.filename
            MsgTerm.debug('[Config] load local configuration: %s' % localConfig)
            if localConfig.exists() and localConfig.is_file():
                with localConfig.open() as localConfig:
                    self.config = json.load(localConfig)
            else:
                MsgTerm.fatal('[Config] Configuration file not found')
                return False

        return True

    # Save project config
    def save(self):
        if not self.filepath:
            self.getHomeFilePath()

        with self.filepath.open('w') as json_file:
            json.dump(self.config, json_file, indent=4)

    # Get value of property
    def get(self, section, name, default=None):
        parts = section.split('.')
        aux = self.config
        for item in parts:
            aux = aux.get(item, None)
            if aux == None:
                MsgTerm.fatal('[Config] section not exists %s' % section)
                return default

        return aux.get(name, default)

    # Return a boolean
    def bool(self, section, name, default=False):
        return bool(self.get(section, name, default))

    # Return a integer
    def int(self, section, name, default=0):
        return int(self.get(section, name, default))

    # Return a float value
    def float(self, section, name, default=0.0):
        return float(self.get(section, name, default))

    # Return a string
    def str(self, section, name, default=''):
        return str(self.get(section, name, default))

    # Return a list
    def list(self, section, name, default=[]):
        return list(self.get(section, name, default))

# Test config file
if __name__ == '__main__':
    cfg = Configurize('Test')
    cfg.load()
