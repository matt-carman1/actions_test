import pytest

import requests

from library.url_endpoints import HOST

LD_PROPERTIES = {'HIDE_COMPOUND_STRUCTURE_COLUMN': 'true'}


@pytest.mark.usefixtures('customized_server_config')
def test_customized_server_config():
    """
    Sanity check test to ensure that the customized_server_config is working fine.
    """
    headers = {"content-type": 'application/json'}

    # ----- Making sure that the flag is on via requests ----- #
    r = requests.post("{}livedesign/api/config/search".format(HOST),
                      auth=requests.auth.HTTPBasicAuth('demo', 'demo'),
                      headers=headers,
                      data='{"keys": ["HIDE_COMPOUND_STRUCTURE_COLUMN"]}').json()
    assert r.get('results') == [{'key': 'HIDE_COMPOUND_STRUCTURE_COLUMN',
                                 'value': 'true',
                                 'default_value': 'false',
                                 'supported_values': 'true or false',
                                 'description': "'true' if the Compound Structure column should be hidden",
                                 'category': 'CONFIGURATIONS',
                                 'sub_category': 'CUSTOM_WORKAROUNDS',
                                 'acl_level': 'USER',
                                 'managed_by': 'SA',
                                 'frontend': True,
                                 'requires_restart': False,
                                 'version_introduced': 'Before 9.0.1'}],\
        'Expected HIDE_COMPOUND_STRUCTURE_COLUMN flag to be true, but got unexpected response {}'.format(r)
