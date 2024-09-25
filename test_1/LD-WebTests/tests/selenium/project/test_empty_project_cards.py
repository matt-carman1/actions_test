"""

Test splash page on opening project for first time .

"""
import pytest

from library import wait, dom

from helpers.verification.element import verify_is_visible
from helpers.change.live_report_picker import close_metapicker
from helpers.selection.modal import CANCEL_BUTTON, WINDOW_HEADER_TEXT, MODAL_DIALOG_HEADER
from helpers.selection.splash_page import BODY, CREATE_LR_TITLE, CREATE_LR_BUTTON, OPEN_LR_TITLE, OPEN_LR_BUTTON
from helpers.selection.live_report_tab import CREATE_NEW_LIVE_REPORT


@pytest.mark.usefixtures("open_project")
def test_empty_project_cards(selenium):
    """
    Testing 2 cards are present on opening a project for first time.
    The boxes contain correct titles.
    Buttons open correct dialog boxes.

    :param selenium: Selenium Webdriver
    """
    # Check for 'Create and Open a New LiveReport' cards
    wait.until_visible(selenium, BODY)
    verify_is_visible(selenium, CREATE_LR_TITLE, selector_text='Create a\nNew LiveReport')
    verify_is_visible(selenium, OPEN_LR_TITLE, selector_text='Open an\nExisting LiveReport')

    # Click on 'Create' button
    dom.click_element(selenium, CREATE_LR_BUTTON)
    wait.until_visible(selenium, WINDOW_HEADER_TEXT, text=CREATE_NEW_LIVE_REPORT)
    dom.click_element(selenium, CANCEL_BUTTON)

    # Click on 'Open' button
    dom.click_element(selenium, OPEN_LR_BUTTON)
    wait.until_visible(selenium, MODAL_DIALOG_HEADER, text="Manage LiveReports")
    close_metapicker(selenium)
