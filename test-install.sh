#!/bin/bash

set -e # exit on first error

MYTMP=$(mktemp -d)
python3 build.py
ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection install --force ${MYTMP}/*.tar.gz
rm -rf ${MYTMP}

ansible-playbook $*  test/test.yml

