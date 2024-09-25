import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from library.utils import request_animation_frame, get_driver_from_element, is_firefox


def hover(driver_or_element, element=None):
    """
    Simulate a hover event for the given element.

    Note: Supplying the driver as first argument is optional. i.e.
        simulate.hover(driver, element)
    and
        simulate.hover(element)
    behave identically.

    :param driver_or_element: webdriver or an element
    :param element:
    :return: None
    """
    driver = get_driver_from_element(driver_or_element)
    if not element:
        element = driver_or_element

    ActionChains(driver).move_to_element(element).perform()


def click(driver_or_element, element=None):
    """
    Correctly simulate a click. First hover, then wait for a screen redraw, then
    click.

    Note: Supplying the driver as first argument is optional. i.e.
        simulate.click(driver, element)
    and
        simulate.click(element)
    behave identically.

    :param driver_or_element:
    :param element:
    :return: None
    """
    driver = get_driver_from_element(driver_or_element)
    if not element:
        element = driver_or_element

    # First hover to correctly simulate user interaction
    hover(driver, element)

    # Then wait for a redraw -- we often need to await state change after hover
    # so that click works correctly.
    request_animation_frame(driver)

    # OK, *NOW* you can click on the thing.
    element.click()


def double_click(element, shift_key_held_during_double_click=False):
    """
    Simulate a double click. First hover, then wait for screen redraw, then
    execute double click.

    Essentially the same as "click" except we are using ActionChains to
    double click on the element.

    :param element: WebElement to double click
    :param shift_key_held_during_double_click: if true, we will hold the shift key down for this click event
    """
    driver = get_driver_from_element(element)
    hover(driver, element)
    request_animation_frame(driver)

    # Get the javascript format of boolean value as a string for interpolation into the script
    shift_key_str = 'true' if shift_key_held_during_double_click else 'false'

    # Double click using ActionChains class does not work in firefox. Please refer to SS-26726 for details.
    if is_firefox(driver):
        driver.execute_script(
            """
            return (function(target) {{
                if (target.fireEvent) {{
                    target.fireEvent('ondblclick');
                }} else {{
                    var evObj = new MouseEvent('dblclick', {{
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        shiftKey: {},
                    }});
                    target.dispatchEvent(evObj);
                }}
                return true;
            }})(arguments[0]);""".format(shift_key_str), element)
    else:
        if shift_key_str:
            ActionChains(driver).key_down(Keys.SHIFT).double_click(element).key_up(Keys.SHIFT).perform()
        else:
            ActionChains(driver).double_click(element).perform()


def typing(element, value, character_delay=0):
    """
    Simulate text entry, optionally with a delay between characters
    :param element: the element to send the text value
    :param value: str, the text to send
    :param character_delay: how long to wait between keys. Default is 0
    :return:
    """
    if character_delay:
        for char in value:
            element.send_keys(char)
            time.sleep(character_delay)
    else:
        element.send_keys(value)


def right_click(element):
    """

    :param element:
    :return:
    """
    driver = get_driver_from_element(element)
    hover(driver, element)
    request_animation_frame(driver)
    ActionChains(driver).context_click(element).perform()


def select_all(input_element):
    """
    Function to select all for a given input element

    :param input_element: the element whose value should be selected
    """
    driver = get_driver_from_element(input_element)
    driver.execute_script('arguments[0].select();', input_element)