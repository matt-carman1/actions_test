import pytest
from ldclient import LDClient
from requests import RequestException
from helpers.api.verification.general import verify_error_response
from helpers.api.verification.model import verify_expected_driver_names_exists_in_drivers_found, verify_expected_driver_name_exists_in_driver_found

# Logging in as userA
test_username = 'userA'
test_password = 'userA'


def test_get_and_verify_async_drivers(ld_api_client: LDClient):
    """
    Test to get drivers list and verify them.

    :param ld_api_client: LDClient, ldclient object
    """
    async_drivers = ld_api_client.async_drivers()
    expected_driver_names = ['sync', 'JS Test Async Driver']
    verify_expected_driver_names_exists_in_drivers_found(async_drivers, expected_driver_names)


def test_get_and_verify_async_driver(ld_api_client: LDClient):
    """
    Test to get driver by id and verify it.

    :param ld_api_client: LDClient, ldclient object
    """
    async_driver = ld_api_client.async_driver('1')
    expected_driver_name = 'sync'
    verify_expected_driver_name_exists_in_driver_found(async_driver, expected_driver_name)
