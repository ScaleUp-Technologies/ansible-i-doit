#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
import idoit_scaleup
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.utils as idoit_utils
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type


DOCUMENTATION = r'''
---
module: idoit_search
short_description: Fulltext search in i-doit.
description: |
  Fulltext search in i-doit.
  see https://kb.i-doit.com/display/en/Search
  or https://kb.i-doit.com/display/de/API+Methoden idoit.search
options:
    search:
        description: String to seach for
        type: str
        required: true
    only_exact_match:
        description: Filter all results which are not exact the searchsting.
        type: bool
    only_key:
        description: Filter all results which are not exact this key.
        type: str
author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
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


def run_module():
    arg_spec = dict(
        idoit=idoit_utils.idoit_argument_spec,
        search=dict(type="str", required=True),
        only_exact_match=dict(type="bool", default=False),
        only_key=dict(type="str", default=None)
    )
    module = AnsibleModule(
        argument_spec=arg_spec,
        supports_check_mode=True,
    )
    idoit_search = idoit_scaleup.search(module.params['idoit'])
    search_result = idoit_search.search(module.params['search'])
    result = {
        'changed': False,
        'result': [],
        'only_key': (module.params['only_key'])
    }
    for ele in search_result:
        add = False
        if module.params['only_exact_match'] is False:
            # value wird bei manchen Felder der Titel des Objekts mit ": " vorgefuegt
            val = ele['value']
            if ": " in val:
                val = ": ".join(val.split(': ')[1:])
            add = (val == module.params['search'])
        else:
            add = True
        if (module.params['only_key'] is not None) and ele['key'] != module.params['only_key']:
            add = False
        if add:
            result['result'].append(ele)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
