import pytest
from urllib.parse import urljoin
from library.url_endpoints import HOST
import requests


def test_get_ldclient_docs(ld_api_client):
    url = urljoin(HOST, "/livedesign/ldclient")
    resp = requests.get(url)
    assert resp.status_code == 200, '\n'.join([
        "Could not get the statically served ldclient documentation at /livedesign/ldclient",
        "Response Headers:",
        str(resp.headers),
        "Response text:",
        resp.text,
    ])
