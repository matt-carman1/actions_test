#!/bin/bash

API_ENV=api_env
BUILD_DIR=${JOB_NAME}-${BUILD_NUMBER}_${BUILD_ID}
export LD_SERVER=http://localhost:8080/

set -x

rm -rf ${API_ENV}
virtualenv -p python3 ${API_ENV}
source ${API_ENV}/bin/activate
pip install -r requirements.txt
pip install -e ../LD-WebServicesClient

python LD-APITests_runner.py --reruns=1 --repeat=${1:-1}
EXIT_CODE=$?

rm -rf ${API_ENV}

exit ${EXIT_CODE}
