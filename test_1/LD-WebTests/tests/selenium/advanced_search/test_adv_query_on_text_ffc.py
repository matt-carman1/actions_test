"""
Selenium test that the Adv query feature works on defined text type FFC's
"""
import pytest

from helpers.change.advanced_search_actions import add_query, get_query
from helpers.change.autosuggest_actions import set_autosuggest_items, remove_autosuggest_bubble_value
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, CLEAR_REPORT_CHECKED, \
    CLEAR_REPORT_CHECKBOX
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_column_contents, verify_footer_values, check_for_butterbar, \
    verify_is_visible, verify_grid_contents

from library import dom, base


@pytest.mark.app_defect(reason="SS-32648: Flaky Test on master")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_adv_query_on_text_ffc(selenium):
    """
    Testing that the Adv query works with FFC's:

    a. Performed a Categorical Active Advanced search with "defined" on a text type FFC.
    b. Verified that the results show up as expected.
    c. Performed a defined, true, false search on a boolean type FFC
    d. Verified that the rows returned are as expected.
    :param selenium: Selenium webdriver
    """

    # Define test variables
    text_ffc_column = 'Published Freeform Text Column'
    ffc_values = ['Sample Published Text', 'Sample Data 2']

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and search
    add_query(selenium, text_ffc_column)

    # Set value "(defined)" in text query
    text_ffc_query = get_query(selenium, text_ffc_column)
    set_autosuggest_items(text_ffc_query, ["(defined)"])
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)
    breakpoint()
    # Three way verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_grid_contents(selenium, {'ID': ['V035624', 'V035625'], text_ffc_column: ffc_values})

    remove_autosuggest_bubble_value(selenium, text_ffc_query, '(defined)')

    # Setting value as "Sample Published Text"
    set_autosuggest_items(text_ffc_query, ["Sample Published Text"])
    dom.click_element(selenium, CLEAR_REPORT_CHECKBOX)
    verify_is_visible(selenium, CLEAR_REPORT_CHECKED)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)

    # Verification of the butterbar message
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)

    # Verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_grid_contents(selenium, {'ID': ['V035624'], text_ffc_column: ['Sample Published Text']})
