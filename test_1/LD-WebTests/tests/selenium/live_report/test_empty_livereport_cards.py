"""

Test splash page in an empty LiveReport.

"""
import pytest

from library import wait, dom

from helpers.verification.element import verify_is_visible
from helpers.selection.add_compound_panel import SEARCH_BY_ID_TEXTAREA, REALTIME_PROPERTIES_PANE, IMPORT_FILE_BUTTON
from helpers.selection.column_tree import COLUMN_TREE_PICKER
from helpers.selection.splash_page import BODY, BY_STRUCTURE_CARD_TITLE, BY_STRUCTURE_CARD_BUTTON, BY_ID_CARD_TITLE, \
    BY_ID_CARD_BUTTON, FILE_CARD_TITLE, FILE_CARD_BUTTON, DATA_COLUMNS_CARD_TITLE, DATA_COLUMNS_CARD_BUTTON


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_empty_livereport_cards(selenium):
    """
    Testing 4 cards are present on creating a new empty LR.
    The boxes contain correct titles.
    Buttons open correct dialog boxes.

    :param selenium: Selenium Webdriver
    """
    # Check for 4 'Add...' cards
    wait.until_visible(selenium, BODY)
    verify_is_visible(selenium, BY_STRUCTURE_CARD_TITLE, selector_text='Add compounds')
    verify_is_visible(selenium, BY_STRUCTURE_CARD_BUTTON, selector_text='By Structure')
    verify_is_visible(selenium, BY_ID_CARD_TITLE, selector_text='Add compounds')
    verify_is_visible(selenium, BY_ID_CARD_BUTTON, selector_text='By ID')
    verify_is_visible(selenium, FILE_CARD_TITLE, selector_text='Add compounds & data')
    verify_is_visible(selenium, FILE_CARD_BUTTON, selector_text='From File')
    verify_is_visible(selenium, DATA_COLUMNS_CARD_TITLE, selector_text='Add more')
    verify_is_visible(selenium, DATA_COLUMNS_CARD_BUTTON, selector_text='Data Columns')

    # Click on 'By Structure' button
    dom.click_element(selenium, BY_STRUCTURE_CARD_BUTTON)
    verify_is_visible(selenium, REALTIME_PROPERTIES_PANE)

    # Click on 'By ID' button
    dom.click_element(selenium, BY_ID_CARD_BUTTON)
    verify_is_visible(selenium, SEARCH_BY_ID_TEXTAREA)

    # Click on 'From File' button
    dom.click_element(selenium, FILE_CARD_BUTTON)
    verify_is_visible(selenium, IMPORT_FILE_BUTTON)

    # Click on 'Data Columns' button
    dom.click_element(selenium, DATA_COLUMNS_CARD_BUTTON)
    verify_is_visible(selenium, COLUMN_TREE_PICKER)
