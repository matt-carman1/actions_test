from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException

from library import dom
from library.dom import DEFAULT_TIMEOUT

__doc__ = """

This is an experiment that attempts to solve the problem of using a dom.wait_*
method immediately followed by an assertion. In many cases, the wait method will
fail with a timeout error and the following assertion that describes the case
will never be called.

For example, instead of

    actual_value = dom.wait_until_something()  # This will timeout on failure
    assert expected_value == actual_value  # this will always pass

you can write

    assert eventually_equal(
        driver,
        lambda driver: logic_that_will_be_called_many_times(driver),
        expected_return_value
    ), 'Widget should go bonk'

This should provide a nice error message, and makes clear the intention of the
statement.

TODO: improve error message. SS-22898
"""


def eventually_equal(driver, test_callback, expected_value, timeout=DEFAULT_TIMEOUT):
    # (mulvaney) hack because selenium webdriver wait until function ignores
    # zero, '0 Compounds' or [] as a valid result
    if expected_value in (0, '0 Compounds', [], set()):
        the_number_zero = 'the_number_zero'

        # Override the expected value with a truthy equivalent
        expected_value = the_number_zero

        # Override the callback with one that substitutes a return value of '0'
        # for the truthy equivalent
        _test_callback = lambda _driver: the_number_zero \
            if test_callback(_driver) in (0, '0 Compounds', [], set()) \
            else False
    else:
        _test_callback = test_callback

    def equality_test(found_value):
        return found_value == expected_value

    return eventually(driver, _test_callback, equality_test, timeout)


def eventually(driver, test_callback, comparator_callback, timeout=DEFAULT_TIMEOUT, negate=False):
    """
    NOTE: Lower-level function. Instead, call a specific one, such as
    eventually_equal or eventually_visible.


    Return True if the result of test_callback causes comparator_callback to
    return True.

    test_callback is called periodically with the webdriver as a parameter,
    until the timeout value is exceeded.

    comparator_callback is invoked every time test_callback returns.

    NOTE: Lower-level function. In general you should call a specific one, such
    as eventually_equal or eventually_visible.


    :param driver: selenium webdriver
    :param test_callback: a function that accepts driver as a parameter
    :param comparator_callback: a function that accepts the result of calling
                                test_callback, and returns a Bool
    :param timeout:
    :param negate:
    :return:
    """
    verifier = _EventualVerifier(test_callback, comparator_callback)
    try:
        if negate:
            dom.wait_until_not(driver, verifier, timeout)
        else:
            dom.wait_until(driver, verifier, timeout)
        return True
    except (TimeoutException, StaleElementReferenceException):
        if verifier.last_found_content is not None:
            print('\nLast found content: {}\n'.format(verifier.last_found_content))
        return False


class _EventualVerifier:
    """
    The verifier used by _eventually
    """

    def __init__(self, test_callback, comparator_callback):
        self.test_callback = test_callback
        self.comparator_callback = comparator_callback
        self.last_found_content = None

    def __call__(self, driver):
        self.last_found_content = self.test_callback(driver)
        return self.last_found_content if self.comparator_callback(self.last_found_content) else False
