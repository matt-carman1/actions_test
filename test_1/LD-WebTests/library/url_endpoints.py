import os
from urllib.parse import urljoin

from library import selenium_jenkins

# TODO Extract this to a config file
HOST = os.getenv('LD_SERVER', '').strip()
if HOST:
    if not HOST.startswith('http'):
        raise ValueError('LD_SERVER must include protocol, i.e. it should start with http:// for local developer '
                         'environments and nodes on jenkins server, and spinner machines (hopefully also everything '
                         'else) are https://')
    print('Using HOST from LD_SERVER env param')
else:
    print('Getting HOST from Jenkins...')
    HOST = selenium_jenkins.get_host()
    print('')

LIVE_DESIGN_URL = urljoin(HOST, 'livedesign/')
LOGIN_URL = urljoin(HOST, 'livedesign/static/login.html')
print('HOST: {}'.format(HOST))

# Get the admin url from the env if set, or fallback on the default
# If you're using the ADMIN_SERVER env variable, be sure to include
# the URL_PATH_PREFIX if necessary

# Note (williams): Keep in sync with runserver command  in Makefile
ADMIN_URL = os.environ.get('ADMIN_SERVER', HOST + 'admin/').strip()
ADMIN_LOGIN_URL = ADMIN_URL + 'login/'
ADMIN_LD_PROPERTY_URL = 'ldproperties/ldproperty/'
ADMIN_COVERPAGE_URL = 'coverpage/coverpage/'
ADMIN_ASYNCDRIVER_URL = 'asyncdrivers/asyncdriver/'
OLD_ADMIN_ASYNCDRIVER_URL = 'models/asyncdriver/'
ADMIN_PROTOCOL_URL = 'models/protocol/'
ADMIN_LDMODEL_URL = 'models/ldmodel/'

LDCLIENT_CONFIG_SEARCH = urljoin(HOST, 'livedesign/api/config/search')
COPYRIGHT_URL = urljoin(HOST, 'livedesign/static/resources/licenses/version_license.txt')
