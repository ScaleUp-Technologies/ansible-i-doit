#!/bin/bash

set -e # exit on first error

MYTMP=$(mktemp -d)
python3 build.py
ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection install --force ${MYTMP}/*.tar.gz
rm -rf ${MYTMP}

ansible-playbook $*  test/test.yml
for file in plugins/modules/*.py ; do
    NAME="scaleuptechnologies.idoit.$(basename $file |cut -d '.' -f 1)"
    echo checkin ansible-doc ${NAME}
    ansible-doc -j "${NAME}" >/dev/null
done

#caleuptechnologies.idoit.idoit_cat_