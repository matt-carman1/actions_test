import pytest
from requests import HTTPError

from helpers.api.verification.general import verify_error_response

# credentials for user with 'User' role
test_username = 'userA'
test_password = 'userA'

test_protocol_name = 'Protocol'


def test_check_user_with_user_role_dont_have_access_to_create_protocol(ld_api_client, create_model_or_protocol_object):
    """
    Test check user with 'User' role don't have access to create protocol using create_protocol method

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(HTTPError) as err_response:
        ld_api_client.create_protocol(create_model_or_protocol_object)
    verify_error_response(err_response.value, '403', 'Permission denied')


def test_check_user_with_user_role_dont_have_access_to_update_protocol(ld_api_client):
    """
    Test check user with 'User' role don't have access to update protocol using update_protocol method

    :param ld_api_client: LDClient, ldclient object
    """
    with pytest.raises(HTTPError) as err_response:
        protocol = ld_api_client.get_protocol_by_id('4004')
        ld_api_client.update_protocol(protocol.id, protocol)
    verify_error_response(err_response.value, '403', 'Permission denied')
