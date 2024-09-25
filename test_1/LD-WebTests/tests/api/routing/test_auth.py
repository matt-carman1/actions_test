import os
from urllib.parse import urljoin

import pytest
import requests

from library.url_endpoints import HOST, LOGIN_URL
from library.utils import is_k8s


@pytest.mark.parametrize("auth", [
    None,
    requests.auth.HTTPBasicAuth("demo", "badpassword"),
])
def test_api_401_page(auth):
    url = urljoin(HOST, "/livedesign/api/about")
    resp = requests.get(url, auth=auth)
    assert resp.status_code == 401, '\n'.join([
        "accessing an API endpoint with invalid auth did not result in a 401",
        "Response Headers:",
        str(resp.headers),
        "Response text:",
        resp.text,
    ])
    assert 'please log in' in resp.text


def get_auth_locked_paths():
    """
    Return a list of URL paths that require authentication to access.
    """
    paths = [
        "/",
        "/livedesign",
        "/livedesign/",
        "/livedesign/index.html",
    ]
    if is_k8s():
        # Documentation routes are only served and therefore auth-protected in
        # k8s and NewJenkins.
        # LD_K8S_DIR is chosen as an arbitrary env var set by the NewJenkins
        # pipeline, and 'k8s.dev.bb.schrodinger.com' should be the suffix of
        # most dev k8s instances.
        # In "oldjenkins" and localhost setups, the doc routes are not served
        # by NGINX so shouldn't be tested against.
        paths.extend([
            "/livedesign/documentation",
            "/livedesign/documentation/livedesign_home.html",
        ])
    return paths


@pytest.mark.parametrize("path", get_auth_locked_paths())
def test_auth_redirect(path):
    url = urljoin(HOST, path)
    resp = requests.get(url)
    assert resp.url.startswith(LOGIN_URL), "accessing auth-locked route without auth should redirect to login page"
