import requests

from library.api.exceptions import LiveDesignAPIException
from library.api.extended_ldclient.client import ExtendedLDClient
from library.api.urls import LDCLIENT_HOST


def get_api_client(username=None, password=None):
    """
    Get the ldclient for specified username and password

    :param username: str, Username for the ldclient
    :param password:str, password for the specified username
    """
    try:
        # Note: Any wrong input for either LDCLIENT_HOST or username or password throws HTTPError.
        client = ExtendedLDClient(host=LDCLIENT_HOST, username=username, password=password, compatibility_mode=(8, 10))
    except requests.exceptions.HTTPError as e:
        raise LiveDesignAPIException(
            "Unable to get LDClient object for Host:{}, username:{} and password:{}, Getting Error:{}".format(
                LDCLIENT_HOST, username, password, e), e)
    try:
        ping_return = client.ping()
        if ping_return:
            return client
        else:
            raise LiveDesignAPIException("ldclient ping returned False, It may not be able to hit the about path")
    except RuntimeError as e:
        raise LiveDesignAPIException("Ping returned error: {}".format(e), e)
