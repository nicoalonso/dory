# Package registers

from config import MsgTerm

from .RegisterBase import RegisterBase
from .SimulateRegister import SimulateRegister
from .OdooRegister import OdooRegister

# List of registers defined
registerTypes = {
    'odoo': OdooRegister,
    'simulate': SimulateRegister
}

# Get calendar
def getRegister(cfg):
    typeReg = cfg.get('register', 'type', None)
    MsgTerm.debug('Register type: %s' % typeReg)
    if typeReg in registerTypes:
        targetClass = registerTypes[typeReg]
        return targetClass(cfg)
    else:
        return SimulateRegister(cfg)
