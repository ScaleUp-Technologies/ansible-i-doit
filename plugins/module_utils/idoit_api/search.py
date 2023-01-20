from pprint import pprint
from .base import IDoitApiBase


class IDoitSearch(IDoitApiBase):

    def search(self, search: str):
        params = {
            'q': search,
        }
        rtn = self.xml_rpc_call('idoit.search', params)
        return rtn['result']
