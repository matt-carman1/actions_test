"""
This file encapsulates the lowest-level page interactions we will perform during
a test. These methods have a selector as an argument, will wait for a matching
element to be present in the dom, and return one element or a list of elements.

Note that these functions encapsulate logic to handle timeouts. The maximum time
to wait for a matching element can be overridden by specifying a value for the
timeout optional named parameter.
"""
import sys
import logging

from selenium.common.exceptions import StaleElementReferenceException, \
    WebDriverException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from library import simulate, utils

DEFAULT_TIMEOUT = 60

LOGGER = logging.getLogger(__name__)


def get_element(driver_or_parent_element,
                selector,
                text='',
                exact_text_match=False,
                selector_type=By.CSS_SELECTOR,
                timeout=DEFAULT_TIMEOUT,
                dont_raise=False,
                must_be_visible=True,
                must_be_clickable=False,
                require_single_matching_element=True,
                action_callback=None):
    """
    This will block execution until an element that matches the specified
    selector is visible.

    :param driver_or_parent_element: webdriver or parent element object
    :param selector: selector for elements to match.
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.

    :param exact_text_match: Whether text match should be exact or not.
                             Disabled by default.
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param timeout: time to wait until a TimeoutException is raised. Optional.
    :param dont_raise: by default, this method raises a TimeoutException once it
                       has run out of time. If this param is set to true, the
                       TimeoutException is swallowed. This is useful in cases
                       where some element *may* be visible, in which case some
                       conditional action is performed. For example, see
                       library.ensure.element_visible
    :param must_be_visible: true if the returned components must be visible.
                            Optional. Default is True.
    :param must_be_clickable: true if the returned components must be clickable.
                            Optional. Default is False.
    :param require_single_matching_element: raise a LiveDesignWebException if >1 element
                                                    matched all criteria. Default is True.
    :param action_callback: a function that will be called on the matching element. If this
                            function throws an exception (e.g. a StaleElementException),
                            we will retry until timeout.
    :return: the matched element. This method may raise either a
             TimeoutException if 0 elements are found and a
             LiveDesignWebException if >1 element matched all criteria.
    """
    callback = ElementCriteriaCondition((selector_type, selector),
                                        text,
                                        exact_text_match=exact_text_match,
                                        must_be_visible=must_be_visible,
                                        must_be_clickable=must_be_clickable,
                                        require_single_matching_element=require_single_matching_element,
                                        action_callback=action_callback)
    message = 'No element matching {} `{}` was found'.format(selector_type, selector)
    if text:
        message += ' containing text `{}`'.format(text)

    if hasattr(driver_or_parent_element, '_selector_used_to_find'):
        message += " within parent {} `{}`".format(*driver_or_parent_element._selector_used_to_find)

    try:
        return wait_until(driver_or_parent_element, callback, message, timeout)
    except TimeoutException as e:
        if dont_raise:
            LOGGER.warning('ignored exception with message ' + message)
            return None

        msg = e.msg
        if getattr(callback, 'reason_elements_filtered', None):
            msg = msg + '\nElements that matched the selector were filtered because:\n' + '\n'.join(
                callback.reason_elements_filtered)

        raise LiveDesignWebException(msg) from e


def click_element(driver_or_parent_element,
                  selector,
                  text='',
                  exact_text_match=False,
                  selector_type=By.CSS_SELECTOR,
                  timeout=DEFAULT_TIMEOUT,
                  must_be_visible=True):
    """
    This will block execution until an element that matches the specified
    selector is visible. When found, a click is simulated.

    :param driver_or_parent_element: webdriver or parent element object
    :param selector: selector for elements to match.
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.
    :param exact_text_match: Whether text match should be exact or not.
                             Disabled by default.
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param timeout: time to wait until a TimeoutException is raised. Optional.
    :param must_be_visible: boolean, default True. Must elements that
                            match be visible?
    :return: the matched element. This method will raise an
             TimeoutException if 0 elements are found and a
             LiveDesignWebException if >1 element matched all criteria.
    """

    def click_element_action_callback(found_element):
        simulate.click(driver_or_parent_element, found_element)

    element = get_element(driver_or_parent_element,
                          selector,
                          text,
                          exact_text_match,
                          selector_type,
                          timeout,
                          must_be_visible=must_be_visible,
                          must_be_clickable=True,
                          action_callback=click_element_action_callback)

    return element


