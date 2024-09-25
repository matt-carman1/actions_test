# ==============================================================================
# LEGACY ADMIN PANEL E2E TESTS
# ==============================================================================
# IMPORTANT: These tests are not up to standard with our best practices.
#            Please do not copy the test formats / development styles used here.
#
import pytest


@pytest.fixture(scope="function")
def selenium_class(request, selenium):
    """
    Set a class property on the invoking test context for legacy E2E tests

    :param request: request object with test metadata (from pytest fixture)
    :param selenium: selenium fixture

    TODO: We should migrate the admin tests to follow best practices
    """
    request.cls.selenium = selenium
