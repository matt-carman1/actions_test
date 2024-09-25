from helpers.selection.visualize import VISUALIZE_TAB
from library import dom, ensure
from helpers.change.actions_pane import TOOLS_PANE_TOOL
import time


def open_gadget(driver, gadget_tab_name=None):
    #ensure.element_visible(driver, '.create-custom-container', '.gadget-item', action_selector_text='VISUALIZE +')
    dom.click_element(driver, TOOLS_PANE_TOOL, gadget_tab_name, True)
    time.sleep(2)
    id = dom.get_element(driver, 'iframe').get_attribute('id')
    return dom.get_element(driver, '#' + id).get_attribute('id')
