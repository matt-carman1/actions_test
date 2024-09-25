"""
Test splash page in an empty Device LiveReport for Material Science mode.
"""

import pytest

from library import wait, dom

from helpers.change.actions_pane import close_add_compounds_panel
from helpers.verification.element import verify_is_visible
from helpers.selection.add_compound_panel import SEARCH_BY_ID_TEXTAREA
from helpers.selection.visualize import VISUALIZER_ACTIVE_TAB_TITLE_BAR
from helpers.selection.splash_page import BODY, BY_ID_CARD_TITLE, BY_ID_CARD_BUTTON, ADD_DEVICES_TITLE, \
    ADD_DEVICES_FROM_FILE_BUTTON

LD_PROPERTIES = {'LIVEDESIGN_MODE': 'MATERIALS_SCIENCE', 'ENABLE_DEVICE_LIVE_REPORTS': 'true'}
test_report_type = 'device'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('new_live_report')
@pytest.mark.usefixtures('customized_server_config')
def test_empty_device_livereport_cards(selenium):
    """
    Testing 2 cards present on creating a new empty Devices LR. Check that:
        1. The boxes contain correct titles.
        2. Buttons open correct dialog boxes.

    :param selenium: Selenium Webdriver
    """

    # Check for 2 'Add devices' cards (Title + Button)
    wait.until_visible(selenium, BODY)
    verify_is_visible(selenium, BY_ID_CARD_TITLE, selector_text='Add devices')
    verify_is_visible(selenium, BY_ID_CARD_BUTTON, selector_text='By ID')
    verify_is_visible(selenium, ADD_DEVICES_TITLE, selector_text='Add devices')
    verify_is_visible(selenium, ADD_DEVICES_FROM_FILE_BUTTON, selector_text='From file')

    # Click on 'By ID' button
    dom.click_element(selenium, BY_ID_CARD_BUTTON)
    verify_is_visible(selenium, SEARCH_BY_ID_TEXTAREA)
    close_add_compounds_panel(selenium)

    # Click on 'From File' button
    dom.click_element(selenium, ADD_DEVICES_FROM_FILE_BUTTON)
    verify_is_visible(selenium, VISUALIZER_ACTIVE_TAB_TITLE_BAR, selector_text='OLED Import Tool')