def get_parent_element(element):
    """
    Returns parent of given element

    :param element: element object
    :return: the matched element. This method may raise either a
             TimeoutException if 0 elements are found and a
             LiveDesignWebException if >1 element matched all criteria.
    """
    return get_element(element, '..', selector_type=By.XPATH)


def set_element_value(driver_or_parent_element,
                      selector,
                      value,
                      text='',
                      exact_text_match=False,
                      selector_type=By.CSS_SELECTOR,
                      timeout=DEFAULT_TIMEOUT,
                      character_delay=0,
                      clear_existing_value=True):
    """
    This will block execution until an element that matches the specified
    selector is visible. When matched, its value is cleared and a value is sent.

    :param driver_or_parent_element: webdriver or parent element object
    :param selector: selector for elements to match.
    :param value: new value for the element
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.
    :param exact_text_match: Whether text match should be exact or not.
                             Disabled by default.
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param timeout: time to wait until a TimeoutException is raised. Optional.
    :param character_delay: how long to wait between entering keystrokes, in
                            seconds. Default is 0
    :param clear_existing_value: should exisitng value be cleared before setting
                                 new value. This occasionally causes elements to
                                 change visibility
    :return: the matched element. This method will raise an
             TimeoutException if 0 elements are found and a
             LiveDesignWebException if >1 element matched all criteria.
    """
    element = click_element(driver_or_parent_element, selector, text, exact_text_match, selector_type, timeout)
    if clear_existing_value:
        driver = utils.get_driver_from_element(driver_or_parent_element)
        while element.get_attribute('value'):
            driver.execute_script(
                """
                    var inputElement = arguments[0];
                    inputElement.focus();
                    inputElement.select();
                """, element)
            ActionChains(driver).send_keys(Keys.BACKSPACE).perform()

    simulate.typing(element, value, character_delay=character_delay)
    return element


def get_elements(driver_or_parent_element,
                 selector,
                 text='',
                 exact_text_match=False,
                 selector_type=By.CSS_SELECTOR,
                 timeout=DEFAULT_TIMEOUT,
                 dont_raise=False,
                 must_be_visible=True):
    """
    This will block execution until one or more elements matching the specified
    selector are visible.

    :param driver_or_parent_element: webdriver or parent element
    :param selector: selector for elements to check.
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.
    :param exact_text_match: Whether text match should be exact or not.
                             Disabled by default.
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
    :param timeout: time to wait until we timeout
    :param dont_raise: by default, this method raises a TimeoutException once it
                       has run out of time. If this param is set to true, the
                       TimeoutException is swallowed. This is useful in cases
                       where some element *may* be visible, in which case some
                       conditional action is performed. For example, see
                       helpers.change.actions_pane.open_filter_action
    :param must_be_visible: boolean, default True. Must elements that
                            match be visible?
    :return: a list of all matching elements that are visible
    """
    callback = ElementCriteriaCondition((selector_type, selector),
                                        text,
                                        exact_text_match=exact_text_match,
                                        must_be_visible=must_be_visible,
                                        return_all_matching=True)
    message = "Expected at least one element matching {} `{}` to become " \
              "visible".format(selector_type, selector)
    if text:
        message += ' containing text `{}`'.format(text)

    if hasattr(driver_or_parent_element, '_selector_used_to_find'):
        message += " within parent {} `{}`".format(*driver_or_parent_element._selector_used_to_find)

    try:
        return wait_until(driver_or_parent_element, callback, message, timeout)
    except TimeoutException as e:
        if dont_raise:
            LOGGER.warning('ignored exception with message ' + message)
            return []

        raise LiveDesignWebException(e.msg) from e


