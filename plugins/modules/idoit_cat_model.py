#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: idoit_cat_model
short_description: Create or update a model category to an object
description: |
  Adds C__CATG__MODEL category to an object if not there or update values
options:
    manufacturer:
        description: Name of the manufacutrer, if not there it will be created.
        tpye: str
    manufacturer_id:
        description: Id of the manufacutrer
        tpye: int
    model:
        description: Name of the model, if not there it will be created.
        type: str
    model_id:
        description: Id of the model
        type: int
    product_id:
        description: Produkt-ID
        type: str
    service_tag:
        description: Service Tag
        type: str
    serial:
        description: Serial
        type: str
    firmware:
        description: Firmware
        type: str
    description:
        description: Description
        type: str
author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
    - scaleuptechnologies.idoit.category_options
'''
EXAMPLES = r'''
- name: Search for Server with name
  scaleuptechnologies.idoit.idoit_cat_model:
    idoit: "{{ idoit_access }}"
    manufacturer: Dell
    model: R430
    sevice_tag: FFH123T
    fimware: 1.20
'''

RETURN = r'''
api_result:
    description: Api Result
    type: list
    returned: always
    sample:
      - fixme: 42
'''

from ansible.module_utils.basic import AnsibleModule
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit_api as idoit_api
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit_api.consts as consts
from pprint import pprint
import json
IDOIT_SPEC={
  'category': consts.C__CATG__MODEL,
  'single_value_cat': True,
  'fields': {
      'productid': { 'ansible_name': 'product_id', 'type':'str'},
      'service_tag': { 'type':'str'},
      'serial': { 'type':'str'},
      'firmware': { 'type':'str'},
      'description': { 'type':'str'},
      'manufacturer': { 'type': 'dialog'},
      'title':{ 'type': 'dialog', 'ansible_name':'model', 'dialog_parent': 'manufacturer'}
    }
}
def run_module():

    if IDOIT_SPEC['single_value_cat']:
      state_choices=['present']
    else:
      state_choices=['absent','present']

    arg_spec=dict(
            idoit=idoit_utils.idoit_argument_spec,
            obj_id=dict(type="int", required=True),
            state=dict(choices=state_choices, default='present')
    )
    for idoit_name in IDOIT_SPEC['fields'].keys():
      field=IDOIT_SPEC['fields'][idoit_name]
      ansible_name=idoit_name
      if 'ansible_name' in field.keys():
        ansible_name=field['ansible_name']
      if field['type']=='str':
          arg_spec[ansible_name]=dict(type='str',default='')
      if field['type']=='dialog':
          arg_spec[ansible_name]=dict(type='str')
          arg_spec[ansible_name+'_id']=dict(type='int')

    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    params= module.params
    # in cfg werden durch die Api noch Werte gecached, was bei Module.params nicht geht
    cfg=json.loads(json.dumps(module.params['idoit']))
    idoit_apis=idoit_api.createApiCalls(cfg)

    old_idoit_data=idoit_apis[IDOIT_SPEC['category']].read_category(params['obj_id'])

    if params['state']=='present':
      present(idoit_apis[IDOIT_SPEC['category']], cfg, module, params, old_idoit_data)
    else:
      # state absent
      absent(idoit_apis[IDOIT_SPEC['category']],module, params['obj_id'], old_idoit_data)

def absent(idoit_cat_api, module, obj_id, old_idoit_data):
  result={}
  if old_idoit_data == None:
    result['changed']=False
    module.exit_json(**result)
  else:
    if module.check_mode:
      r='Not deleted, check_mode=true'
    else:
      r=idoit_cat_api.delete_category(obj_id, old_idoit_data['id'])
    result['changed']=True
    result['return']=r
    module.exit_json(**result)

def present(idoit_cat_api,cfg, module, params, old_idoit_data):
    result=dict(
      changed=False
    )
    new_data={}
    idoit_new_data={}
    old_data={}

    for idoit_name in IDOIT_SPEC['fields'].keys():
      field=IDOIT_SPEC['fields'][idoit_name]
      ansible_name=idoit_name
      if 'ansible_name' in field.keys():
        ansible_name=field['ansible_name']
      if field['type']=='str':
        new_data[ansible_name]=params[ansible_name]
        idoit_new_data[idoit_name]=new_data[ansible_name]
        old_data[ansible_name]=old_idoit_data[idoit_name]
      if field['type']=='dialog':
        ansible_id_name='%s_id' % (ansible_name)
        old_data[ansible_id_name]=old_idoit_data[idoit_name]
        if params[ansible_name] is not None and params[ansible_id_name] is not None:
          module.fail_json(msg='You can only specify %s or %s' % (ansible_name, ansible_id_name))
        if params[ansible_id_name] is not None:
          new_data[ansible_id_name]=params[ansible_id_name]
        if params[ansible_name] is not None:
          my_dialog_api=idoit_api.createApiDialogs(cfg,IDOIT_SPEC['category'],idoit_name)
          dialog_parent_id = None
          if 'dialog_parent' in field:
            dialog_parent_field_name= '%s_id' % field['dialog_parent']
            dialog_parent_id = new_data[dialog_parent_field_name]
            if dialog_parent_id is None:
              my_msg = 'You need to specify a %s or %s if you want to set %s' % (field['dialog_parent'], dialog_parent_field_name, ansible_name)
              module.fail_json(msg=my_msg, **result)
          my_dialog_id = my_dialog_api.get(params[ansible_name], dialog_parent_id)
          if my_dialog_id is not None:
            new_data[ansible_id_name] = my_dialog_id
            idoit_new_data[idoit_name] = my_dialog_id
          elif module.check_mode :
            result['changed'] = True
            new_data[ansible_id_name] = -42
          else:
            new_data[ansible_id_name] = my_dialog_api.create(params['ansible_name'], dialog_parent_id)
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
      if module.check_mode:
        r='Not modified, check_mode=True'
      else:
        r=idoit_cat_api.update_category(params['obj_id'], idoit_new_data)
      result['return']=r
    if module._diff:
      result["diff"] = {
        "before": sanitized_before,
        "after": sanitized_after,
      }

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
