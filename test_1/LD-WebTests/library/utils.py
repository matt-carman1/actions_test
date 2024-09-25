import os
import re
from random import randint

from selenium.common.exceptions import TimeoutException

from library.url_endpoints import HOST


def make_unique_name(name):
    """
    Append a random 8-digit number to the end of the given string to make it
    almost certainly unique.

    :param name:
    :return: The appended string.
    """
    return name + '_' + ('%08d' % randint(0, 99999999))


def request_animation_frame(driver):
    """
    Wait for the browser to redraw before returning.

    :param driver: selenium webdriver
    :return: None
    """
    # Let the browser redraw
    try:
        driver.execute_async_script("""
            done = arguments[0];
            window.requestAnimationFrame(function(){ done(); });
        """)
    except TimeoutException:
        pass


def first_element_containing_text(elements, text):
    """
    Get the first element from a list that contains a specified substring

    :param elements: a list of elements
    :param text: the text to look for
    :return: the element, or False if the list is empty or no elements contain
    the text
    """
    return next((element for element in elements if text in element.text), False)


def get_driver_from_element(driver_or_parent_element):
    """
    Iterate through the parents of the element until we reach the webdriver.

    Why?? It's idiomatic to call functions in dom and simulate with an element
    in place of the driver because it enables us to do selection within a
    tighter scope.  However, functionality, for example invoking a javascript
    script, must be called on the driver itself. This method gets the driver
    from the element's parent attribute

    :param driver_or_parent_element:
    :return:
    """
    while not hasattr(driver_or_parent_element, 'wc3') and hasattr(driver_or_parent_element, 'parent'):
        driver_or_parent_element = driver_or_parent_element.parent

    return driver_or_parent_element


def get_first_int(string):
    """
    Get the first positive integer from a given string.

    For example:
    utils.get_first_int('(5 Hidden)') # returns 5
    utils.get_first_int('hello123abc456') # returns 123
    utils.get_first_int('-5345') # returns 5345

    :param string:
    :return int:
    """
    return int(re.compile(r'\d+').search(string).group())


def element_is_vertically_within_parent(parent_element, child_element):
    """
    Is the child element located entirely within the parent elements y and y+height?

    :param parent_element: parent element
    :param child_element: child element that should be entirely within parent
    :return bool: True if child element is within parent.
    """
    y_lower_bound = parent_element.location['y']
    y_upper_bound = parent_element.location['y'] + parent_element.size['height']

    child_y = child_element.location['y']
    child_height = child_element.size['height']

    return child_y >= y_lower_bound and child_y + child_height <= y_upper_bound


def element_is_horizontally_within_parent(parent_element, child_element):
    """
    Is the child element located entirely between the parent elements' x and x+width

    :param parent_element: parent element
    :param child_element: child element that should be entirely within parent
    :return bool: True if child element is within parent.
    """
    x_lower_bound = parent_element.location['x']
    x_upper_bound = parent_element.location['x'] + parent_element.size['width']

    child_x = child_element.location['x']
    child_width = child_element.size['width']

    return child_x >= x_lower_bound and child_x + child_width <= x_upper_bound


def is_chrome(driver_or_element):
    """
    Is this test running in chrome?

    :param driver_or_element: Selenium WebDriver or WebElement
    :return bool:
    """
    driver = get_driver_from_element(driver_or_element)
    return driver.capabilities.get('chrome')


def is_internet_explorer(driver_or_element):
    """
    Is this test running in IE?

    :param driver_or_element: Selenium WebDriver or WebElement
    :return bool:
    """
    driver = get_driver_from_element(driver_or_element)
    return driver.capabilities.get('browserName') == 'internet explorer'


def is_firefox(driver_or_element):
    """
    Is this test running in Firefox?

    :param driver_or_element: Selenium WebDriver or WebElement
    :return bool:
    """
    driver = get_driver_from_element(driver_or_element)
    return driver.capabilities.get('browserName') == 'firefox'


def get_current_test_name():
    complete_path = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
    # Note: In case the file name of the test is required, use this
    # test_file = complete_path.split("::")[0].split('/')[-1].split('.py')[0]
    test_name = complete_path.split("::")[1]

    return test_name


def is_k8s():
    """
    Is this test running in k8s?
    """
    return "LD_K8S_DIR" in os.environ or "k8s.dev.bb.schrodinger.com" in HOST