def wait_until(driver_or_element, callback, message='', timeout=DEFAULT_TIMEOUT):
    """
    Block testing until condition returned by callback is not false
    See: selenium.webdriver.support.wait.WebDriverWait
    """
    return WebDriverWait(driver_or_element, timeout).until(callback, message)


def wait_until_not(driver_or_element, callback, message='', timeout=DEFAULT_TIMEOUT):
    """
    Block testing until condition returned by callback is not false
    See: selenium.webdriver.support.wait.WebDriverWait
    """
    return WebDriverWait(driver_or_element, timeout) \
        .until_not(callback, message)


def get_visibility_callback(locator, text):
    """
    If text is defined, we will use the callback defined in this file that
    matches text inside the element in addition to using a selector. Otherwise
    we use a callback defined in expected_conditions.
    :param locator:
    :param text:
    :return: callback
    """
    return ElementCriteriaCondition(locator, text)


class ElementCriteriaCondition(object):
    """ This is an expectation (see
    selenium.webdriver.support.expected_conditions) that finds all visible
    elements that match a given selector and then finds all those whose text
    content includes a given string. If >1 element is found, we will throw an
    Exception, otherwise we return the single matching element.
    """

    def __init__(self,
                 locator,
                 text='',
                 exact_text_match=False,
                 must_be_visible=True,
                 filter_function=None,
                 must_be_clickable=False,
                 return_all_matching=False,
                 require_single_matching_element=True,
                 action_callback=None):
        """
        Constuct an ElementCriteriaCondition with the desired conditions. This
        can then be passed into wait_until or wait_until_not as the callback.

        For example usage, see dom.get_element or wait.until_page_title_is

        :param locator: a tuple of (selector_type, selector)
        :param text: str, optional. text that an element should contain
        :param exact_text_match: Whether text match should be exact or not.
                                 Disabled by default.
        :param must_be_visible: boolean, default True. Must elements that
                                match be visible?
        :param filter_function: a function that takes an element as an argument
                                and returns a boolean representing whether the
                                element should be regarded as a match.
        :param must_be_clickable: boolean, default False. Must elements that
                                match be clickable?
        :param return_all_matching: return all found elements (may be slow)
        :param require_single_matching_element: if >1 element matches the selector, fail
        :param action_callback: optional function to pass that will act on the found element(s)
        """
        self.locator = locator
        self.expected_text = text
        self.exact_text_match = exact_text_match
        self.return_all_matching = return_all_matching
        self.require_single_matching_element = require_single_matching_element
        self.action_callback = action_callback
        self.must_be_visible = must_be_visible
        self.must_be_clickable = must_be_clickable
        self.filter_function = filter_function
        self.last_found_elements = ()

    def test_element(self, element):
        if self.expected_text:
            actual_text = element.text
            if self.exact_text_match and self.expected_text != actual_text:
                self.reason_elements_filtered.append('element text `{}` did not match expected value `{}`'.format(
                    actual_text, self.expected_text))
                return False
            elif self.expected_text not in actual_text:
                self.reason_elements_filtered.append('element text `{}` did not contain expected substring `{}`'.format(
                    actual_text, self.expected_text))
                return False

        if self.must_be_visible and not element.is_displayed():
            self.reason_elements_filtered.append('element is not visible')
            return False

        if self.must_be_clickable and not element.is_enabled():
            self.reason_elements_filtered.append('element is not clickable')
            return False

        if self.filter_function and not self.filter_function(element):
            self.reason_elements_filtered.append('element failed to pass custom filter')
            return False

        return True

    def __call__(self, driver_or_parent_element):
        try:
            self.last_found_elements = driver_or_parent_element.find_elements(*self.locator)
            self.reason_elements_filtered = []
            element_generator = (element for element in self.last_found_elements if self.test_element(element))

            if self.return_all_matching:
                result = []
                for element in element_generator:
                    element._selector_used_to_find = self.locator
                    result.append(element)
            else:
                result = next(element_generator, None)
                if result:
                    result._selector_used_to_find = self.locator

                # If we find another match, throw an error
                if self.require_single_matching_element and next(element_generator, None):
                    msg = "Found more than one element for {} `{}`".format(*self.locator)
                    if self.expected_text:
                        msg += " with text `{}`".format(self.expected_text)
                    if hasattr(driver_or_parent_element, '_selector_used_to_find'):
                        msg += " within parent {} `{}`".format(*driver_or_parent_element._selector_used_to_find)
                    msg += ". Please make the selector more specific, set the error_if_selector_matches_many_elements" \
                           " flag to False or consider using dom.get_elements"
                    raise LiveDesignWebException(msg)

            if result and self.action_callback:
                self.action_callback(result)

            return result

        except (StaleElementReferenceException, WebDriverException, LiveDesignRetryException, StopIteration) as e:
            return False


