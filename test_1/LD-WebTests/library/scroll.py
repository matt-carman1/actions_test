import time

from selenium.common.exceptions import StaleElementReferenceException, \
    WebDriverException
from selenium.webdriver.common.by import By

from library import utils
from library.dom import wait_until, DEFAULT_TIMEOUT
from library.utils import request_animation_frame


def scroll_until_visible(driver,
                         scrollable_element,
                         selector,
                         delta_px=0,
                         text='',
                         horizontal=False,
                         selector_type=By.CSS_SELECTOR,
                         message='',
                         timeout=DEFAULT_TIMEOUT):
    """
    This function imitates a wait_* function from library.dom. However, instead
    of just waiting for an element to become visible, it actively scrolls a
    given parent element, checking after each motion whether a child element
    that matches the supplied selector is visible.

    :param driver: selenium webdriver
    :param scrollable_element: the element to be scrolled
    :param selector: selector for child elements to match.
    :param delta_px: The amount that the element should be scrolled, in pixels.
    :param text: text that the element should contain. Default is an empty
                 string. This is optional.
    :param horizontal: Whether we should scroll horizonally. Default is False,
                       for vertical scrolling
    :param selector_type: format for the selector. Default is By.CSS_SELECTOR.
                          Optional.
    :param message: str, message to be displayed on failure
    :param timeout: time to wait until a TimeoutException is raised. Optional.
    :return:
    """
    return wait_until(driver,
                      _ElementWheeledIntoView(scrollable_element, (selector_type, selector), text, delta_px,
                                              horizontal),
                      message=message,
                      timeout=timeout)


def element_is_scrolled_to_extreme(element, start=True, horizontal=False):
    """
    Is the element scrolled to an extremity? This will return true if the given
    element cannot be scrolled in the given direction
    :param element:
    :param start: True if scrolling to the start (i.e. to the top if vertical,
                  to the left if horizontal). Default is True
    :param horizontal: True if we want to know about horizontal scrolling state.
                       Default is False.
    :return: Boolean
    """
    if start:
        if horizontal:
            return element_is_scrolled_to_left(element)
        else:
            return element_is_scrolled_to_top(element)
    else:
        if horizontal:
            return element_is_scrolled_to_right(element)
        else:
            return element_is_scrolled_to_bottom(element)


def element_is_scrolled_to_bottom(element):
    """
    Is the element scrolled to the bottom?
    :param element:
    :return: Boolean
    """
    # calculation from
    # https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
    scroll_height = int(element.get_property('scrollHeight'))
    scroll_top = int(element.get_property('scrollTop'))
    client_height = int(element.get_property('clientHeight'))

    return scroll_height - scroll_top == client_height


def element_is_scrolled_to_top(element):
    """
    Is the element scrolled to the top?
    :param element:
    :return: Boolean
    """
    return int(element.get_property('scrollTop')) == 0


def element_is_scrolled_to_right(element):
    """
    Is the element scrolled to the right?
    :param element:
    :return: Boolean
    """
    # calculation from
    # https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
    scroll_width = int(element.get_property('scrollWidth'))
    scroll_left = int(element.get_property('scrollLeft'))
    client_width = int(element.get_property('clientWidth'))

    return scroll_width - scroll_left == client_width


def element_is_scrolled_to_left(element):
    """
    Is the element scrolled to the left?
    :param element:
    :return: Boolean
    """
    return int(element.get_property('scrollLeft')) == 0


def wheel_element(driver, element, delta_px, horizontal=False):
    """
    Send the given element a wheel event in order to scroll it, and then await
    a screen redraw.

    :param driver: selenium webdriver
    :param element:
    :param delta_px: How many pixels to scroll.
    :param horizontal: True if wheel event should simulate a horizontal scroll.
                       Default is false.
    :return: None
    """
    if delta_px == 0:
        raise ValueError('Attempt to fire wheel event zero pixels')
    horizontal_px = delta_px if horizontal else 0
    vertical_px = delta_px if not horizontal else 0

    # We extract the selenium driver because if driver is a webelement container/obj, calling .execute_script will give:
    #   AttributeError: 'WebElement' object has no attribute 'execute_script'
    driver = utils.get_driver_from_element(driver)
    driver.execute_script(
        """
    var element = arguments[0];
    var deltaY = arguments[1];
    var deltaX = arguments[2];
        
    var e;
    try {
      // Chrome, Firefox
      e = new WheelEvent('wheel', { bubbles: true, deltaX: deltaX, 
                                    deltaY: deltaY })
    }
    catch(error) {
      // Internet Explorer
      e = document.createEvent('wheelevent');
      e.initWheelEvent('wheel', true, true, window, 0, 0, 0, 0, 0, 0, null, '', 
                       deltaX, deltaY, 0, 0);
    }
    
    element.dispatchEvent(e);
    """, element, vertical_px, horizontal_px)

    request_animation_frame(driver)


def wheel_to_top(driver, element):
    """
    Scroll the given element to the top using a wheel event.

    :param driver: selenium webdriver
    :param element:
    :return: None
    """
    wheel_to_extreme(driver, element, start=True, horizontal=False)


def wheel_to_bottom(driver, element):
    """
    Scroll the given element to the bottom using a wheel event.

    :param driver: selenium webdriver
    :param element:
    :return: None
    """
    wheel_to_extreme(driver, element, start=False, horizontal=False)


def wheel_to_leftmost(driver, element):
    """
    Scroll the given element to the left extreme using a wheel event.

    :param driver: selenium webdriver
    :param element:
    :return: None
    """
    wheel_to_extreme(driver, element, start=True, horizontal=True)


