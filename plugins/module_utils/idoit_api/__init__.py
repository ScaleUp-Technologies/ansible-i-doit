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

def createApiCalls(cfg):
    rtn={}
    rtn[consts.C__CATG__CONNECTOR]=IDoitConnector(cfg)
    rtn[consts.C__CATG__CUSTOM_FIELDS_RACKTABLES]=Racktables(cfg)
    rtn[consts.C__CATG__LOCATION]=IDoitLocation(cfg)
    rtn[consts.C__CATG__NETWORK_PORT]=IDoitNetworkPort(cfg)
    for varname in consts.__dict__.keys():
        if not (varname in rtn.keys()):
            if varname.startswith('C__OBJTYPE__'):
                rtn[varname]=IDoitObject(cfg, varname)
            if varname.startswith('C__CATS__') or varname.startswith('C__CATG__'):
                rtn[varname]=IDoitCategory(cfg, varname)
    return rtn


def createApiDialogs(cfg,category, field):
    if  not 'dialogs' in cfg.keys():
        cfg['dialogs']={}
    if not category in cfg['dialogs'].keys():
        cfg['dialogs'][category]={}
    if not field in cfg['dialogs'][category].keys():
        cfg['dialogs'][category][field]=IDoitDialog(cfg, category, field)
    return cfg['dialogs'][category][field]

def search(cfg):
    return IDoitSearch(cfg,'no_type')