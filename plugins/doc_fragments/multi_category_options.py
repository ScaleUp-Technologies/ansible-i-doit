# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
  id:
    type: int
    description: i-doit category id to update
  search_by_fields:
    type: list
    description: field names to compare to find a category to update. Please note, Dialog-Fields can only searched by id.
"""
