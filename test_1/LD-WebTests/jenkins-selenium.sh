#!/bin/bash

SELENIUM_ENV=selenium_env
BUILD_DIR=${JOB_NAME}-${BUILD_NUMBER}_${BUILD_ID}
SELENIUM_REPORT_DIR=selenium_reports-${BUILD_DIR}
export LD_SERVER=http://localhost:8080/

set -x

# Only using the latest Firefox driver as it is incompatible with Selenium 4. Old jenkins does not have
# latest Chrome browser so updating the chromedriver causes issues.
which geckodriver
export PATH=/mnt/jenkins/workspace/LD-WebTests/resources/webdrivers/geckodriver:${PATH}
which geckodriver
geckodriver --version
chromedriver --version
sudo cp /mnt/jenkins/workspace/LD-WebTests/resources/webdrivers/geckodriver /usr/local/bin/geckodriver

mkdir ${SELENIUM_REPORT_DIR}
rm -rf ${SELENIUM_ENV}
virtualenv -p python3 ${SELENIUM_ENV}
source ${SELENIUM_ENV}/bin/activate
pip install -r requirements.txt
pip install -e ../LD-WebServicesClient

../gradlew :livedesign-web-tests:html

python LD-WebTests_runner.py --browser Chrome --reruns=1
EXIT_CODE_1=$?
python LD-WebTests_runner.py --browser Firefox --reruns=1
EXIT_CODE_2=$?

# Fail if either of the test suites failed or the code is not formatted correctly
EXIT_CODE=$((${EXIT_CODE_1} || ${EXIT_CODE_2}))

mv *.html assets/ __pycache__/ ${SELENIUM_REPORT_DIR}
rm -rf ${SELENIUM_ENV}

exit ${EXIT_CODE}
