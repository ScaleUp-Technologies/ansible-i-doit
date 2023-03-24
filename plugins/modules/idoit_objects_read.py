#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import idoit_scaleup
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idoit_objects_read
short_description: Read objects of a object type
description: |
  Search for objects of a object type
options:
    filter_by_object_type:
        description: Object Type Name
        required: true
    categories:
        description: Categories to return
        default: []
        type: list
        elements: str
author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
'''
EXAMPLES = r'''
- name: Search for all Layer2 Nets with VLAN info
  scaleuptechnologies.idoit.idoit_objects_read:
    idoit: "{{ idoit_access_test }}"
    filter_by_object_type: C__OBJTYPE__LAYER2_NET
    categories: C__CATS__LAYER2_NET
'''

RETURN = r'''
result:
    description: List of Results
    type: list
    returned: always
    sample:
      - categories:
        - C__CATS__LAYER2_NET:
            description: ""
            id: "336"
            ip_helper_addresses: []
            layer3_assignments:
            - id: 42
              name: hi
        cmdb_status: "6"
        cmdb_status_title: "in operation"
        created: "2023-01-31 11:37:45"
        id: "10623"
        status: "2"
        sysid: "SYSID_1675172088"
        title: "BER INT MANAGEMENT"
        type: "70"
        updated: "2023-01-31 11:46:42"
'''

import json

def run_module():
    arg_spec = dict(
        idoit=idoit_utils.idoit_argument_spec,
        filter_by_object_type=dict(type="str"),
        categories=dict(type='list',default=[], options=
            dict(type='str')
        )
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    cfg = json.loads(json.dumps(module.params['idoit']))
    if cfg['api_log']:
        idoit_scaleup.turn_on_api_logging()
    api_call = idoit_scaleup.createApiCall(
            cfg, module.params['filter_by_object_type'])
    search_result = api_call.get_all(module.params['categories'])
    result = {
        'changed': False,
        'result': search_result,
    }
    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
