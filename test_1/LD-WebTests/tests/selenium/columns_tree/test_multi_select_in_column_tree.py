import pytest

from helpers.change.actions_pane import open_add_data_panel, close_add_data_panel
from helpers.change.columns_action import select_multiple_columns_in_column_tree
from helpers.flows.columns_tree import select_and_add_multiple_columns_from_column_tree
from helpers.selection.column_tree import COLUMN_TREE_PICKER_TEXT_NODE, COLUMN_TREE_ADD_COLUMNS_BUTTON, \
    PARTIALLY_SELECTED_COLUMN_NODE, SELECTED_COLUMN_NODE
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values
from library import dom
from library.utils import is_k8s


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
def test_multi_select_in_column_tree(selenium):
    """
    Test for multi Select columns in D&C Tree
    1. Select multiple columns sequentially and add them to LR by 'Add Columns' button
    2. Select Multiple columns from different sections and add them to LR by 'Add Columns' button
    3. Verification of Selection Criteria for parent columns
    4. Verifying added columns in LR
    :param selenium: a fixture that returns Selenium Webdriver
    :return:
    """
    # opening D&C Tree
    open_add_data_panel(selenium)

    # ----- Select multiple columns sequentially and add them to LR by 'Add Columns' button ----- #
    # select multiple columns contiguously using Shift+Click
    select_and_add_multiple_columns_from_column_tree(selenium, {'Other Columns': ['Lot Nb Page', 'Lot Number']},
                                                     is_contiguous=True)

    # verification of columns by columns count in footer
    verify_footer_values(selenium, {'column_all_count': '8 Columns'})

    # ----- Select Multiple columns from different sections and add them to LR by 'Add Columns' button ----- #
    # Selecting multiple columns in different sections
    select_multiple_columns_in_column_tree(
        selenium, {
            'Experimental Assays': {
                'Chembl': {
                    'A-431 (Epidermoid carcinoma cells)': [
                        'A-431 (Epidermoid carcinoma cells) (EC50)', 'A-431 (Epidermoid carcinoma cells) (IC50)',
                        'A-431 (Epidermoid carcinoma cells) (Inhibition)'
                    ]
                }
            },
            'Multi-Parameter Optimization':
                ['(Global) Higher is Good', '(Global) Lower is Good', '(JS Testing) (Global) Pose']
        })

    # adding selected column to LR by 'Add Columns' button
    dom.click_element(selenium, COLUMN_TREE_ADD_COLUMNS_BUTTON)
    # verification of added columns using columns count in footer
    verify_footer_values(selenium, {'column_all_count': '21 Columns'})

    # ----- Verification of Selection Criteria for parent columns ----- #
    dom.click_element(selenium, COLUMN_TREE_PICKER_TEXT_NODE, text='Experimental Assays', exact_text_match=True)

    # verifying the partial and complete selection after the columns are added to the LR as it also helps us check in
    # a way that the selection is ̥retained even after adding the columns to the LR.
    # Verifying partially selected(few child nodes selected) parent column
    verify_is_visible(selenium, PARTIALLY_SELECTED_COLUMN_NODE, selector_text='Chembl', exact_selector_text_match=True)
    # verifying completely selected(all child nodes selected) parent column
    verify_is_visible(selenium,
                      SELECTED_COLUMN_NODE,
                      selector_text='A-431 (Epidermoid carcinoma cells)',
                      exact_selector_text_match=True)

    # ----- Verifying added columns in LR ----- #
    # ----- New Columns are added in the order(except MPO Desirability columns) they appear in the D&C Tree ----- #
    expected_column_names = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Nb Page', 'Lot Notebook', 'Lot Number',
        'A-431 (Epidermoid carcinoma cells) (EC50)', 'A-431 (Epidermoid carcinoma cells) (IC50)',
        'A-431 (Epidermoid carcinoma cells) (Inhibition)', 'Higher is Good',
        'Higher is Good Desirability Scores and Number of Missing Inputs', 'ABL-TRFRET (Ki) Desirability',
        'Number of missing inputs', 'Lower is Good', 'Lower is Good Desirability Scores and Number of Missing Inputs',
        'BTK-TRFRET (Ki) Desirability', 'Number of missing inputs', '(Global) Pose',
        '(Global) Pose Desirability Scores and Number of Missing Inputs',
        'Fake 3D model with 2 Poses (Docking Score) Desirability', 'Fake 3D model with 2 Poses (3D) Desirability',
        'Number of missing inputs'
    ]

    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_names)

    # closing data panel
    close_add_data_panel(selenium)
