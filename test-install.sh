#!/bin/bash
MYTMP=$(mktemp -d)

ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection install --force ${MYTMP}/*.tar.gz

ansible-playbook $*  test/test.yml