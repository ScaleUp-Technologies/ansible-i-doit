from .base import IDoitApiBase


class IDoitDialog(IDoitApiBase):
    def __init__(self, cfg, obj_type: str, property: str):
        super().__init__(cfg, obj_type)
        self.property = property
        self.cache = {}

    def get_all(self):
        if self.cache == {}:
            params = {
                'category': self.obj_type,
                'property': self.property
            }
            r = self.xml_rpc_call('cmdb.dialog.read', params)
            self.cache = r
        else:
            r = self.cache
        return self.cache['result']

    def get(self, value: str, parent: int = None):
        for entry in self.get_all():
            if parent is None:
                if value == entry['title']:
                    return int(entry['id'])
            else:
                if (value == entry['title'] and
                   entry['parent']['id'] == str(parent)):
                    return int(entry['id'])
        return None

    def get_ignore_case(self, value: str, parent: int = None):
        for entry in self.get_all():
            if parent is None:
                if value.lower() == entry['title'].lower():
                    return int(entry['id'])
            else:
                if (value.lower() == entry['title'].lower() and
                   entry['parent']['id'] == str(parent)):
                    return int(entry['id'])
        return None

    def create(self, value: str, parent: int = None):
        params = {
            'category': self.obj_type,
            'property': self.property,
            'value': value
        }
        self.cache = {}
        if parent is not None:
            params['parent'] = parent
        r = self.xml_rpc_call('cmdb.dialog.create', params)
        return r['result']['entry_id']

    def create_or_get_id(self, value: str, parent: int = None):
        id = self.get(value, parent)
        if id is None:
            id = self.create(value, parent)
        return id
