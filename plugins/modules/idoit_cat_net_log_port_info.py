#!/usr/bin/python

# Autogenerated by build.py DO NOT EDIT HERE

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
author:
- Scaleup Technologies
- Sven Anders (@tabacha)
description: Gets C__CATG__NETWORK_LOG_PORT category  values
extends_documentation_fragment:
- scaleuptechnologies.idoit.idoit_option
- scaleuptechnologies.idoit.category_options
module: idoit_cat_net_log_port_info
options: {}
short_description: Get values from a net_log_port category to an object

'''

EXAMPLES = r'''
name: Search for a category for object 1320
scaleuptechnologies.idoit.idoit_cat_net_log_port_info:
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
category: C__CATG__NETWORK_LOG_PORT
fields:
  active:
    default: true
    description: Active
    type: bool
  addresses:
    description: Ids of the Adress Object-id
    element_type: int
    type: list
  description:
    description: Description of the Model
    type: html
  mac:
    description: MAC-address
    type: str
  net:
    ansible_name: layer2_net
    description: Id of Layer2 Network (if VLAN)
    element_type: int
    type: list
  parent:
    description: Parent
    type: int
  port_type:
    description: Type
    description_id: Id of the port_type
    type: dialog
  ports:
    ansible_name: port_ids
    description: Id of the physical port
    element_type: int
    type: list
  standard:
    description: Standard
    description_id: Id of Strandard
    type: dialog
  title:
    description: Title
    type: str
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