class LiveDesignWebException(Exception):
    """
    Exception thrown by the core web test framework
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class LiveDesignRetryException(Exception):
    """
    Exception raised when a DOM interaction did not succeed but may succeed if retried.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


def copy(driver):
    """
    Function to copy current page selection by simulating the user
    typing ctrl/command + c

    :param driver: selenium webdriver
    """
    ctrl = get_ctrl_key()

    copy_action = ActionChains(driver).key_down(ctrl).send_keys('c').key_up(ctrl)
    copy_action.perform()


def paste(driver_or_element):
    """
    Function to paste a copied or cut selection by simulating the user
    typing ctrl/command + v

    :param driver_or_element: element to paste onto, or webdriver
    """
    if sys.platform == 'darwin':
        if utils.is_chrome(driver_or_element):
            # Chrome on Mac is odd.
            # https://stackoverflow.com/a/41046276
            paste_keys = (Keys.SHIFT, Keys.INSERT)
        else:
            paste_keys = (Keys.COMMAND, 'v')
    else:
        paste_keys = (Keys.CONTROL, 'v')

    driver_or_element.send_keys(*paste_keys)


def get_ctrl_key():
    """
    Set control key to "Command" or "Control" depending on platform

    :return: corresponding control key
    """

    if sys.platform == 'darwin':
        return Keys.COMMAND
    return Keys.CONTROL


def select_cut_and_paste_text(driver):
    """
    Selects the text, cuts it and pastes it.

    :param driver: Selenium Webdriver
    """
    ctrl = get_ctrl_key()
    action_chain = ActionChains(driver)
    action_chain.key_down(ctrl).send_keys('a').perform()
    action_chain.key_down(ctrl).send_keys('x').perform()
    action_chain.key_down(ctrl).send_keys('v').perform()


def press_esc(driver):
    """
    Presses the Esc key
    """
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def press_enter_key(driver):
    """
    Presses the Enter key
    """
    ActionChains(driver).send_keys(Keys.ENTER).perform()


def press_ctrl_and_keys(driver, *keys):
    """
    Holds Ctrl/Command while pressing key(s).

    :param driver: Selenium Webdriver
    :param keys: Keys/str, if you want to pass keys use from selenium.webdriver.common.keys, otherwise use letters like
     'f', 'c' etc as string.
    :return: None
    """
    control_key = get_ctrl_key()
    ActionChains(driver).key_down(control_key).send_keys(*keys).key_up(control_key).perform()


def press_keys(driver, *keys):
    """
    Presses key(s)

    :param driver: Selenium driver or element
    :param keys: Keys, from selenium.webdriver.common.keys
    :return: None
    """
    ActionChains(driver).send_keys(*keys).perform()


def get_pseudo_element_property_value(driver, selector, pseudo_elem=':after', property_='content'):
    """
    Function to retrieve property value of a particular selector's pseudo-element using javascript

    :param driver: Selenium Webdriver
    :param selector: str, Selector which holds the pseudo element
    :param pseudo_elem: str, Pseudo-element value. Default value set as ':after'
    :param property_: str, Property of the pseudo-element. Default value set as 'content'

    :returns: str, Property value
    """

    value = driver.execute_script(
        """return window.getComputedStyle(document.querySelector(arguments[0]),
                                    arguments[1]).getPropertyValue(arguments[2])""", selector, pseudo_elem, property_)
    return value
