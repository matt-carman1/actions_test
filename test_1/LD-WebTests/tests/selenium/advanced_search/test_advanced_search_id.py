"""
Testing that the Adv query feature works with ID condition and some wild cards:
"""
import pytest

from helpers.change import actions_pane, advanced_search_actions
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, AUTO_UPDATE_CHECKED
from helpers.selection.grid import Footer
from helpers.verification import grid
from library import dom


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_search_id(selenium):
    """
    Testing that the Adv query feature works with ID condition and some wild cards:
    :param selenium: Selenium webdriver
    """

    # Define test variables
    first_query = ['CHEMBL105*']
    second_query = ['CHEMBL100', 'CHEMBL1050']
    first_query_expected_result = [
        'CHEMBL105',
        'CHEMBL1050',
        'CHEMBL1051',
        'CHEMBL1052',
        'CHEMBL1053',
        'CHEMBL1054',
        'CHEMBL1055',
        'CHEMBL1056',
        'CHEMBL1057',
        'CHEMBL1058',
        'CHEMBL1059',
    ]
    second_query_expected_result = ['CHEMBL100', 'CHEMBL1050']

    # Open the Advanced Query Tab
    actions_pane.open_add_compounds_panel(selenium)
    actions_pane.open_advanced_search(selenium)

    # Turn auto update on
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    grid.verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    # Do first query
    advanced_search_actions.add_query_all_id(selenium, first_query)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify first query result
    grid.verify_grid_contents(selenium, {'ID': first_query_expected_result})
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(11)})

    # Stop search and clear queries
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    advanced_search_actions.remove_all_search_conditions(selenium)

    # Do second query
    advanced_search_actions.add_query_all_id(selenium, second_query)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify second query result
    grid.verify_grid_contents(selenium, {'ID': second_query_expected_result})
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
