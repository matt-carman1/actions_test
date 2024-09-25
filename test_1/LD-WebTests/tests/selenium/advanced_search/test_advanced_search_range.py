"""
Testing that the Adv query feature works with Range condition:
"""
import pytest

from helpers.change import actions_pane, advanced_search_actions, range_actions
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, QUERY_RANGE_UPPER_BOX, QUERY_RANGE_UPPER_AUTO_BUTTON, AUTO_UPDATE_CHECKED
from helpers.selection.grid import Footer
from helpers.verification import grid, advanced_search
from library import dom
import time


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_search_range(selenium):
    """
    Testing that the Adv query feature works with Range condition:
    :param selenium: Selenium webdriver
    """

    # Define test variables column_name is what we see in the D&C Tree and the displayed_column_name is what we see
    # when the column is added to the LR and has observation
    column_name = 'Serotonin 2a (5-HT2a) receptor (IC50)'
    displayed_column_name = '{} [uM]'.format(column_name)
    first_query_expected_result = {
        'ID': [
            'CHEMBL104',
            'CHEMBL1065',
        ],
        displayed_column_name: [
            '=11.14',
            '=0.013',
        ]
    }
    second_query_expected_result = {'ID': ['CHEMBL1065',], displayed_column_name: ['=0.013',]}

    # Open the Advanced Query Tab
    actions_pane.open_add_compounds_panel(selenium)
    actions_pane.open_advanced_search(selenium)

    # Turn auto update on
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    grid.verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    # Add range query and search
    advanced_search_actions.add_query(selenium, column_name)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify first query result
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
    grid.verify_grid_contents(selenium, first_query_expected_result)
    advanced_search.verify_active_search_callout(selenium, 2)

    # Stop search
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)

    # Update range and search
    condition_box = advanced_search_actions.get_query(selenium, column_name)
    advanced_search_actions.set_query_range(condition_box, upper_limit=3)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify second query result
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(1)})
    grid.verify_grid_contents(selenium, second_query_expected_result)
    advanced_search.verify_active_search_callout(selenium, 1)

    # Stop search
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)

    # Reset range to auto and search
    range_actions.set_range_to_auto_or_infinity(selenium,
                                                condition_box,
                                                QUERY_RANGE_UPPER_AUTO_BUTTON,
                                                hover_element_selector=QUERY_RANGE_UPPER_BOX)
    time.sleep(1)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify reseting to infinity gives first query result
    grid.verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
    grid.verify_grid_contents(selenium, first_query_expected_result)
    advanced_search.verify_active_search_callout(selenium, 2)

    # Stop search
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
