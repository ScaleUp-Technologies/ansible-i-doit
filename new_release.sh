#!/bin/bash

if [ "$1" == "" ] ; then
    echo "Please sepcify a new version number" 1>&2
    exit 1
fi

VERSION=$1
GIT_STATUS=$(git status -s |grep -v new_release.sh)

if [ -n "${GIT_STATUS}" ] ; then
    echo "Please checkin all files" 1>&2
    exit 1
fi

if [ -z "${GALAXY_TOKEN}" ] ; then
    echo "Set GALAXY_TOKEN to upload" 1>&2
    exit 1
fi

set -e

sed -i -e "s/version: .*/version: $VERSION/" galaxy.yml
git commit -m 'New Version $VERSION' galaxy.yml
git tag v${VERSION}

MYTMP=$(mktemp -d)
ansible-galaxy collection build --output-path ${MYTMP}
ansible-galaxy collection publish --token ${GALAXY_TOKEN} ${MYTMP}/*.tar.gz
rm -rf ${MYTMP}
