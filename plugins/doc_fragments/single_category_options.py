# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SingleDocFragment(object):

    DOCUMENTATION = r"""
options:
  state:
    choices: ['present', 'merge']
    decription: State of the category
    default: present
"""
