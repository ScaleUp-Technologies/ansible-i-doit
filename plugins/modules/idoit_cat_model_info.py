#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: idoit_cat_model_info
short_description: Get values from a model category of an object
description: Get values from a model category of an object
options:
author:
    - Sven Anders (@tabacha)
extends_documentation_fragment:
    - scaleuptechnologies.idoit.idoit_option
    - scaleuptechnologies.idoit.category_options
'''
EXAMPLES = r'''
- name: Search for Server with name
  scaleuptechnologies.idoit.idoit_cat_model_info:
    idoit: "{{ idoit_access }}"
    obj_id: 1320
'''

RETURN = r'''
api_result:
    description: Api Result
    type: list
    returned: always
    sample:
      - fixme: 42
'''

from ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit import IdoitCategoryInfoModule
import ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit_api.consts as consts
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
    module = IdoitCategoryInfoModule(
        idoit_spec=IDOIT_SPEC,
    )
    module.run()

def main():
    run_module()

if __name__ == '__main__':
    main()
