from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
from . import utils as idoit_utils
from pprint import pprint
import idoit_scaleup
import json
from math import isclose
from datetime import datetime

class IdoitCategoryModule(AnsibleModule):
    def __init__(self, *args, idoit_spec):

        self.idoit_spec = idoit_spec
        if idoit_spec['single_value_cat']:
            state_choices = ['present', 'merge']
        else:
            state_choices = ['absent', 'merge', 'present']

        arg_spec = dict(
            idoit=idoit_utils.idoit_argument_spec,
            obj_id=dict(type="int", required=True),
            state=dict(choices=state_choices, default='present')
        )
        ansible_fields = {}
        for idoit_name in idoit_spec['fields'].keys():
            field = idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            ansible_fields[ansible_name] = field
            if field['type'] in  ['str','html','datetime']:
                arg_spec[ansible_name] = dict(type='str')
            elif field['type'] == 'float':
                arg_spec[ansible_name] = dict(type='float')
            elif field['type'] == 'int':
                arg_spec[ansible_name] = dict(type='int')
            elif field['type'] == 'bool':
                arg_spec[ansible_name] = dict(type='bool')
            elif field['type'] == 'list':
                arg_spec[ansible_name] = dict(
                    type='list', elements=field['element_type'])
            elif field['type'] == 'dialog':
                arg_spec[ansible_name] = dict(type='str')
                arg_spec[ansible_name+'_id'] = dict(type='int')
                ansible_fields[ansible_name+'_id'] = field
            else:
                raise Exception('Unknown Type type=%s' % field['type'])
        self.ansible_fields = ansible_fields
        if not idoit_spec['single_value_cat']:
            arg_spec['id'] = {
                'type': 'int',
            }
            arg_spec['search_by_fields'] = {
                'type': 'list',
            }
        super().__init__(*args, argument_spec=arg_spec, supports_check_mode=True)

    def run(self):
        # in cfg werden durch die Api noch Werte gecached, was bei Module.params nicht geht
        self.cfg = json.loads(json.dumps(self.params['idoit']))
        if self.cfg['api_log']:
            idoit_scaleup.turn_on_api_logging()
        self.idoit_cat_api = idoit_scaleup.createApiCall(
            self.cfg, self.idoit_spec['category'])
        if self.idoit_spec['single_value_cat']:
            old_idoit_data = self.idoit_cat_api.read_category(
                self.params['obj_id'])
        else:
            if self.params['id'] and self.params['search_by_fields']:
                self.fail_json(
                    msg='You can only specify "id" or "search_by_fields" not both')
            if self.params['id']:
                old_idoit_data = self.idoit_cat_api.read_category_by_id(
                    self.params['obj_id'], self.params['id'])
            elif self.params['search_by_fields']:
                cat_ids = []
                result = self.idoit_cat_api.read_categories(
                    self.params['obj_id'])
                for idoit_cat in result:
                    equal = True
                    cat = self.conv_idoit_to_ansible(idoit_cat)
                    for field in self.params['search_by_fields']:
                        if field not in cat.keys():
                            equal = False
                        elif cat[field] != self.params[field]:
                            equal = False
                    if equal:
                        old_idoit_data = idoit_cat
                        cat_ids.append(idoit_cat['id'])
                if len(cat_ids) > 1:
                    self.fail_json(msg='More than one category with the same search_by_fields (ids:%s)' % ",".join(
                        list(map(str, cat_ids))))
                elif len(cat_ids) == 0:
                    old_idoit_data = None
                elif len(cat_ids) == 1:
                    self.params['id'] = cat_ids[0]
            else:
                old_idoit_data = {}
        if self.params['state'] == 'present':
            self.present(old_idoit_data, False)
        elif self.params['state'] == 'merge':
            self.present(old_idoit_data, True)
        elif self.params['state'] == 'absent':
            # state absent
            self.absent(self.params['obj_id'], old_idoit_data)
        else:
            self.fail_json('Unknown state')

    def absent(self, obj_id, old_idoit_data):
        result = {}
        if old_idoit_data is None:
            result['changed'] = False
        else:
            if self.check_mode:
                r = 'Not deleted, check_mode=true'
            else:
                r = self.idoit_cat_api.delete_category(
                    obj_id, old_idoit_data['id'])
            result['changed'] = True
            result['return'] = r
        if self.cfg['api_log']:
            result['api_log'] = idoit_scaleup.get_api_log()
        self.exit_json(**result)

    def conv_idoit_to_ansible(self, idoit_data):
        data = {}
        for idoit_name in self.idoit_spec['fields'].keys():
            field = self.idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            if field['type'] == 'dialog':
                ansible_name = '%s_id' % (ansible_name)
            if idoit_name in idoit_data.keys():
                data[ansible_name] = idoit_data[idoit_name]
        return data

    def dialog_field(self, field, ansible_name, idoit_name, new_data):
        ansible_id_name = '%s_id' % (ansible_name)
        my_dialog_api = None
        my_dialog_id = None
        if self.params[ansible_name] is not None and self.params[ansible_id_name] is not None:
            self.fail_json(msg='You can only specify %s or %s' %
                           (ansible_name, ansible_id_name))
        if self.params[ansible_id_name] is not None:
            my_dialog_id = self.params[ansible_id_name]
        if self.params[ansible_name] is not None:
            my_dialog_api = idoit_scaleup.createApiDialogs(
                self.cfg, self.idoit_spec['category'], idoit_name)
            if my_dialog_api is None:
                raise Exception(
                    'Dialog API for type %s is None' % idoit_name)
            dialog_parent_id = None
            if 'dialog_parent' in field:
                dialog_parent_field_name = '%s_id' % field['dialog_parent']
                if not dialog_parent_field_name in new_data.keys():
                    dialog_parent_field_name = field['dialog_parent']
                dialog_parent_id = new_data[dialog_parent_field_name]
                if dialog_parent_id is None:
                    my_msg = 'You need to specify a %s or %s if you want to set %s' % (
                        field['dialog_parent'], dialog_parent_field_name, ansible_name)
                    self.fail_json(msg=my_msg)
            if my_dialog_api is None:
                my_dialog_id = None
            else:
                my_dialog_id = my_dialog_api.get_ignore_case(
                    self.params[ansible_name], dialog_parent_id)
        if my_dialog_id is not None:
            return (False, my_dialog_id)
        elif self.check_mode:
            return (True, -42)
        elif my_dialog_api is None:
            return (False, None)
        else:
            if not (self.idoit_cat_api.is_dialog_plus_field(idoit_name)):
                titles = []
                for dialog_ele in my_dialog_api.get_all():
                    titles.append(dialog_ele['title'])
                self.fail_json(msg='Wrong value %s for field %s You can only use [ %s ] ' %
                               (self.params[ansible_name], ansible_name, ", ".join(titles)))
            else:
                ret = my_dialog_api.create(
                    self.params[ansible_name], dialog_parent_id)
                return (True, ret)

    def present(self,  old_idoit_data, merge_mode):
        result = dict(
            changed=False
        )
        new_data = {}
        idoit_new_data = {}
        if old_idoit_data is None:
            old_data = {}
        else:
            old_data = self.conv_idoit_to_ansible(old_idoit_data)

        for idoit_name in self.idoit_spec['fields'].keys():
            field = self.idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            if ((not merge_mode) and
                    (self.params[ansible_name] is None)):
                if ('default' in field.keys()):
                    self.params[ansible_name] = field['default']
                elif (field['type'] in ['str', 'html']):
                    self.params[ansible_name] = ""
            if (field['type']=='datetime'):
                try:
                    datetime_object = datetime.strptime(self.params[ansible_name], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    self.fail_json(msg=f"Datetime not parseable in {ansible_name} field (value={self.params[ansible_name]}")
            if ((field['type'] in ['dialog', 'str']) and
                (self.params[ansible_name] is not None) and
                    ('\n' in self.params[ansible_name])):
                self.fail_json(msg='Linefeed is not allowed in %s field (value="%s")' %
                                   (ansible_name, self.params[ansible_name]))
            if field['type'] in ['html', 'str', 'float', 'int', 'datetime']:
                new_data[ansible_name] = self.params[ansible_name]
                idoit_new_data[idoit_name] = new_data[ansible_name]
            elif field['type'] == 'dialog':
                ansible_id_name = '%s_id' % (ansible_name)
                (change, dialog_val) = self.dialog_field(
                    field, ansible_name, idoit_name, new_data)
                if change:
                    result['changed'] = True
                new_data[ansible_id_name] = dialog_val
                idoit_new_data[idoit_name] = dialog_val
            elif field['type'] == 'bool':
                new_data[ansible_name] = self.params[ansible_name]
                if new_data[ansible_name]:
                    idoit_new_data[idoit_name] = 1
                else:
                    idoit_new_data[idoit_name] = 0
            elif field['type'] == 'list':
                new_data[ansible_name] = self.params[ansible_name]
                idoit_new_data[idoit_name] = self.params[ansible_name]
            else:
                raise Exception('Unknown Type %s' % field['type'])
        result['data'] = new_data
        sanitized_before = {}
        sanitized_after = {}
        for key in old_data.keys():
            if key not in new_data.keys():
                if merge_mode:
                    new_data[key] = old_data[key]
                    if old_data[key] is not None:
                        idoit_new_data[key] = old_data[key]
                else:
                    result['changed'] = True
                    sanitized_before[key] = old_data[key]
            elif new_data[key] is None and merge_mode:
                new_data[key] = old_data[key]
                if old_data[key] is not None:
                    # Je nach Typ bearbeiten, bei dialog z.B. muss das _id wieder weg
                    if key in self.idoit_spec['fields'].keys():
                        type=self.idoit_spec['fields'][key]['type']
                        if type in ['html', 'str', 'float', 'int', 'list']:
                            idoit_new_data[key] = old_data[key]
                        elif type == 'bool':
                            if old_data[key]:
                                idoit_new_data[key] = 1
                            else:
                                idoit_new_data[key] = 0
                        else:
                            raise Exception('Unknown old data type %s in merge mode %s = %s' % (type, key, old_data[key]))
                    elif ((key.endswith('_id')) and
                         (key[:-3] in self.idoit_spec['fields'].keys()) and
                         (self.idoit_spec['fields'][key[:-3]]['type']=='dialog')):
                        idoit_new_data[key[:-3]]=old_data[key]

        for key in new_data.keys():
            if key not in old_data.keys():
                result['changed'] = True
                sanitized_after[key] = new_data[key]
            elif self.ansible_fields[key]['type'] == 'list':
                changed_list = False
                old_members = old_data[key]
                new_members = new_data[key]
                if old_members is None:
                    old_members = []
                if new_members is None:
                    new_members = []
                if len(old_members) != len(new_members):
                    changed_list = True
                else:
                    for ele in old_members:
                        if ele not in new_members:
                            changed_list = True
                            break
                if changed_list:
                    result['changed'] = True
                    sanitized_before[key] = old_data[key]
                    sanitized_after[key] = new_data[key]
            elif self.ansible_fields[key]['type'] == 'float':
                changed_float = False
                if new_data[key] is None and old_data[key] is not None:
                    changed_float = True
                if new_data[key] is not None and old_data[key] is None:
                    changed_float = True
                if new_data[key] is not None and old_data[key] is not None:
                    if not (isclose(new_data[key], old_data[key], rel_tol=1e-3)):
                        changed_float = True
                if changed_float:
                    result['changed'] = True
                    sanitized_before[key] = old_data[key]
                    sanitized_after[key] = new_data[key]
            elif new_data[key] != old_data[key]:
                result['changed'] = True
                sanitized_before[key] = old_data[key]
                sanitized_after[key] = new_data[key]
        if result['changed']:
            if self.check_mode:
                r = 'Not modified, check_mode=True'
            else:
                if 'id' in self.params.keys() and self.params['id'] is not None:
                    idoit_new_data['id'] = self.params['id']
                    r = self.idoit_cat_api.update_category(
                        self.params['obj_id'], idoit_new_data)
                    result['id'] = idoit_new_data['id']
                else:
                    r = self.idoit_cat_api.save_category(
                        self.params['obj_id'], idoit_new_data)
                    if r is None:
                        api_log=idoit_scaleup.get_api_log()
                        self.fail_json(msg='None RTN nach Cat Save',idn=idoit_new_data, api_log=api_log)
                    if 'result' not in r:
                        api_log=idoit_scaleup.get_api_log()
                        self.fail_json(msg='No Result in r nach Cat Save',idn=idoit_new_data, rtn=r, api_log=api_log)
                    if r['result'] is None:
                        api_log=idoit_scaleup.get_api_log()
                        self.fail_json(msg='None Result in r nach Cat Save',idn=idoit_new_data, rtn=r, api_log=api_log)

                    if 'entry' in r['result']:
                        result['id'] = r['result']['entry']
                    else:
                        self.fail_json(msg='Keine Id nach Save',
                                       rtn=r['result'])
            result['return'] = r
        else:
            if 'id' in old_idoit_data.keys():
                result['id'] = old_idoit_data['id']
            else:
                result['no_id'] = old_idoit_data
        if self._diff:
            result["diff"] = {
                "before": sanitized_before,
                "after": sanitized_after,
            }
        if self.cfg['api_log']:
            result['api_log'] = idoit_scaleup.get_api_log()
        self.exit_json(**result)


class IdoitCategoryInfoModule(AnsibleModule):
    def __init__(self, *args, idoit_spec):
        self.idoit_spec = idoit_spec
        arg_spec = dict(
            idoit=idoit_utils.idoit_argument_spec,
            obj_id=dict(type="int", required=True),
        )
        super().__init__(*args, argument_spec=arg_spec, supports_check_mode=True)

    def convert_idoit_api_to_ansible(self, idoit_data):
        ans_data = {}
        if idoit_data == None:
            return None
        for idoit_name in self.idoit_spec['fields'].keys():
            field = self.idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            if not 'type' in field.keys():
                raise Exception('Type not defined %s' % json.dumps(field))
            if field['type'] in ['str', 'float', 'int', 'bool', 'html', 'list','datetime']:
                ans_data[ansible_name] = idoit_data[idoit_name]
            elif field['type'] == 'dialog':
                ansible_id_name = '%s_id' % (ansible_name)
                ans_data[ansible_id_name] = idoit_data[idoit_name]
            else:
                raise Exception('Unknown Type %s' % field['type'])
        if not self.idoit_spec['single_value_cat']:
            ans_data['id'] = idoit_data['id']
        return ans_data

    def run(self):
        self.cfg = json.loads(json.dumps(self.params['idoit']))
        if self.cfg['api_log']:
            idoit_scaleup.turn_on_api_logging()
        self.idoit_cat_api = idoit_scaleup.createApiCall(
            self.cfg, self.idoit_spec['category'])
        if self.idoit_spec['single_value_cat']:
            old_idoit_data = self.idoit_cat_api.read_category(
                self.params['obj_id'])
            old_data = self.convert_idoit_api_to_ansible(old_idoit_data)
            rtn = {'data': old_data}
        else:
            old_idoit_data_arr = self.idoit_cat_api.read_categories(
                self.params['obj_id'])
            data = []
            for old_idoit_data in old_idoit_data_arr:
                data.append(self.convert_idoit_api_to_ansible(old_idoit_data))
            rtn = {'data': data}
        if self.cfg['api_log']:
            rtn['api_log'] = idoit_scaleup.get_api_log()
        self.exit_json(**rtn)
