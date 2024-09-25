#!/bin/bash

# test writers will use this script to create their virtualenv with ldclient installed

if [ -z "$1" ]; then
    echo "No directory specified to create python virtualenv."
    exit 1
fi

SELENIUM_ENV="$1"
rm -rf ${SELENIUM_ENV}
virtualenv -p python3 ${SELENIUM_ENV}
source ${SELENIUM_ENV}/bin/activate
pip install -r requirements.txt
pip install -e ../LD-WebServicesClient
