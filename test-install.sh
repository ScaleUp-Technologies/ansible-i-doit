#!/bin/bash
MYTMP=$(mktemp -d)
export IDOIT_KEY IDOIT_USER IDOIT_PASS IDOIT_JURL

ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection install --force ${MYTMP}/*.tar.gz

ansible-playbook $*  test/test.yml