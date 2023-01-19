#!/bin/bash

set -e # exit on first error
test -n $GALXY_TOKEN && echo 'Error: GALAXY_TOKEN is not set' ; exit 1
MYTMP=$(mktemp -d)
python3 build.py
ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection publish --token ${GALAXY_TOKEN} ${MYTMP}/*.tar.gz
rm -rf ${MYTMP}