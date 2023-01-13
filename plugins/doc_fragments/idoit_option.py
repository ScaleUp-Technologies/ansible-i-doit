# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):

    DOCUMENTATION = r"""
options:
  idoit:
    type: dict
    description: i-doit credentials
    required: true
    suboptions:
      api_key:
        type: str
        description: The API Key for i-doit.
        required: true
      user:
        type: str
        description: The username to login in i-doit.
        required: true
      password:
        type: str
        description: The password for the user.
        required: true
      jrpc_url:
        type: str
        description: The Json RPC Url to i-doit.
        required: true
"""