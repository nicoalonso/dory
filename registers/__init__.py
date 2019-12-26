#!/usr/bin/python3

from msgterm import MsgTerm

from .RegisterBase import RegisterBase
from .SimulateRegister import SimulateRegister
from .OdooRegister import OdooRegister

# List of registers defined
registerTypes = {
    'odoo': OdooRegister,
    'simulate': SimulateRegister
}


def getRegister(cfg):
    '''Get register
    
    Return the class instance of register defined by the user
    
    Arguments:
        cfg {Configurize}: User configuration
    
    Returns:
        RegisterBase: Instance inherit from RegisterBase
    '''

    typeReg = cfg.get('register.type', None)
    MsgTerm.debug('Register type: %s' % typeReg)
    
    if typeReg in registerTypes:
        targetClass = registerTypes[typeReg]
        return targetClass(cfg)
    else:
        return SimulateRegister(cfg)
