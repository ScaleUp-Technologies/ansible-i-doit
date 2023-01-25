from .object import IDoitObject
from . import consts
from pprint import pprint
from .location import IDoitLocation
from .racktables import Racktables
from .category import IDoitCategory
from .connector import IDoitConnector
from .networkport import IDoitNetworkPort
from .dialog import IDoitDialog
from .search import IDoitSearch
from .memory import IDoitMemory
from .cpu import IDoitCpu
from .power_consumer import IDoitPowerConsumer



def createApiCall(cfg, category):
    if category == consts.C__CATG__CONNECTOR:
        return IDoitConnector(cfg)
    if category == consts.C__CATG__CUSTOM_FIELDS_RACKTABLES:
        return Racktables(cfg)
    if category == consts.C__CATG__LOCATION:
        return IDoitLocation(cfg)
    if category == consts.C__CATG__MEMORY:
        return IDoitMemory(cfg)
    if category == consts.C__CATG__NETWORK_PORT:
        return IDoitNetworkPort(cfg)
    if category == consts.C__CATG__POWER_CONUMER:
        return IDoitPowerConsumer(cfg)
    if category == consts.C__CATG__CPU:
        return IDoitCpu(cfg)
    if category.startswith('C__OBJTYPE__'):
        return IDoitObject(cfg, category)
    if category.startswith('C__CATS__') or category.startswith('C__CATG__'):
        return IDoitCategory(cfg, category)
    return None

def createApiCalls(cfg):
    rtn = {}
    for varname in consts.__dict__.keys():
        if not (varname in rtn.keys()):
            rtn[varname] = createApiCall(cfg, varname)
    return rtn

def createApiDialogs(cfg, category, field):
    if 'dialogs' not in cfg.keys():
        cfg['dialogs'] = {}
    if category not in cfg['dialogs'].keys():
        cfg['dialogs'][category] = {}
    if field not in cfg['dialogs'][category].keys():
        cfg['dialogs'][category][field] = IDoitDialog(cfg, category, field)
    return cfg['dialogs'][category][field]


def search(cfg):
    return IDoitSearch(cfg, 'no_type')
