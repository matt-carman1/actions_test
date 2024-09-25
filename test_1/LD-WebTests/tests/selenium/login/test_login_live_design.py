import pytest

from helpers.selection.authentication import LOGIN_ERROR_MSG, USER_NAME_ELEMENT
from helpers.verification.element import verify_is_visible
from library.authentication import do_login


@pytest.mark.smoke
@pytest.mark.parametrize("username, password", [("userC", "demo"), ("", ""), ("@test", "userC")])
def test_login_negative_case(selenium, username, password):
    """
    Test login with negative test data and validate the login functionality
    :param selenium: Selenium Webdriver
    """
    do_login(selenium, username, password)
    verify_is_visible(selenium, selector=LOGIN_ERROR_MSG, selector_text='Invalid username or password.')
