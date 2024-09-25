import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from typing import Callable
from helpers.selection.grid import GRID_SCROLLBAR_THUMB
from helpers.selection.modal import EXTJS_LOADING_MASK, LOADING_MASK, LR_LOADING_MASK
from library import dom, utils
from library.dom import DEFAULT_TIMEOUT, ElementCriteriaCondition, \
    LiveDesignWebException
from library.style import get_inline_style_as_dict
import re


def until_visible(driver_or_parent_element,
                  selector,
                  text='',
                  selector_type=By.CSS_SELECTOR,
                  timeout=DEFAULT_TIMEOUT,
                  dont_raise=False,
                  exact_text_match=True):
    """
    This will block execution until an element that matches the specified
    selector is visible and raises an exception if none are visible after
    the timeout

    :param driver_or_parent_element: webdriver or parent element object
    :param selector: selector for elements to match.
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param timeout: time to wait until the function times out. Optional.
    :param dont_raise: by default, this method raises a TimeoutException once it
                       has run out of time. If this param is set to true, the
                       TimeoutException is swallowed. This is useful in cases
                       where some element *may* be visible, in which case some
                       conditional action is performed. For example, see
                       helpers.change.actions_pane.open_filter_action
    :param exact_text_match: Whether text match should be exact. Optional.
    """
    dom.get_element(driver_or_parent_element,
                    selector,
                    text=text,
                    selector_type=selector_type,
                    timeout=timeout,
                    dont_raise=dont_raise,
                    exact_text_match=exact_text_match,
                    require_single_matching_element=False)


def until_not_visible(driver_or_parent_element,
                      selector,
                      text='',
                      selector_type=By.CSS_SELECTOR,
                      timeout=DEFAULT_TIMEOUT,
                      dont_raise=False):
    """
    This will block execution until an element that matches the specified
    selector is no longer visible, and raises an error if an element remains
    visible after the timeout

    :param driver_or_parent_element: webdriver or parent element object
    :param selector: selector for elements to match.
    :param text: optionally, text that the element should contain exactly.
    :param text: str, exact text that the element should contain. This is optional
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param timeout: time to wait until the function times out. Optional.
    :param dont_raise: by default, this method raises a TimeoutException once it
                       has run out of time. If this param is set to true, the
                       TimeoutException is swallowed. This is useful in cases
                       where some element *may* be visible, in which case some
                       conditional action is performed. For example, see
                       helpers.change.actions_pane.open_filter_action
    """
    callback = ElementCriteriaCondition((selector_type, selector),
                                        text,
                                        require_single_matching_element=False,
                                        exact_text_match=True)
    message = 'A visible element matching {} `{}` was found'.format(selector_type, selector)

    if text:
        message += ' with exact text content `{}`'.format(text)

    try:
        dom.wait_until_not(driver_or_parent_element, callback, message, timeout)
    except TimeoutException as e:
        if dont_raise:
            return None

        raise LiveDesignWebException(e.msg) from e


def until_page_title_is(driver, expected_page_title, timeout=DEFAULT_TIMEOUT):
    """
    Blocks execution until the page title matches the given title, or raises a
    TimeoutException if the page has not matched after a given timeout.

    Example usage:

    wait.until_page_title_is(driver, 'Log in to LiveDesign')

    :param driver: selenium webdriver
    :param expected_page_title: the expected page title
    :param timeout: optional timeout value to override default
    :return:
    """

    def title_filter_function(element):
        # we can't use 'text' prop for the title element because it's not
        # visible so selenium returns an empty string. Instead we use the
        # 'textContent' attribute to compare to expected
        current_page_title = element.get_attribute('textContent')
        if not current_page_title:
            return False
        return current_page_title.strip() == expected_page_title.strip()

    page_title_condition = ElementCriteriaCondition((By.TAG_NAME, 'title'),
                                                    must_be_visible=False,
                                                    filter_function=title_filter_function)

    message = 'Expected html page title to be `{}`'.format(expected_page_title)

    dom.wait_until(driver, page_title_condition, message, timeout)


def until_loading_mask_not_visible(driver):
    """
    Utility function for waiting till the loading mask goes away

    :param driver: Selenium Webdriver
    """
    utils.request_animation_frame(driver)
    loading_mask = dom.get_element(driver, LOADING_MASK, timeout=2, dont_raise=True)

    if loading_mask:
        until_not_visible(driver, LOADING_MASK, timeout=2, dont_raise=True)


def until_extjs_loading_mask_not_visible(driver):
    """
    Utility function for waiting till the ExtJS viewport loading mask goes away
    This mask shows up whenever freezing or unfreezing compounds.

    :param driver: Selenium Webdriver
    """
    until_not_visible(driver, EXTJS_LOADING_MASK)


def until_live_report_loading_mask_not_visible(driver):
    """
    Utility function for waiting till the LR loading mask is not visible

    :param driver: Selenium Webdriver
    """
    # This wait on requestAnimationFrame is needed so we don't pass the wait before the LR loading mask becomes visible
    utils.request_animation_frame(driver)
    until_not_visible(driver, LR_LOADING_MASK)


def until_grid_is_scrolled_to_leftmost(driver):
    """
    :param driver: Selenium Webdriver
    """

    # if the grid's scrollbar doesn't exist, then the grid is already scrolled to the beginning
    scrollbar_thumb = dom.get_visibility_callback((By.CSS_SELECTOR, GRID_SCROLLBAR_THUMB), '')(driver)
    if not scrollbar_thumb:
        return

    def scrollbar_thumb_position_checker(thumb):
        thumb_styles = get_inline_style_as_dict(thumb)

        if 'left' in thumb_styles:
            # either the thumb is positioned through css `left`
            match = re.match(r'(.+)px', thumb_styles['left'])
            thumb_offset = float(match.group(1))
        else:
            # or the thumb is positioned through css `transform`
            transform = thumb_styles['transform']

            # NOTE (pradeep): The regex monstrosity here matches and extracts the horizontal translation value.
            # eg: The value `100` is extracted from the string "translate3d(100px, 20px, 50px)"
            match = re.match(r'translate3d\((.+)px,\s*.*,\s*.*\)', transform)
            thumb_offset = float(match.group(1))

        # Due to borders/margins/paddings/other pixel imperfections, it's a good idea to keep a small
        # tolerance to error when calculating DOM bounds.
        error_delta = 5

        return (-error_delta) <= thumb_offset <= error_delta

    dom.wait_until(scrollbar_thumb, scrollbar_thumb_position_checker)


def until_condition_met(condition_function: Callable, retries: int = 60, interval: int = 1000, driver=None):
    """
    Retries to execute a callable function with wait time in-between each attempt.
    Exits if function is successfully executed before maximum number of retries given.

    :param condition_function: a callable function
    :param retries: int, max # of retries
    :param interval: int, wait time in-between each attempt of execution of the function (in ms)
    :param driver: selenium webdriver
    """
    for i in range(retries):
        try:
            if driver:
                condition_function(driver)
            else:
                condition_function()
            return
        except AssertionError as e:
            if i == retries - 1:
                raise e
            time.sleep(interval / 1000)


def sleep_if_k8s(seconds: int):
    """
    Sleep for a certain amount of time, but only when running in k8s / new Jenkins

    :param seconds: The number of seconds to sleep for
    """
    if utils.is_k8s():
        time.sleep(seconds)
