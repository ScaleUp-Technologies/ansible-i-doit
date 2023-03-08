#!/bin/bash

set -e # exit on first error

MYTMP=$(mktemp -d)
python3 build.py
ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection install --force ${MYTMP}/*.tar.gz
rm -rf ${MYTMP}

ansible-playbook $*  test/test.yml
for file in src/idoit/category/*.yml ; do
    NAME="scaleuptechnologies.idoit.idoit_cat_$(grep basename: $file |cut -d ' ' -f 2-)"
    echo checkin ansible-doc ${NAME}
    ansible-doc -j "${NAME}" >/dev/null
    ansible-doc -j "${NAME}_info" >/dev/null
done

#caleuptechnologies.idoit.idoit_cat_