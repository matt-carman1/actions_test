"""
Testing that the Adv query feature works with 3D cols
"""
import pytest

from helpers.change import actions_pane, advanced_search_actions
from helpers.change.advanced_search_actions import get_query
from helpers.change.autosuggest_actions import set_autosuggest_items
from helpers.change.grid_column_menu import remove_column
from helpers.selection.advanced_search import SEARCH_AND_ADD_COMPOUNDS_BUTTON, AUTO_UPDATE_CHECKBOX, \
    ADV_QUERY_STOP_SEARCH, AUTO_UPDATE_CHECKED
from helpers.selection.grid import PYMOL_VIEW_TEXT, Footer
from helpers.verification.grid import verify_column_contents, verify_footer_values, verify_is_visible
from library import dom, simulate


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_advanced_search_3d(selenium):
    """
    Testing that the Adv query feature works with 3d columns
    :param selenium: Selenium webdriver
    """

    # Defining a callback for getting 3D cell text
    def get_3d_cell_text(cell):
        simulate.hover(selenium, cell)
        cell_item = dom.get_element(cell, PYMOL_VIEW_TEXT)
        return cell_item.text

    # Open the Advanced Query Tab
    actions_pane.open_add_compounds_panel(selenium)
    actions_pane.open_advanced_search(selenium)

    # Turn auto update on
    dom.click_element(selenium, AUTO_UPDATE_CHECKBOX)
    verify_is_visible(selenium, AUTO_UPDATE_CHECKED)

    # ----- ADD FIRST QUERY AND SEARCH ----- #
    three_d_model_column_name = 'Fake 3D model (3D)'
    expected_ids_for_three_d_model = [
        'CRA-032665', 'CRA-032718', 'CRA-032845', 'CRA-034042', 'V046171', 'V048220', 'V055836'
    ]

    advanced_search_actions.add_query(selenium, three_d_model_column_name)
    # Set value "(defined)" in text query
    query = get_query(selenium, three_d_model_column_name)
    set_autosuggest_items(query, ["(defined)"])
    dom.click_element(selenium, SEARCH_AND_ADD_COMPOUNDS_BUTTON)

    # Verify query result
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(7)})
    verify_column_contents(selenium, 'ID', expected_ids_for_three_d_model)
    verify_column_contents(selenium, three_d_model_column_name, ['View 3D'] * 7, get_3d_cell_text)

    # Stop search and clear queries and the column from the grid as well.
    dom.click_element(selenium, ADV_QUERY_STOP_SEARCH)
    remove_column(selenium, three_d_model_column_name)
    advanced_search_actions.remove_all_search_conditions(selenium)
