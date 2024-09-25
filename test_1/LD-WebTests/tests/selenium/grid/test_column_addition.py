import pytest

from helpers.change.columns_action import add_column_by_name, add_column_by_expanding_nodes
from helpers.change.actions_pane import open_add_data_panel
from helpers.flows.add_compound import search_by_id
from helpers.verification.grid import check_for_butterbar, verify_footer_values
from helpers.selection.grid import GRID_FOOTER_COLUMN_ALL_COUNT, GRID_GROUP_HEADER_CELL
from helpers.selection.column_tree import (ADD_TO_LIVEREPORT_TOOLTIP_BUTTON, COLUMN_TREE_PICKER_TEXT_NODE,
                                           COLUMN_TREE_PICKER_NODE_TEXT_AREA, COLUMN_TREE_ADD_COLUMNS_BUTTON,
                                           COLUMN_TREE_PICKER_TEXT_NODE_HIGHLIGHTED, COLUMN_TREE_PICKER_TOOLTIP)
from library import dom, utils, simulate, wait
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.change.data_and_columns_tree import clear_column_tree_search, scroll_column_tree_to_top, search_column_tree


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures('new_live_report')
def test_column_addition(selenium):
    """
    Test for adding columns(Model column, Freeform column, MPO column and multiple columns):
    1. searching and clicking on "Add Columns" button
    2. using 'Add to LiveReport' button from tooltip
    3. navigating through D&C Tree nodes and double click on column
    4. using + button in D&C Tree
    Verifying the addition of columns using footer column count
    Verifying the columns in Column Management UI
    :param selenium: a fixture that returns Selenium Webdriver
    :return:
    """
    mpo_column_name = '(Global) Category'
    mpo_desirability_score_column_group = 'Category Desirability Scores and Number of Missing Inputs'
    ffc_column_name = 'Published Freeform Text Column'
    model_column = 'CorpID String'
    assay_parent_column = 'A431'

    # adding compound using search by id
    search_by_id(selenium, 'CHEMBL1049')

    open_add_data_panel(selenium)

    # getting the default column count from LR using footer
    initial_column_count = utils.get_first_int(dom.get_element(selenium, GRID_FOOTER_COLUMN_ALL_COUNT).text)

    # ----- searching and clicking on "Add Columns" button ----- #
    # adding MPO column to the LR
    dom.click_element(selenium,
                      COLUMN_TREE_PICKER_TEXT_NODE,
                      text='Multi-Parameter Optimization',
                      exact_text_match=True)
    wait.until_visible(selenium,
                       COLUMN_TREE_PICKER_TEXT_NODE_HIGHLIGHTED,
                       text='Multi-Parameter Optimization',
                       timeout=10)
    dom.click_element(selenium, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=mpo_column_name, exact_text_match=True)
    dom.click_element(selenium, COLUMN_TREE_ADD_COLUMNS_BUTTON)

    # collapse MPO accordion
    dom.click_element(selenium,
                      COLUMN_TREE_PICKER_TEXT_NODE,
                      text='Multi-Parameter Optimization',
                      exact_text_match=True)

    # verifying addition of MPO column
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 3)})

    # ----- using 'Add to LiveReport' button from tooltip ----- #
    # adding FFC column to the LR
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Freeform Columns', exact_text_match=True)
    wait.until_visible(selenium, COLUMN_TREE_PICKER_TEXT_NODE_HIGHLIGHTED, text='Freeform Columns', timeout=10)

    # Search column tree and hover over new ffc
    # Note we wait for to update to the search by checking that Other Columns is not visible
    # This is necessary to avoid attempting to hover over the ffc while it's offscreen
    search_column_tree(selenium, ffc_column_name)
    wait.until_not_visible(selenium, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text="Other Columns")
    simulate.hover(
        selenium,
        dom.get_element(selenium, COLUMN_TREE_PICKER_NODE_TEXT_AREA, text=ffc_column_name, exact_text_match=True))

    # Note (absingh): move to the center of the tooltip first so that the tooltip doesn't disappear while the cursor is
    # travelling
    simulate.hover(selenium, dom.get_element(selenium, COLUMN_TREE_PICKER_TOOLTIP))
    dom.click_element(selenium, ADD_TO_LIVEREPORT_TOOLTIP_BUTTON)
    clear_column_tree_search(selenium)

    # collapse FFC accordion
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Freeform Columns', exact_text_match=True)

    # verifying addition of FFC column
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 4)})

    # ----- navigating through D&C Tree nodes and double click on column ----- #
    # adding model column to the LR
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Computational Models', exact_text_match=True)
    wait.until_visible(selenium, COLUMN_TREE_PICKER_TEXT_NODE_HIGHLIGHTED, text='Computational Models', timeout=10)
    add_column_by_expanding_nodes(selenium, ['User Defined', 'BS Models', model_column])

    # collapse Computational Models accordion
    scroll_column_tree_to_top(selenium)
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Computational Models', exact_text_match=True)

    # verifying addition of Model Column
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 5)})

    # ----- using + button in D&C Tree ----- #
    # adding assay parent column. This will add multiple columns (3 in this case) to the LR
    add_column_by_name(selenium, assay_parent_column)
    clear_column_tree_search(selenium)

    # Verify butter bar appears and goes away
    check_for_butterbar(selenium, 'Adding columns to LiveReport', visible=False)

    # verifying addition of assay parent column
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 8)})

    # verify for Desirability Score column group added
    group_header_element = dom.get_element(selenium, GRID_GROUP_HEADER_CELL)
    assert group_header_element.text == mpo_desirability_score_column_group, \
        "No Group with name {} was found, instead found group with name {}".format(mpo_desirability_score_column_group,
                                                                                   group_header_element.text)
    expected_column_names = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Category',
        'Category Desirability Scores and Number of Missing Inputs', 'Lot Scientist Desirability',
        'Number of missing inputs', ffc_column_name, '{} ({})'.format(model_column, model_column),
        '{} (Activity)'.format(assay_parent_column), '{} (ED50)'.format(assay_parent_column),
        '{} (IC50)'.format(assay_parent_column)
    ]

    # verify columns in Column Management UI
    # deliberately decided to just verify columns from Col Mgmt UI to avoid scrolling and increasing the steps in test
    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_names)
