from helpers.selection.live_report_tab import TAB_ACTIVE, TAB_NAME_ATTRIBUTE
from library import dom, wait


def get_active_live_report_name(driver):
    """
    Gets the name of the opened and active LiveReport
    :param driver: webdriver
    :return: str, opened and active LiveReport name
    """
    wait.until_visible(driver, TAB_ACTIVE)
    active_tab = dom.get_element(driver, TAB_ACTIVE)
    return active_tab.get_attribute(TAB_NAME_ATTRIBUTE)
