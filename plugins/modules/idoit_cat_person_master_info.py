#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Scaleup Technologies
- Sven Anders (@tabacha)
description: Gets C__CATS__PERSON_MASTER category  values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
module: idoit_cat_person_master_info
options: {}
short_description: Get values from a person_master category to an object

'''

EXAMPLES = r'''
name: Search for a category for object 1320
scaleuptechnologies.idoit.idoit_cat_person_master_info:
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
category: C__CATS__PERSON_MASTER
fields:
  description:
    description: Description of the Power Consumer
    type: html
  first_name:
    description: First Name
    type: str
  function:
    description: Function
    type: str
  last_name:
    description: Last Name
    type: str
  mail:
    description: Mail
    type: str
  personnel_number:
    description: Personal Number
    type: str
  phone_company:
    description: Phone number in the office
    type: str
  phone_mobile:
    description: Mobile phone number
    type: str
  title:
    description: Title
    type: str
single_value_cat: true

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
