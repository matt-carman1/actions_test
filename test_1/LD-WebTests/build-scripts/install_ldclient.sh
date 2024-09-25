#!/bin/bash

# Install LDClient from host server set w/ LD_SERVER environment variable
# Retries on failure 60 times

for i in {1..60}; do
    error=0
    pip install ${LD_SERVER}livedesign/ldclient.tar.gz && break || error=$?
    echo "LDClient install failed, sleeping and retrying.."
    sleep 1
done
