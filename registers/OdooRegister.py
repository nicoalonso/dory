# Odoo register

import requests

from .RegisterBase import RegisterBase

# Odoo class register
class OdooRegister(RegisterBase):
    # Constructor
    def __init__(self, config):
        RegisterBase.__init__(self, config)
        self.endpoint = config.get('register.odoo', 'endpoint')
        self.user = config.get('register.odoo', 'user')
        self.password = config.get('register.odoo', 'password')

    # Check connection with register
    def check(self):
        pass
