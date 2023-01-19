from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ansible.module_utils.basic import AnsibleModule
#import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from . import utils as idoit_utils
from pprint import pprint
from . import idoit_api
import json

class IdoitCategoryModule(AnsibleModule):
    def __init__(self, *args, idoit_spec):

        self.idoit_spec=idoit_spec
        if idoit_spec['single_value_cat']:
            state_choices=['present']
        else:
            state_choices=['absent','present']

        arg_spec=dict(
             idoit=idoit_utils.idoit_argument_spec,
             obj_id=dict(type="int", required=True),
            state=dict(choices=state_choices, default='present')
        )
        for idoit_name in idoit_spec['fields'].keys():
            field=idoit_spec['fields'][idoit_name]
            ansible_name=idoit_name
            if 'ansible_name' in field.keys():
                ansible_name=field['ansible_name']
            if field['type']=='str':
                arg_spec[ansible_name]=dict(type='str',default='')
            if field['type']=='dialog':
                arg_spec[ansible_name]=dict(type='str')
                arg_spec[ansible_name+'_id']=dict(type='int')
        super().__init__(*args, argument_spec=arg_spec, supports_check_mode=True)

    def run(self):
        # in cfg werden durch die Api noch Werte gecached, was bei Module.params nicht geht
        self.cfg=json.loads(json.dumps(self.params['idoit']))
        self.idoit_cat_api=idoit_api.createApiCall(self.cfg,self.idoit_spec['category'])
        old_idoit_data= self.idoit_cat_api.read_category(self.params['obj_id'])

        if self.params['state']=='present':
          self.present(old_idoit_data)
        else:
          # state absent
          self.absent(self.params['obj_id'], old_idoit_data)

    def absent(self, obj_id, old_idoit_data):
        result={}
        if old_idoit_data == None:
            result['changed']=False
        else:
            if self.check_mode:
                r='Not deleted, check_mode=true'
            else:
                r=self.idoit_cat_api.delete_category(obj_id, old_idoit_data['id'])
            result['changed']=True
            result['return']=r
        self.exit_json(**result)

    def present(self,  old_idoit_data):
        result=dict(
            changed=False
        )
        new_data={}
        idoit_new_data={}
        old_data={}
        for idoit_name in self.idoit_spec['fields'].keys():
            field=self.idoit_spec['fields'][idoit_name]
            ansible_name=idoit_name
            if 'ansible_name' in field.keys():
                ansible_name=field['ansible_name']
            if field['type']=='str':
                new_data[ansible_name]=self.params[ansible_name]
                idoit_new_data[idoit_name]=new_data[ansible_name]
                old_data[ansible_name]=old_idoit_data[idoit_name]
            if field['type']=='dialog':
                ansible_id_name='%s_id' % (ansible_name)
                old_data[ansible_id_name]=old_idoit_data[idoit_name]
                if self.params[ansible_name] is not None and self.params[ansible_id_name] is not None:
                    self.fail_json(msg='You can only specify %s or %s' % (ansible_name, ansible_id_name))
                if self.params[ansible_id_name] is not None:
                    new_data[ansible_id_name]=self.params[ansible_id_name]
                if self.params[ansible_name] is not None:
                    my_dialog_api=idoit_api.createApiDialogs(self.cfg, self.idoit_spec['category'],idoit_name)
                dialog_parent_id = None
                if 'dialog_parent' in field:
                    dialog_parent_field_name= '%s_id' % field['dialog_parent']
                    dialog_parent_id = new_data[dialog_parent_field_name]
                    if dialog_parent_id is None:
                        my_msg = 'You need to specify a %s or %s if you want to set %s' % (field['dialog_parent'], dialog_parent_field_name, ansible_name)
                        self.fail_json(msg=my_msg, **result)
                my_dialog_id = my_dialog_api.get(self.params[ansible_name], dialog_parent_id)
                if my_dialog_id is not None:
                    new_data[ansible_id_name] = my_dialog_id
                    idoit_new_data[idoit_name] = my_dialog_id
                elif self.check_mode :
                    result['changed'] = True
                    new_data[ansible_id_name] = -42
                else:
                    new_data[ansible_id_name] = my_dialog_api.create(self.params['ansible_name'], dialog_parent_id)
                    idoit_new_data[idoit_name] = new_data[ansible_id_name]


        #result['old_idoit_data']=old_idoit_data
        result['data']=new_data
        #result['new_idoit_data']= idoit_new_data
        #result['old_data']=old_data
        sanitized_before={}
        sanitized_after={}
        for key in new_data.keys():
            if key not in old_data.keys():
                result['changed'] = True
                sanitized_after[key]=new_data[key]
            elif new_data[key] != old_data[key]:
                result['changed'] = True
                sanitized_before[key]=old_data[key]
                sanitized_after[key]=new_data[key]
        for key in old_data.keys():
            if key not in new_data:
                result['changed'] = True
                sanitized_before[key]=old_data[key]
        if result['changed']:
            if self.check_mode:
                r='Not modified, check_mode=True'
            else:
                r=self.idoit_cat_api.update_category(self.params['obj_id'], idoit_new_data)
        result['return']=r
        if self._diff:
            result["diff"] = {
                "before": sanitized_before,
                "after": sanitized_after,
            }

        self.exit_json(**result)

class IdoitCategoryInfoModule(AnsibleModule):
    def __init__(self, *args, idoit_spec):
        self.idoit_spec=idoit_spec
        arg_spec=dict(
             idoit=idoit_utils.idoit_argument_spec,
             obj_id=dict(type="int", required=True),
        )
        super().__init__(*args, argument_spec=arg_spec, supports_check_mode=True)

    def run(self):
        self.cfg=json.loads(json.dumps(self.params['idoit']))
        self.idoit_cat_api=idoit_api.createApiCall(self.cfg,self.idoit_spec['category'])
        old_idoit_data= self.idoit_cat_api.read_category(self.params['obj_id'])
        old_data={}
        for idoit_name in self.idoit_spec['fields'].keys():
            field=self.idoit_spec['fields'][idoit_name]
            ansible_name=idoit_name
            if 'ansible_name' in field.keys():
                ansible_name=field['ansible_name']
            if field['type']=='str':
                old_data[ansible_name]=old_idoit_data[idoit_name]
            if field['type']=='dialog':
                ansible_id_name='%s_id' % (ansible_name)
                old_data[ansible_id_name]=old_idoit_data[idoit_name]
        rtn={'data':old_data}
        self.exit_json(**rtn)