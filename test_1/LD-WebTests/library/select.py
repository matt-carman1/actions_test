import time

from selenium.webdriver.support.ui import Select

from library import dom, wait


def select_option_by_text(selenium, select_selector, option_text):
    """
    Helper to select an option on a select element, with some added robustness against redraws

    :param selenium: Webdriver
    :param select_selector: The selector for the select element
    :param option_text: The text of the option to select
    :return:
    """

    def select_option(element):
        select_element = Select(element)
        select_element.select_by_visible_text(option_text)
        time.sleep(.5)
        wait.until_visible(selenium, 'option', text=option_text)

    dom.get_element(selenium, select_selector, action_callback=select_option)
