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

from ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit import IdoitCategoryModule
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
    module = IdoitCategoryModule(
        idoit_spec=IDOIT_SPEC,
    )
    module.run()

def main():
    run_module()

if __name__ == '__main__':
    main()
