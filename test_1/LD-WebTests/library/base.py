from selenium.webdriver.common.by import By

from helpers.selection.modal import MODAL_DIALOG, OK_BUTTON, CANCEL_BUTTON
from library import dom, simulate, url

__doc__ = """

This file is intended for lower-level, but LiveDesign-specific, test page 
interactions

"""


def go_to_project_picker(driver):
    """
    Open the project picker. This is done by manipulating the URL hash and will
    work even if a modal is blocking the button.

    :param driver: selenium webdriver
    :return: the project picker element
    """
    url.set_page_hash(driver, '/projects')
    return dom.get_element(driver, MODAL_DIALOG)


def click_cancel(driver_or_parent_element):
    """
    Click a modal Cancel button.

    :param driver_or_parent_element: web element
    """
    dom.click_element(driver_or_parent_element, CANCEL_BUTTON, text='Cancel')


def click_ok(driver_or_parent_element):
    """
    Click a modal OK button. There is usually only one on the screen, but if
    more specificity is needed, a container element may be passed in instead of
    the driver.

    :param driver_or_parent_element:
    """
    dom.click_element(driver_or_parent_element, OK_BUTTON)


def set_input_text(parent_element, text, input_label='', character_delay=0):
    """
    Set the value of the first text input in the given element.

    :param parent_element: the parent of the input. This is typically a modal
    window element.
    :param text: the new value
    :param character_delay: how long to wait between entering keystrokes, in
                            seconds. Default is 0
    :param input_label: text in the input's label. This is used to identify the
                        correct input if there is more than one. Note: This will
                        only work if the label as its for attribute set to the
                        id of the corresponding input.
    """

    # If we are given a text label for the input, let's find the label and thus
    # the input. This is only tested with for ExtJS dialog boxes, which
    # consistently set the label for attribute value to the id of the input
    if input_label:
        label_element = dom.get_element(parent_element, 'label', input_label)
        input_id = label_element.get_attribute('for')

        # TODO handle cases where the input is a child of the label (likely in
        # modern HTML, not in ExtJS-derived markup) or those cases where the
        # input is the immediately adjacent sibling to the label (e.g. in
        # parameterized-dialog)
        input_element = dom.get_element(parent_element, input_id, selector_type=By.ID)

        if input_element:
            input_element.clear()
            simulate.typing(input_element, text, character_delay=character_delay)
            return

    # If the above doesn't happen, let's assume that it's the only text input
    # and try that. If there's >1 text input in the parent_element, this will
    # raise an error
    dom.set_element_value(parent_element, 'input[type="text"]', text, character_delay=character_delay)
