#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Sven Anders (during work by ScaleUp Technologies) (@tabacha)
description: Adds C__CATS__NET category to an object if not there or update
  values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
- scaleuptechnologies.idoit.single_category_options
module: idoit_cat_layer3_net
options:
  address:
    description: Address
    type: str
  cidr_suffix:
    description: Netmask Suffix
    type: int
  description:
    description: Description of the Layer2 Net
    type: str
  type:
    description: Type
    type: str
  type_id:
    description: Id of Type
    type: int
short_description: Create or update a layer3_net category to an object

'''

EXAMPLES = r'''
- name: Create a new Net
  scaleuptechnologies.idoit.idoit_cat_layer3_net:
    address: 10.0.10.0
    cidr_suffix": 24
    idoit: '{{ idoit_access }}'
    obj_id: 1320
    type: 1

'''

RETURN = r'''
changed:
  description: Are there changes?
  returned: always
  type: bool
data:
  description: New data
  sample:
    description: ''
    firmware: ''
    manufacturer_id: 5
    model_id: 22
    product_id: ''
    serial: Test 42
    service_tag: CZJ037040C
  type: complex
id:
  description: Category Id of the saved category
  type: int
return:
  description: I-Doit API Result
  type: complex

'''

IDOIT_SPEC = r'''
category: C__CATS__NET
fields:
  address:
    description: Address
    type: str
  cidr_suffix:
    description: Netmask Suffix
    type: int
  description:
    description: Description of the Layer2 Net
    type: html
  type:
    description: Typ
    description_id: Id of Typ
    type: dialog
single_value_cat: true

'''

from ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit import IdoitCategoryModule
import yaml


def run_module():
    module = IdoitCategoryModule(
        idoit_spec=yaml.safe_load(IDOIT_SPEC),
    )
    module.run()


def main():
    run_module()


if __name__ == '__main__':
    main()