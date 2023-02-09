#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Sven Anders (during work by ScaleUp Technologies) (@tabacha)
description: Adds C__CATG__MEMORY category to an object if not there or
  update values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
- scaleuptechnologies.idoit.multi_category_options
module: idoit_cat_memory
options:
  capacity:
    description: Size of the RAM in unit
    type: float
  description:
    description: Description of the Memory Module
    type: str
  manufacturer:
    description: Name of Manufactuerer of the device, if not there it will
      be created
    type: str
  manufacturer_id:
    description: Id of Manufactuerer of the device
    type: int
  title:
    description: Something like MemoryStick, Flash, DDRAM, SDRAM, ..
    type: str
  title_id:
    description: Id of title
    type: int
  type:
    description: Type of the RAM like DDR, DDR2, DDR3
    type: str
  type_id:
    description: Id of the type
    type: int
  unit:
    description: Unit of the capacity (B,KB,MB,GB,TB)
    type: str
  unit_id:
    description: Id of Capacity Unit
    type: int
short_description: Create or update a memory category to an object

'''

EXAMPLES = r'''
- name: Set a new Memory Module
  scaleuptechnologies.idoit.idoit_cat_model:
    capacity: 8388608
    description: DIMM.Socket.A1 M393B1G70BH0-YK0 131A13D9
    id: 2
    idoit: '{{ idoit_access }}'
    manufacturer: Samsung
    obj_id: 1320
    title: SDRAM
    unit: KB

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
category: C__CATG__MEMORY
fields:
  capacity:
    description: Size of the RAM in unit
    type: float
  description:
    description: Description of the Memory Module
    type: html
  manufacturer:
    description: Name of Manufactuerer of the device, if not there it will
      be created
    description_id: Id of Manufactuerer of the device
    type: dialog
  title:
    description: Something like MemoryStick, Flash, DDRAM, SDRAM, ..
    description_id: Id of title
    type: dialog
  type:
    description: Type of the RAM like DDR, DDR2, DDR3
    description_id: Id of the type
    type: dialog
  unit:
    description: Unit of the capacity (B,KB,MB,GB,TB)
    description_id: Id of Capacity Unit
    type: dialog
single_value_cat: false

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
