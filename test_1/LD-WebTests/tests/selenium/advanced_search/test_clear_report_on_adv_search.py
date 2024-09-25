"""
Selenium test for the Clear report on Search functionality on Advanced Search
"""

import pytest
from helpers.change.advanced_search_actions import add_query, get_query, set_query_range
from helpers.change.grid_column_menu import sort_grid_by
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    CLEAR_REPORT_CHECKBOX, CLEAR_REPORT_NOT_CHECKED, CLEAR_REPORT_CHECKED, AUTO_UPDATE_CHECKED
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.grid import Footer
from helpers.verification.grid import check_for_butterbar
from helpers.verification.grid import verify_footer_values, verify_column_contents, \
    verify_visible_columns_in_live_report, verify_is_visible
from helpers.verification import element
from library import dom, base

live_report_to_duplicate = {'livereport_name': "Test Reactants - Halides", 'livereport_id': '2554'}
test_project_id = '4'


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_clear_report_on_adv_search(selenium):
    """
    Selenium test for the Clear report on Search functionality in Adv Search
    :param selenium: Selenium Webdriver
    """

    # Define test variables
    column_name = 'PQR Permeability-Efflux (ABSORPTIVE_QUOTIENT)'
    column_list = [
        'Compound Structure', 'ID', 'All IDs', 'Rationale', 'Lot Scientist',
        'PQR Permeability-Efflux (ABSORPTIVE_QUOTIENT)'
    ]

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and Clear report on search
    add_query(selenium, column_name)
    dom.click_element(selenium, CLEAR_REPORT_CHECKBOX)
    verify_is_visible(selenium, CLEAR_REPORT_CHECKED)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)

    # Verification of the butterbar message
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)

    sort_grid_by(selenium, 'ID')
    # Verify R-groups are added to the LR
    verify_footer_values(
        selenium, {
            Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(4),
            Footer.COLUMN_ALL_COUNT_KEY: Footer.COLUMN_ALL_COUNT_VALUE.format(6)
        })
    verify_column_contents(selenium, 'ID', ['V046192', 'V055779', 'V055780', 'V055783'])
    verify_visible_columns_in_live_report(selenium, column_list)

    # Add range condition and Clear report on search
    condition_box = get_query(selenium, column_name)
    set_query_range(condition_box, lower_limit=0, upper_limit=1)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)
    base.click_ok(selenium)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=True)
    check_for_butterbar(selenium, notification_text='Removing all and Searching for compounds...', visible=False)

    # Verify compounds are added to the LR
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
    verify_column_contents(selenium, 'ID', ['V046192', 'V055780'])
    verify_visible_columns_in_live_report(selenium, column_list)

    # Verify that when we click the AUTO_UPDATE_CHECKBOX the other checkbox is unchecked
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)
    element.verify_is_visible(selenium, CLEAR_REPORT_NOT_CHECKED)
