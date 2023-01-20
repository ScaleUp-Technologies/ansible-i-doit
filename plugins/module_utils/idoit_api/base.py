import json
import requests
from pprint import pprint


class IDoitApiBase:
    def __init__(self, cfg, obj_type: str):
        self.cfg = cfg
        self.obj_type = obj_type
        self.debug = False

    def set_debug_mode(self, debug=True):
        self.debug = debug

    def xml_rpc_call(self, method, params, debug=False):
        headers = {'content-type': 'application/json'}
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 1,
        }
        basic_auth = (self.cfg['user'], self.cfg['password'])
        params['apikey'] = self.cfg['api_key']
        response = requests.post(
            self.cfg['jrpc_url'],
            data=json.dumps(payload),
            auth=basic_auth,
            headers=headers
        ).json()
        if self.debug or debug or 'error' in response.keys():
            print('Url')
            print(self.cfg['jrpc_url'])
            print('Payload')
            pprint(payload)
            print('Resonse')
            pprint(response)

        return response
