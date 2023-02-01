#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Scaleup Technologies
- Sven Anders (@tabacha)
description: Gets C__CATG__CONTROLLER category  values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
module: idoit_cat_controller_info
options: {}
short_description: Get values from a controller category to an object

'''

EXAMPLES = r'''
name: Search for a category for object 1320
scaleuptechnologies.idoit.idoit_cat_controller_info:
  idoit: '{{ idoit_access }}'
  obj_id: 1320

'''

RETURN = r'''
changed:
  description: Are there changes?
  returned: always
  type: bool
data:
  description: Data of the category
  returned: always
  type: complex

'''

IDOIT_SPEC = r'''
category: C__CATG__CONTROLLER
fields:
  description:
    description: Description of the Model
    type: str
  firmware:
    description: Firmware
    type: str
  manufacturer:
    description: Name of Manufactuerer of the device, if not there it will
      be created
    description_id: Id of Manufactuerer of the device
    type: dialog
  model:
    description: Model of the device, if not there it will be created
    description_id: Id of Model of the device
    type: dialog
  title:
    description: Title
    type: str
  type:
    description: Type of the Controller like ATA, SAS, SATA, USB
    description_id: Id of the type
    type: dialog
single_value_cat: false

'''

from ansible_collections.scaleuptechnologies.idoit.plugins.module_utils.idoit import IdoitCategoryInfoModule
import yaml


def run_module():
    module = IdoitCategoryInfoModule(
        idoit_spec=yaml.safe_load(IDOIT_SPEC),
    )
    module.run()


def main():
    run_module()


if __name__ == '__main__':
    main()
