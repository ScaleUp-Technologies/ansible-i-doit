from unicodedata import category
from pprint import pprint
from .base import IDoitApiBase
from .consts import C__CATG__CONNECTOR
from copy import deepcopy
import json


class IDoitCategory(IDoitApiBase):
    def __init__(self, cfg, obj_type: str):
        super().__init__(cfg, obj_type)
        params = {
            'category': obj_type
        }
        r = self.xml_rpc_call('cmdb.category_info', params)
        self.fields = {}
        for fieldname in r['result'].keys():
            default = None
            if 'default' in r['result'][fieldname]['ui']:
                default = r['result'][fieldname]['ui']['default'] or None
            self.fields[fieldname] = {
                'data_type': r['result'][fieldname]['data']['type'],
                'ui_type': r['result'][fieldname]['ui']['type'],
                'default': default,
                'title': r['result'][fieldname]['info']['title']
            }

    def save_category(self, objId, data):
        sdata = deepcopy(data)
        if "_data" in sdata.keys():
            del (sdata["_data"])

        params = {
            "object": objId,
            'category': self.obj_type,
            'data': sdata}
        if self.debug:
            print('--Category Save---')
            pprint(params)
            print('--Category Save---')
        return self.xml_rpc_call('cmdb.category.save', params)

    def update_category(self, objId, data):
        sdata = deepcopy(data)
        if "_data" in sdata.keys():
            del (sdata["_data"])
        if "id" in sdata.keys():
            sdata['category_id'] = sdata['id']
            del (sdata["id"])
        if sdata['category_id'] is None:
            raise Exception('category_id is None')
        params = {
            "objID": objId,
            'category': self.obj_type,
            'data': sdata}
        if self.debug:
            print('--Category Update---')
            pprint(params)
            print('--Category Update---')
        return self.xml_rpc_call('cmdb.category.update', params)

    def read_categories(self, objId):
        params = {
            "objID": objId,
            'category': self.obj_type,
        }
        r = self.xml_rpc_call('cmdb.category.read', params)
        rtn = []
        for item in r['result']:
            rtn.append(self.convert_incomming_category(item))
        return rtn

    def read_category_by_id(self, objId, id):
        for cat in self.read_categories(objId):
            if cat['id'] == id:
                return cat
        # not found
        return None

    def delete_category(self, objId, id):
        params = {
            "objID": objId,
            'category': self.obj_type,
            'cateID': id
        }
        return self.xml_rpc_call('cmdb.category.delete', params)

    def read_category(self, objId):
        r = self.read_categories(objId)
        if len(r) == 0:
            return None
        assert (len(r) == 1)
        return r[0]

    def conv_array_field(self, fieldname, data, ref_field):
        if len(data[fieldname]) == 0:
            return None
        if len(data[fieldname]) != 1:
            raise Exception('Field "%s" has more than one entry %s' %
                            (fieldname, json.dumps(data)))
        return int(data[fieldname][0][ref_field])

    def convert_field(self, fieldname, data):
        object_methods = [method_name for method_name in dir(self)
                          if callable(getattr(self, method_name))]
        field = self.fields[fieldname]
        if fieldname in data.keys():
            if data[fieldname] == None:
                return None
            field_method_name = 'convert_field_with_name_%s' % fieldname
            if field_method_name in object_methods:
                method = getattr(self, field_method_name)
                return method(data)
            try:
                if field['ui_type'] == 'popup':
                    if field['data_type'] == 'int':
                        return int(data[fieldname]['id'])
                if field['ui_type'] == 'text':
                    if field['data_type'] == 'int':
                        return int(data[fieldname])
                    if field['data_type'] == 'float':
                        return float(data[fieldname])
                    if field['data_type'] == 'link':
                        return data[fieldname]
                    if field['data_type'] == 'text':
                        return data[fieldname]
                if field['ui_type'] == 'wysiwyg':
                    if field['data_type'] == 'text':
                        return data[fieldname]
                if field['ui_type'] == 'textarea':
                    if field['data_type'] == 'text_area':
                        return data[fieldname]
                if field['ui_type'] == 'dialog':
                    if field['data_type'] == 'int':
                        return int(data[fieldname]['id'])
                    if field['data_type'] == 'text':
                        return data[fieldname]['id']
            except:
                raise Exception('Wrong conversion ',
                                self.obj_type, fieldname, field, data)
            raise Exception('Unknwown data_type/ ui_type',
                            self.obj_type, fieldname, field, data)

    def convert_incomming_category(self, data):
        rtn = {}
        for fieldname in self.fields.keys():
            rtn[fieldname] = self.convert_field(fieldname, data)
        if 'id' in data.keys():
            rtn['id'] = int(data['id'])
        rtn['_data'] = data
        return rtn

    def partial_equal(self, obj1, obj2):
        if isinstance(obj1, str):
            return (obj1 == obj2)
        if isinstance(obj1, int):
            return (obj1 == obj2)
        if obj2 is None and not (obj1 is None):
            return False
        for key in obj1.keys():
            if key not in obj2:
                return False
            if not (self.partial_equal(obj1[key], obj2[key])):
                return False
        return True

    # Funktioniert nur wo es genau eine Kategory gibt
    def save_category_if_changed(self, objId, data):
        oldData = self.read_category(objId)
        if not (self.partial_equal(data, oldData)):
            print('save', objId, self.obj_type)
            pprint(data)
            print('old:')
            pprint(oldData)
            r = self.save_category(objId, data)
            print(r)

    def update_categorys(self, objId, equals_attr, new_data_arr):
        old_data_arr = self.read_categories(objId)
        for old_data in old_data_arr:
            old_found = False
            for new_data in new_data_arr:
                if old_data[equals_attr] == new_data[equals_attr]:
                    old_found = True
                    if not (self.partial_equal(new_data, old_data)):
                        print('save', objId, self.obj_type)
                        pprint(new_data)
                        print('old:')
                        pprint(old_data)
                        new_data['id'] = old_data['id']
                        r = self.update_category(objId, new_data)
                        pprint(r)
            if not old_found:
                print('delete:', objId, self.obj_type)
                pprint(old_data)
                self.delete_category(objId, old_data['id'])
        for new_data in new_data_arr:
            new_found = False
            for old_data in old_data_arr:
                if old_data[equals_attr] == new_data[equals_attr]:
                    new_found = True
            if not new_found:
                print('save', objId, self.obj_type)
                pprint(new_data)
                r = self.save_category(objId, new_data)
                pprint(r)
