#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Sven Anders (during work by ScaleUp Technologies) (@tabacha)
description: Adds C__CATG__CPU category to an object if not there or update
  values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
- scaleuptechnologies.idoit.multi_category_options
module: idoit_cat_cpu
options:
  cores:
    description: Number of CPU cores
    type: int
  description:
    description: Description of the CPU
    type: str
  frequency:
    description: CPU-Frequency
    type: float
  frequency_unit:
    description: Unit of the frequency (KHz,MHz,GHz,THz)
    type: str
  frequency_unit_id:
    description: Id of the frequency
    type: int
  manufacturer:
    description: Name of Manufactuerer of the device, if not there it will
      be created
    type: str
  manufacturer_id:
    description: Id of Manufactuerer of the device
    type: int
  title:
    description: Title
    type: str
  type:
    description: CPU Type of the device, if not there it will be created
    type: str
  type_id:
    description: Id of Type of the device
    type: int
short_description: Create or update a cpu category to an object

'''

EXAMPLES = r'''
- name: Set a new CPU
  scaleuptechnologies.idoit.idoit_cat_cpu:
    cores: 8
    frequency: 2300
    frequency_unit: MHz
    id: 2
    idoit: '{{ idoit_access }}'
    manufacturer: Intel
    obj_id: 1320
    title: Intel(R) Core(TM) i7-10510U CPU @ 1.80GHz
    type: Core I7

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
category: C__CATG__CPU
fields:
  cores:
    description: Number of CPU cores
    type: int
  description:
    description: Description of the CPU
    type: html
  frequency:
    description: CPU-Frequency
    type: float
  frequency_unit:
    description: Unit of the frequency (KHz,MHz,GHz,THz)
    description_id: Id of the frequency
    type: dialog
  manufacturer:
    description: Name of Manufactuerer of the device, if not there it will
      be created
    description_id: Id of Manufactuerer of the device
    type: dialog
  title:
    description: Title
    type: str
  type:
    description: CPU Type of the device, if not there it will be created
    description_id: Id of Type of the device
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
