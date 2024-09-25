"""
Selenium test that the Adv query feature works on defined FFC's
"""
import pytest

from helpers.change.advanced_search_actions import add_query, get_query
from helpers.change.autosuggest_actions import set_autosuggest_items, remove_autosuggest_bubble_value
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, CLEAR_REPORT_CHECKED, \
    CLEAR_REPORT_CHECKBOX
from helpers.selection.grid import Footer
from helpers.verification.grid import verify_column_contents, verify_footer_values, verify_is_visible, \
    check_for_butterbar
from library import dom, base


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_adv_query_on_bool_ffc(selenium):
    """
    Testing that the Adv query works with boolean FFC's:

    a. Performed a defined, true, false search on a boolean type FFC.
    b. Verified that the rows returned are as expected.
    :param selenium: Selenium webdriver
    """

    # Define test variables
    boolean_ffc_column = 'Boolean - published'

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and search
    add_query(selenium, boolean_ffc_column)

    # Set value "true" in query
    bool_ffc_query = get_query(selenium, boolean_ffc_column)
    set_autosuggest_items(bool_ffc_query, ["true"])

    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verification of the butterbar message
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Searching for compounds...', visible=False)

    # Three way verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-031437', 'CRA-032370'])

    remove_autosuggest_bubble_value(selenium, bool_ffc_query, "true")

    # Setting value of "false"
    set_autosuggest_items(bool_ffc_query, ["false"])
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
    verify_column_contents(selenium, 'ID', ['CRA-031137'])

    remove_autosuggest_bubble_value(selenium, bool_ffc_query, "false")

    # Setting value as (defined)
    set_autosuggest_items(bool_ffc_query, ["(defined)"])
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)

    # Verification of the butterbar message
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)

    # Verification of the compounds returned
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(3),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['CRA-031137', 'CRA-031437', 'CRA-032370'])

    # Skipping validation of a couple of more use cases:
    # a. (undefined) - undefined boolean search is not a valid search item
    # b. inverted (defined) -  search would bring all compounds present in the db and increase time of the test and
    # Overload/slow-down the small build nodes
