#!/bin/bash

cp -a $REPO ./build/

${PIP} install -r $REPO/
