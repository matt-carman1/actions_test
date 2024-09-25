from functools import wraps

from selenium.webdriver.common.by import By

from library import dom


def within_iframe(iframe_selector, selector_type=By.CSS_SELECTOR):
    """
    Decorator that switches webdriver context to the iframe specified by the
    selector, and then switches back again when the function either returns or
    raises an exception (which is reraised).

    Important: The decorated function must have a named argument 'driver' or the
    webdriver must be the first argument.

    :param iframe_selector: selector string to get the iframe of interest
    :param selector_type: selector type. Default is CSS.
    :return: decorated function
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            driver = kwargs.get('driver') or args[0]
            iframe = dom.get_element(driver, iframe_selector, selector_type=selector_type)
            driver.switch_to.frame(iframe)
            try:
                result = f(*args, **kwargs)
            finally:
                driver.switch_to.default_content()
            return result

        return decorated_function

    return decorator
