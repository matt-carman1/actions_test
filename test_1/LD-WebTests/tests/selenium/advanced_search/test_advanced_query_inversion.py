"""
Testing that the Adv query inversion feature works as expected
"""
import pytest

from helpers.change.advanced_search_actions import add_query, get_query, set_query_range
from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, ADV_QUERY_INVERT, AUTO_UPDATE_CHECKED
from helpers.selection.grid import Footer
from helpers.verification.advanced_search import verify_active_search_callout
from helpers.verification.grid import verify_column_contents, verify_footer_values, verify_is_visible
from library import dom, wait


@pytest.mark.app_defect("SS-42433: More compounds than expected match inversion query")
@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures('customized_server_config')
def test_advanced_query_inversion(selenium):
    """
    Testing that the Adv query inversion feature works as expected. Details:

    a. Performed a range based Active Advanced search and verified the results.
    b. Inverted the query and  ran the search again.
    c. Verified that the results show up as expected.
    :param selenium: Selenium webdriver
    """

    # Define test variables
    column_name = 'HBD'
    displayed_name = column_name + ' (HBD)'
    expected_ids = {
        "first_query_result": ['CRA-032665', 'CRA-032718', 'CRA-032845', 'CRA-034042', 'V044401'],
        "second_query_result": ['V035752', 'V038399', 'V041170', 'V041471', 'V046171', 'V055836']
    }

    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # Add range query and search
    add_query(selenium, column_name, displayed_name)
    condition_box = get_query(selenium, displayed_name)
    set_query_range(condition_box, lower_limit=1, upper_limit=2)

    # Turn auto update on
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify first query result
    wait.until_visible(selenium, ADV_QUERY_STOP_SEARCH)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(5)})
    verify_active_search_callout(selenium, 5)
    verify_column_contents(selenium, 'ID', expected_ids["first_query_result"])

    # Stop search
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    wait.until_loading_mask_not_visible(selenium)

    # Invert the query and execute the search
    dom.click_element(selenium, ADV_QUERY_INVERT)
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify second query result
    wait.until_visible(selenium, ADV_QUERY_STOP_SEARCH)
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(6)})
    verify_active_search_callout(selenium, 6)
    verify_column_contents(selenium, 'ID', expected_ids["second_query_result"])