def wheel_to_rightmost(driver, element):
    """
    Scroll the given element to the right extreme using a wheel event.

    :param driver: selenium webdriver
    :param element:
    :return: None
    """
    wheel_to_extreme(driver, element, start=False, horizontal=True)


def wheel_to_extreme(driver, element, start=True, horizontal=False):
    """
    Scroll the given element to the maximum extent in the given direction. This
    is done by simulating a wheel event that scrolls the largest finite integer
    number of pixels.

    :param driver: selenium webdriver
    :param element:
    :param start: Boolean for whether we will go to the start (True) or the end
                  of the scroll range. Default is True.
    :param horizontal: Boolean for whether we will scroll horizontally. Default
                       is False, i.e. vertical scrolling.
    :return: None
    """
    driver = utils.get_driver_from_element(driver)
    driver.execute_script(
        """
        var element = arguments[0];
        var start = arguments[1];
        var horizontal = arguments[2];
        
        var e;
        try {
          // Chrome, Firefox
          var deltaKey = horizontal ? 'deltaX' : 'deltaY';
          var deltaValue = start ? Number.MIN_SAFE_INTEGER : 
                                   Number.MAX_SAFE_INTEGER;
          
          var eventPayload = { bubbles: true };
          eventPayload[deltaKey] = deltaValue;
          e = new WheelEvent('wheel', eventPayload);
        }
        catch(error) {
          // Internet Explorer
          var dx = horizontal ? deltaValue : 0;
          var dy = horizontal ? 0 : deltaValue;
          e = document.createEvent('wheelevent');
          e.initWheelEvent('wheel', true, true, window, 0, 0, 0, 0, 0, 0, null, 
                           '', dx, dy, 0, 0);
        }
        
        element.dispatchEvent(e);
    """, element, start, horizontal)


def user_scroll(driver, element, delta_px, horizontal=False, chunk_px=10, chunk_delay=.01):
    """
    Simulate user scroll, optionally with a delay between "chunks"
    :param driver: selenium webdriver
    :param element: the element to scroll
    :param delta_px: total pixels to scroll
    :param horizontal: True if wheel event should simulate a horizontal scroll.
                       Default is false.
    :param chunk_px: the size in pixels of each scroll event. Default is 10
    :param chunk_delay: how many seconds to wait between scroll events. Default is 50ms
    :return:
    """
    while delta_px > 0:
        wheel_element(driver, element, chunk_px, horizontal)
        delta_px -= chunk_px
        time.sleep(chunk_delay)


class _ElementWheeledIntoView(object):
    """ An expectation for checking that an element has scrolled into view. More
    specifically, it searches for elements within the parent_element that match
    the child_selector, contain the specified text (if any), and if visible,
    returns the first found element. If none are visible the parent_element is
    scrolled by sending a wheel event of a specified number of pixels either
    horizontally or vertically before trying again.

    :param parent_element: the element that will be scrolled
    :param child_locator: a selector that will search inside the parent element
                          for all matching elements
    :param text: the text to search for in found child elements
    :param delta_px: the number of pixels to scroll parent_element if no
                     matching elements are found
    :param horizontal: if truthy, we scroll horizontally. Otherwise, and in the
                       default, scroll vertically.
    :return: the WebElement once it is located and visible
    """

    def __init__(self, parent_element, child_locator, text='', delta_px=0, horizontal=False):
        if delta_px == 0:
            raise ValueError('Please provide a non-zero delta_px to scroll element')

        self.parent_element = parent_element
        self.child_locator = child_locator
        self.delta_px = delta_px
        self.horizontal = horizontal
        self.text = text

    def __call__(self, driver):
        try:
            child_elements = _find_elements(driver, self.child_locator)

            if self.horizontal:
                bounds_check = utils.element_is_horizontally_within_parent
            else:
                bounds_check = utils.element_is_vertically_within_parent

            found_element = next((element for element in child_elements
                                  if element.is_displayed() and bounds_check(self.parent_element, element) and
                                  (not self.text or self.text in element.text)), None)

            if found_element:
                return found_element

            self._move_element(driver)
            return False

        except StaleElementReferenceException:
            return False

    def _move_element(self, driver):
        delta_px_is_positive = self.delta_px > 0

        # If we have hit the end of the scroll of an element, go back to the
        # beginning
        if element_is_scrolled_to_extreme(self.parent_element,
                                          start=not delta_px_is_positive,
                                          horizontal=self.horizontal):
            wheel_to_extreme(driver, self.parent_element, start=delta_px_is_positive, horizontal=self.horizontal)

        # Otherwise move it by the specified amount
        else:
            wheel_element(driver, self.parent_element, self.delta_px, self.horizontal)


# copied from selenium.webdriver.support.expected_conditions to avoid importing
# private
def _find_elements(driver, by):
    try:
        return driver.find_elements(*by)
    except WebDriverException as e:
        raise e


# NOTE: Wrote this specifically for Scrolling over the Compounds Panel because other helpers that uses WheelEvent are
# not working properly for the Compounds panel.
def scroll_element_by(driver, scrollable_element, horizontal_px=0, vertical_px=0):
    """
    scrolls the element by the specified number of pixels both horizontally and vertically. It uses scrollBy() method
    internally to scroll the specified element.

    :param driver: Selenium Webdriver
    :param scrollable_element: web element to be scrolled.
    :param horizontal_px: int, pixels to be scrolled by horizontally.
    :param vertical_px: int, pixels to be scrolled by vertically.
    :return: None
    """

    scrolled_distance = driver.execute_script(
        """
        var element = arguments[0];
        element.scrollBy(arguments[1], arguments[2]);
        return element.scrollTop;
       """, scrollable_element, horizontal_px, vertical_px)

    return scrolled_distance
