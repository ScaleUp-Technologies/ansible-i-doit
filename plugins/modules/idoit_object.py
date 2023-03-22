#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import idoit_scaleup
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idoit_object
short_description: Create a object of a object type
description: |
  Search for objects of a object type
options:
    type:
        description: Object Type
        required: true
        type: str
    title:
        description: Title
        required: true
        type: str
author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
'''
XAMPLES = r'''
- name: Search for all Layer2 Nets with VLAN info
  scaleuptechnologies.idoit.idoit_object:
    idoit: "{{ idoit_access_test }}"
    type: C__OBJTYPE__LAYER2_NET
    title: "DMZ Customer 70123 [47]"
'''

RETURN = r'''
id:
    description: Object Id of the object
    type: int
    returned: always
    sample: 42
sys_id:
    description: Sys Id of the object
    type: str
    returned: always
    sample: VLAN_42
'''

import json

def run_module():
    arg_spec = dict(
        idoit=idoit_utils.idoit_argument_spec,
        title=dict(type="str"),
        type=dict(type="str"),
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    cfg = json.loads(json.dumps(module.params['idoit']))
    if cfg['api_log']:
        idoit_scaleup.turn_on_api_logging()
    api_call = idoit_scaleup.createApiCall(
            cfg, module.params['type'])
    search_result = api_call.get_by_title(module.params['title'])
    if search_result == None:
        if module.check_mode:
            result = {
                'changed': True,
                'result': 'not_created_check_mode'
            }
        else:
            create_result=api_call.create_object_with_title(module.params['title'])
            search_result = api_call.get_by_title(module.params['title'])
            result = {
                'changed': True,
                'result': search_result,
            }
    else:
        result = {
            'changed': False,
            'result': search_result,
        }
    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
