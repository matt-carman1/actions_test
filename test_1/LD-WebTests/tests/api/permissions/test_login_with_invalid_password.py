import pytest

from helpers.api.verification.general import verify_error_response
from tests.conftest import get_api_client


@pytest.mark.parametrize('username,password', [('userA', 'invalidPassword'), ('invalidUser', 'invalidPassword')])
def test_login_with_invalid_credentials(username, password):
    """
    Test login with invalid password.
    1. Login with valid user and invalid password.
    2. Verify error message.
    """
    # ----- Login with valid username and invalid password ----- #
    with pytest.raises(Exception) as error_response:
        get_api_client(username=username, password=password)
    # ----- Verify Error message ----- #
    verify_error_response(error_response.value.error,
                          expected_status_code='401',
                          expected_error_message='401 Client Error: Unauthorized for url')
