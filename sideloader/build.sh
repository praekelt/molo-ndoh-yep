#!/bin/bash

cp -a $REPO ./build/

# for some odd reason South has ended up on the workspace
${PIP} uninstall South -y

${PIP} install -r $REPO/requirements.txt
