from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
# import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from . import utils as idoit_utils
from pprint import pprint
from . import idoit_api
import json


class IdoitCategoryModule(AnsibleModule):
    def __init__(self, *args, idoit_spec):

        self.idoit_spec = idoit_spec
        if idoit_spec['single_value_cat']:
            state_choices = ['present']
        else:
            state_choices = ['absent', 'present']

        arg_spec = dict(
            idoit=idoit_utils.idoit_argument_spec,
            obj_id=dict(type="int", required=True),
            state=dict(choices=state_choices, default='present')
        )
        for idoit_name in idoit_spec['fields'].keys():
            field = idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            if field['type'] == 'str':
                arg_spec[ansible_name] = dict(type='str', default='')
            elif field['type'] == 'float':
                arg_spec[ansible_name] = dict(type='float')
            elif field['type'] == 'dialog':
                arg_spec[ansible_name] = dict(type='str')
                arg_spec[ansible_name+'_id'] = dict(type='int')
            else:
                raise Exception('Unknown Type type=%s' % field['type'])

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
        self.idoit_cat_api = idoit_api.createApiCall(
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
                            print("== not found %s ==" % field)
                            equal = False
                        elif cat[field] != self.params[field]:
                            print("== not equal %s ==" % field)
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
            self.present(old_idoit_data)
        else:
            # state absent
            self.absent(self.params['obj_id'], old_idoit_data)

    def absent(self, obj_id, old_idoit_data):
        result = {}
        if old_idoit_data == None:
            result['changed'] = False
        else:
            if self.check_mode:
                r = 'Not deleted, check_mode=true'
            else:
                r = self.idoit_cat_api.delete_category(
                    obj_id, old_idoit_data['id'])
            result['changed'] = True
            result['return'] = r
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

    def present(self,  old_idoit_data):
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
            if field['type'] == 'str':
                new_data[ansible_name] = self.params[ansible_name]
                idoit_new_data[idoit_name] = new_data[ansible_name]
            elif field['type'] == 'dialog':
                ansible_id_name = '%s_id' % (ansible_name)
                if self.params[ansible_name] is not None and self.params[ansible_id_name] is not None:
                    self.fail_json(msg='You can only specify %s or %s' %
                                   (ansible_name, ansible_id_name))
                if self.params[ansible_id_name] is not None:
                    new_data[ansible_id_name] = self.params[ansible_id_name]
                if self.params[ansible_name] is not None:
                    my_dialog_api = idoit_api.createApiDialogs(
                        self.cfg, self.idoit_spec['category'], idoit_name)
                dialog_parent_id = None
                if 'dialog_parent' in field:
                    dialog_parent_field_name = '%s_id' % field['dialog_parent']
                    dialog_parent_id = new_data[dialog_parent_field_name]
                    if dialog_parent_id is None:
                        my_msg = 'You need to specify a %s or %s if you want to set %s' % (
                            field['dialog_parent'], dialog_parent_field_name, ansible_name)
                        self.fail_json(msg=my_msg, **result)
                my_dialog_id = my_dialog_api.get(
                    self.params[ansible_name], dialog_parent_id)
                if my_dialog_id is not None:
                    new_data[ansible_id_name] = my_dialog_id
                    idoit_new_data[idoit_name] = my_dialog_id
                elif self.check_mode:
                    result['changed'] = True
                    new_data[ansible_id_name] = -42
                else:
                    new_data[ansible_id_name] = my_dialog_api.create(
                        self.params[ansible_name], dialog_parent_id)
                    idoit_new_data[idoit_name] = new_data[ansible_id_name]
            elif field['type'] == 'float':
                new_data[ansible_name] = self.params[ansible_name]
                idoit_new_data[idoit_name] = new_data[ansible_name]
            else:
                raise Exception('Unknown Type')
        result['data'] = new_data
        sanitized_before = {}
        sanitized_after = {}
        for key in new_data.keys():
            if key not in old_data.keys():
                result['changed'] = True
                sanitized_after[key] = new_data[key]
            elif new_data[key] != old_data[key]:
                result['changed'] = True
                sanitized_before[key] = old_data[key]
                sanitized_after[key] = new_data[key]
        for key in old_data.keys():
            if key not in new_data:
                result['changed'] = True
                sanitized_before[key] = old_data[key]
        if result['changed']:
            if self.check_mode:
                r = 'Not modified, check_mode=True'
            else:
                if 'id' in self.params.keys() and self.params['id'] is not None:
                    idoit_new_data['id'] = self.params['id']
                    r = self.idoit_cat_api.update_category(
                        self.params['obj_id'], idoit_new_data)
                else:
                    r = self.idoit_cat_api.save_category(
                        self.params['obj_id'], idoit_new_data)
            result['return'] = r
        if self._diff:
            result["diff"] = {
                "before": sanitized_before,
                "after": sanitized_after,
            }

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
        for idoit_name in self.idoit_spec['fields'].keys():
            field = self.idoit_spec['fields'][idoit_name]
            ansible_name = idoit_name
            if 'ansible_name' in field.keys():
                ansible_name = field['ansible_name']
            if field['type'] == 'str':
                ans_data[ansible_name] = idoit_data[idoit_name]
            elif field['type'] == 'float':
                ans_data[ansible_name] = idoit_data[idoit_name]
            elif field['type'] == 'dialog':
                ansible_id_name = '%s_id' % (ansible_name)
                ans_data[ansible_id_name] = idoit_data[idoit_name]
            else:
                raise Exception('Unknown Type')
        if not self.idoit_spec['single_value_cat']:
            ans_data['id'] = idoit_data['id']
        return ans_data

    def run(self):
        self.cfg = json.loads(json.dumps(self.params['idoit']))
        self.idoit_cat_api = idoit_api.createApiCall(
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
        self.exit_json(**rtn)
