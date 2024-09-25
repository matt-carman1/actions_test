"""
Testing validation and restrictions working as expected with Service Tokens
"""
import os
from tempfile import NamedTemporaryFile

import pytest
from ldclient import LDClient
from library.url_endpoints import HOST
from requests.exceptions import HTTPError

# GOOD_TOKEN has expiration set to 2200-01-01, so it should not expire very soon.
GOOD_TOKEN = 's3LshWtOGoEQuiLhwkmk49/bevct+2rHF/p4ioptlk0rJM3ZCT/1RdcaQCnc4XQQkzm4TLSMjbjAhku/CP2jJzMOTr9rfEunVC16nm0r89lNaGYruTNNGhsVCFdgxdEubeaVEyi2rrKU27tv3s9XoAw6ArNwMrOwhVo5zz6ILuEKcDgT/PfDDBwUyWNV2nv6nqRnsBvi69hXPzDAQXJRGejp5boAjoQmVP6TaOFLevySmviTT3NmpzvZkw6sMDmh0etxDu2Ajk4KnveI/iplrLbhiFpBMmHYOcAyCKCMpxDWk8O/0n+N4ues/quRaTvxRAc8hjrzrmkU+GSjgCdeOA=='

BAD_TOKEN = 'not a valid token'

EXPIRED_TOKEN = 'KqO5t6Fw+wxdgN3XZyzuvqtKtI4XaurdN729bqpEwX5Khar531NGjQShtpZ9QIZVWhh+qWoz6jvnWvX55l+63krR5HwcUu9NDrQQwALVWLpNozAJna/C4ZN5KUn6bhVW0bmf7vDqusK38rNNrS3P4Y0l/Ys+Erll20+vzyHsyoFF2GoBUV3lBCzfbvfcqV+ivePDNnBXR9bI2Tf+Aw1+ynaeOzYibJaA6/NWzTHbKFTZ1jdgXnBk9QGWuUgTQDkMkBBiD3uqqKMJqyr61Tv9moHN0ApGt7MMXR7P+rotzHIXWMFKsMhoVaxRrOHb/qL7hHsCJsTDB5qjRtWmGFmCjQ=='


@pytest.mark.skip
def test_write_access_service_token():
    """
    test create attachment endpoint with valid auth token
    """
    print(create_attachment(GOOD_TOKEN))


def test_write_access_bad_token():
    """
    test create attachment endpoint with bad token
    """
    with pytest.raises(HTTPError, match=r'^401 '):
        create_attachment(BAD_TOKEN)


def test_expired_token():
    """
    test create attachment endpoint with expired token
    """
    with pytest.raises(HTTPError, match=r'^401 '):
        create_attachment(EXPIRED_TOKEN)


@pytest.mark.skip
def test_endpoints_token():
    """
    test live report additional rows using valid token
    """
    client = get_ldclient(GOOD_TOKEN)
    rows = client.live_report_rows('1548')
    assert (len(rows) == 2)


def test_endpoints_bad_token():
    """
    test live report additional rows using bad token
    """
    with pytest.raises(HTTPError, match=r'^401 '):
        client = get_ldclient(BAD_TOKEN)
        client.live_report_rows('1548')


def create_attachment(token):
    """
    create an attachment using api and a dummy file
    """
    client = get_ldclient(token)
    with NamedTemporaryFile(delete=False) as f:
        f.write(b"whatever")
    try:
        client.get_or_create_attachment(f.name, 'ATTACHMENT', [0])
    finally:
        os.unlink(f.name)


def get_ldclient(token):
    """
    initialize api
    """
    ldclient_host = "{}livedesign/api/".format(HOST)
    return LDClient(host=ldclient_host, token=token, compatibility_mode=(8, 10))
