#!/bin/bash

current=`pwd`
mkdir -p /tmp/prSHARK/
cp * /tmp/prSHARK/
cp -R ../prSHARK /tmp/prSHARK/
cp ../setup.py /tmp/prSHARK/
cp ../smartshark_plugin.py /tmp/prSHARK/
cd /tmp/prSHARK/

tar -cvf "$current/prSHARK_plugin.tar" --exclude=*.tar --exclude=build_plugin.sh --exclude=*/tests --exclude=*/__pycache__ --exclude=*.pyc *
