#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import idoit_scaleup
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: idoit_condition_read
short_description: Search for a property in i-doit.
description: |
  Search for a property in i-doit.
options:
    query:
        description: what to query for
        type: list
        required: true
        elements: dict
        suboptions:
            category:
                type: str
                description: The category to search in
                required: true
            field:
                type: str
                description: The fieldname in the category
                required: true
            value:
                type: str
                description: What to search for
                required: true
            operator:
                type: str
                choices:
                    - AND
                    - OR
                description: The logic operator if you use 2 or more conditions, pt this to the 2nd and next elements


author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
'''
EXAMPLES = r'''
- name: Search for a Network
  scaleuptechnologies.idoit.idoit_condition_read:
    idoit: "{{ idoit_access_test }}"
    query:
      - category: C__CATS__NET
        field: address
        value: 10.23.23.0
      - category: C__CATS__NET
        field: netmask
        value: 255.255.255.0
        operator: AND
'''

RETURN = r'''
result:
    description: List of Results
    type: list
    returned: always
    sample:
      - cmdb_status: "6"
        cmdb_status_title: "in operation"
        created: "2023-01-31 11:37:45"
        id: "10623"
        status: "2"
        sysid: "SYSID_1675172088"
        title: "BER INT MANAGEMENT"
        type: "31"
        type_icon: "images/axialis/web-email/cloud-computer-filled.svg"
        type_title: "Layer 3-Net"
        updated: "2023-01-31 11:46:42"
'''

def run_module():
    arg_spec = dict(
        idoit=idoit_utils.idoit_argument_spec,
        query=dict(type='list',required=True, options=
            dict(type='dict', required=True, options=dict(
                category=dict(type="str", required=True),
                field=dict(type="str", required=True),
                value=dict(type="str", required=True),
                operator=dict(choices=['AND','OR'], default=None)
                )
            )
        )
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    api_call = idoit_scaleup.conditional_read(module.params['idoit'])
    for ele in module.params['query']:
        api_call.add_search_param(**ele)
    search_result = api_call.search()
    result = {
        'changed': False,
        'result': search_result,
    }
    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()
