from pprint import pprint
from .base import IDoitApiBase


class IDoitConditionalRead(IDoitApiBase):

    def __init__(self, cfg, obj_type: str):
        super().__init__(cfg, obj_type)#
        self.clear_search_list()

    def clear_search_list(self):
        self.search_list=[]

    def add_search_param(self, category: str, field: str, value: str, operator: str=None, compare:str="=", ):
        entry={
                'property': "%s-%s" % (category, field),
                'comparison': compare,
                'value': value,
        }
        if operator:
            entry['operator']=operator
        self.search_list.append(entry)

    def search(self):
        params = {
            'conditions': self.search_list,
        }
        rtn = self.xml_rpc_call('cmdb.condition.read', params)
        return rtn['result']
