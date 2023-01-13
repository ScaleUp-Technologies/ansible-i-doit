#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: idoit_search
short_description: Fulltext search in i-doit.
description: Fulltext search in i-doit.
options:
    idoit:
        description: Idoit Json rpc url and credentials
        tpye: dict
        required: true
    search:
        description: String to seach for
        tpye: str
        required: true
author:
    - Sven Anders (@tabacha)
'''
EXAMPLES = r'''
- name: Search for Server with name
  scaleuptechnologies.idoit.idoit_search:
    idoit: "{{ idoit_access }}"
    search: "ceph004.occ1.ham1.int.yco.de"
'''

RETURN = r'''
result:
    description: List of Results
    type: list
    returned: always
    sample:
      - documentId: 3024
        key: "Server > General > Title"
        link: "/?objID=3024&catgID=1&cateID=3024&highlight=ceph004.occ1.ham1.int.yco.de"
        score: 100
        status: Normal
        type: cmdb
        value: ceph004.occ1.ham1.int.yco.de
'''
RETURN2 = r'''
result:
  - documentId: 3024
    key: "Server > General > Title"
    link: "/?objID=3024&catgID=1&cateID=3024&highlight=ceph004.occ1.ham1.int.yco.de"
    score: 100
    status: Normal
    type: cmdb
    value: ceph004.occ1.ham1.int.yco.de
'''

from ansible.module_utils.basic import AnsibleModule
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit_api as idoit_api
#  see https://kb.i-doit.com/display/en/Search
#  or https://kb.i-doit.com/display/de/API+Methoden idoit.search

def main():
    arg_spec=dict(
            idoit=idoit_utils.idoit_argument_spec,
            search=dict(type="str", required=True),
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    idoit_search=idoit_api.search(module.params['idoit'])
    result=idoit_search.search(module.params['search'])
    result['changed']=False
    module.exit_json(**result)

if __name__ == '__main__':
    main()

