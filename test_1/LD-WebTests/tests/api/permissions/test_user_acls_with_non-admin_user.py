import pytest
from requests import RequestException

from helpers.api.extraction.user import get_users_list
from helpers.api.verification.general import verify_error_response

test_username = 'userB'
test_password = 'userB'


def test_list_users_with_non_admin(ld_api_client):
    """
    Test whether list_users give error message when login with non-admin user

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(RequestException) as error_response:
        get_users_list(ld_api_client)

    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')

    with pytest.raises(RequestException) as error_response:
        get_users_list(ld_api_client, include_permissions=True)

    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')


def test_get_user_with_non_admin(ld_api_client):
    """
    Test get_user give error message when login with non-admin user.

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(RequestException) as error_response:
        ld_api_client.get_user('userC')

    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')


def test_list_memberships_with_non_admin(ld_api_client):
    """
    Test get_user give error message when login with non-admin user.

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(RequestException) as error_response:
        ld_api_client.list_memberships()

    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')


def test_list_permissions_with_non_admin(ld_api_client):
    """
    Test get_user give error message when login with non-admin user.

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(RequestException) as error_response:
        ld_api_client.list_permissions()

    verify_error_response(error_response.value, expected_status_code='403', expected_error_message='Permission denied')
