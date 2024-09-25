import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search, open_add_data_panel
from helpers.change.advanced_search_actions import remove_all_search_conditions
from helpers.change.columns_action import select_multiple_contiguous_columns_in_column_tree, \
    select_multiple_columns_in_column_tree
from helpers.selection.advanced_search import ADVANCED_SEARCH_ADD_COLUMNS_BUTTON, ADVANCED_SEARCH_TEXTBOX
from helpers.verification.advanced_search import verify_added_columns_in_advanced_query_panel
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from library import dom


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_multiselect_columns_in_adv_search(selenium):
    """
    Test for multi Select columns in D&C Tree
    1. Select multiple columns sequentially and verify the columns with order in advanced search panel
    2. Select Multiple columns from different sections and verify the columns with order in advanced search panel
    3. Verify added columns in livereport

    :param selenium: a fixture that returns Selenium Webdriver
    """
    # Open the Advanced Query Tab
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # ----- Select multiple columns using Shift+Click and verify the columns with order in advanced search panel ----- #
    # Select multiple columns using Shift+Click, Here passing columns without any order
    dom.click_element(selenium, ADVANCED_SEARCH_TEXTBOX)
    select_multiple_contiguous_columns_in_column_tree(selenium,
                                                      {'Other Columns': ['Assay Name', 'Compound Live Report']})
    # Adding columns to advanced search query panel
    dom.click_element(selenium, ADVANCED_SEARCH_ADD_COLUMNS_BUTTON)

    # Verify whether columns added to advances search query panel with D&C tree order.
    verify_added_columns_in_advanced_query_panel(selenium,
                                                 ['Assay Name', 'Common Chemical Name', 'Compound Live Report'])

    remove_all_search_conditions(selenium)

    # Opening D&C Tree in Advanced Search
    dom.click_element(selenium, ADVANCED_SEARCH_TEXTBOX)
    # ----- Select Multiple columns from different sections and verify columns with order in adv search panel ----- #
    # Select columns from different sections
    select_multiple_columns_in_column_tree(selenium, {'Computational Models': {'Misc': ['A1 (undefined)']}})
    # Adding columns to advanced search query panel
    dom.click_element(selenium, ADVANCED_SEARCH_ADD_COLUMNS_BUTTON)

    # Verify whether columns added to advances search query panel with D&C tree order.
    verify_added_columns_in_advanced_query_panel(
        selenium, ['A1 (undefined)', 'Assay Name', 'Common Chemical Name', 'Compound Live Report'])

    # ----- Verify added columns in livereport ----- #
    open_add_data_panel(selenium)
    verify_visible_columns_from_column_mgmt_ui(selenium, [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Assay Name', 'Common Chemical Name', 'Compound Live Report',
        'A1 (undefined)'
    ])
