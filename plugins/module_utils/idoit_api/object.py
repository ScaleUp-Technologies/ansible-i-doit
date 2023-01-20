from .base import IDoitApiBase


class IDoitObject(IDoitApiBase):
    def get_by_title(self, title: str):
        params = {
            'filter': {
                'type': self.obj_type,
                'title': title,
            }
        }
        rtn = self.xml_rpc_call('cmdb.objects', params)
        if len(rtn['result']) == 0:
            return None
        else:
            return rtn['result'][0]

    def get_all(self):
        params = {
            'filter': {
                'type': self.obj_type
            }
        }
        rtn = self.xml_rpc_call('cmdb.objects', params)
        return rtn['result']

    def create_object_with_tile(self, title: str):
        params = {
            'title': title,
            'type': self.obj_type
        }
        return self.xml_rpc_call('cmdb.object.create', params)

    def create_object_if_not_there(self, title):
        obj = self.get_by_title(title)
        if obj is None:
            r = self.create_object_with_tile(title)
            print('-------------------')
            print("%s  (%s) " % (title, self.obj_type))
            print('-------------------')
            objId = r['result']['id']
        else:
            objId = obj['id']
        return objId
