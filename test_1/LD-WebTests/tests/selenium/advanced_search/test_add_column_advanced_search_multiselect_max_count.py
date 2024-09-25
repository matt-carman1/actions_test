import pytest

from helpers.change.actions_pane import open_add_compounds_panel, open_advanced_search
from helpers.change.advanced_search_actions import remove_all_search_conditions
from helpers.change.columns_action import select_multiple_contiguous_columns_in_column_tree, \
    select_multiple_columns_in_column_tree, clear_column_selection
from helpers.selection.advanced_search import ADVANCED_SEARCH_ADD_COLUMNS_BUTTON, ADVANCED_QUERY_COLUMN_SELECTOR
from helpers.selection.modal import MODAL_DIALOG_BODY, MODAL_DIALOG, MODAL_DIALOG_HEADER
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values
from library import dom
from library.base import click_ok

# This is FF which set maximum count of columns that can be added to the Advanced query using colum picker multi-select
LD_PROPERTIES = {'ADD_COLUMN_ADVANCED_SEARCH_MULTISELECT_MAX_COUNT': 3}


@pytest.mark.k8s_defect(reason="SS-42607: flakiness due to issues finding columns in the column tree")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures('customized_server_config')
def test_add_column_advanced_search_multiselect_max_count(selenium):
    """
    This will check whether ADD_COLUMN_ADVANCED_SEARCH_MULTISELECT_MAX_COUNT FF working properly.

    1. Adding greater number of columns than FFC value and verify column not added
    2. Adding fewer number of columns than FF value and verify added columns
    3. Adding equal number of column as FF value and verify added columns
    :param selenium: Selenium Webdriver
    """
    # Open advanced search panel
    open_add_compounds_panel(selenium)
    open_advanced_search(selenium)

    # ----- Adding greater number of columns than FF value and verify columns not added ----- #
    # opening D&C tree in advanced search
    dom.click_element(selenium, ADVANCED_QUERY_COLUMN_SELECTOR)

    columns_in_more_case = [
        '10 Atom MCSS Clustering', '10 Bond MCSS Clustering', '11 Atom MCSS Clustering', '11 Bond MCSS Clustering'
    ]
    # adding columns to advanced search
    select_multiple_contiguous_columns_in_column_tree(
        selenium, {'Computed Properties': {
            'Chemaxon LibMCS': [columns_in_more_case[0], columns_in_more_case[3]]
        }})
    dom.click_element(selenium, ADVANCED_SEARCH_ADD_COLUMNS_BUTTON)

    # verification for too many columns dialogue and message
    verify_is_visible(selenium, MODAL_DIALOG)
    verify_is_visible(selenium, selector=MODAL_DIALOG_HEADER, selector_text='Too many Columns Selected')
    verify_is_visible(selenium,
                      selector=MODAL_DIALOG_BODY,
                      selector_text='More than 3 columns would be added to the Advanced Search, please select fewer '
                      'columns ')

    click_ok(selenium)
    # verify new columns not added, here 5 is default column count
    verify_footer_values(selenium, {'column_all_count': '5 Columns'})

    # ----- Adding fewer number of columns than FF value ----- #
    # opening D&C tree in advanced search
    dom.click_element(selenium, ADVANCED_QUERY_COLUMN_SELECTOR)
    # clearing previous selection
    clear_column_selection(selenium)
    columns_in_less_case = ['Assay Name', 'Compound Live Report']
    # adding columns to advanced search
    select_multiple_columns_in_column_tree(selenium, {'Other Columns': columns_in_less_case})
    dom.click_element(selenium, ADVANCED_SEARCH_ADD_COLUMNS_BUTTON)

    # verify added columns
    verify_footer_values(selenium, {'column_all_count': '7 Columns'})

    remove_all_search_conditions(selenium)

    # ----- Adding equal number of columns as FF value ----- #
    # opening D&C Tree in advanced search
    dom.click_element(selenium, ADVANCED_QUERY_COLUMN_SELECTOR)

    # adding columns to advanced search
    select_multiple_contiguous_columns_in_column_tree(
        selenium, {'Computational Models': {
            'Misc': ['A10 (undefined)', 'A12 (undefined)']
        }})
    dom.click_element(selenium, ADVANCED_SEARCH_ADD_COLUMNS_BUTTON)

    # verify added columns
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})
