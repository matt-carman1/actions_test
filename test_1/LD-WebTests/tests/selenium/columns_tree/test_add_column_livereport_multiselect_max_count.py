import pytest

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_action import select_multiple_columns_in_column_tree
from helpers.flows.columns_tree import select_and_add_multiple_columns_from_column_tree
from helpers.selection.column_tree import COLUMN_TREE_ADD_COLUMNS_BUTTON
from helpers.selection.grid import GRID_FOOTER_COLUMN_ALL_COUNT
from helpers.selection.modal import MODAL_DIALOG_BODY, MODAL_DIALOG_HEADER
from helpers.verification.data_and_columns_tree import verify_visible_columns_from_column_mgmt_ui
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_footer_values, check_for_butterbar
from library import dom, utils
from library.base import click_ok

# Sets the maximum count of columns that can be added to the LiveReport using column picker multi-select
LD_PROPERTIES = {'ADD_COLUMN_LIVEREPORT_MULTISELECT_MAX_COUNT': '7'}


@pytest.mark.app_defect("SS-42440: Fails to click the add columns buttons")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("new_live_report")
@pytest.mark.usefixtures('customized_server_config')
def test_add_column_livereport_multiselect_max_count(selenium):
    """
    Test to verify the feature flag 'ADD_COLUMN_LIVEREPORT_MULTISELECT_MAX_COUNT'
    1. Selects columns less than the value set for the FF
    4. Verifies columns are added to LR
    5. Selects columns equal to value set for FF
    6. Verifies columns are added to LR
    7. Selects columns greater than the value set for FF
    8. Verifies columns are not added to LR
    :param selenium: Selenium Webdriver
    :return:
    """
    # opening D&C Tree
    open_add_data_panel(selenium)

    # Getting the default column count from LR using footer
    initial_column_count = utils.get_first_int(dom.get_element(selenium, GRID_FOOTER_COLUMN_ALL_COUNT).text)

    # ----- Selects multiple columns, adds them to LR and verifies if columns are added to LR----- #

    # Selecting multiple contiguous columns and adding them to LR
    # Number of columns selected = '6'
    select_and_add_multiple_columns_from_column_tree(selenium, {'Other Columns': ['Assay Name', 'Lot Amount Prepared']},
                                                     is_contiguous=True)

    # Verifying the butterbar disappears before column selection
    check_for_butterbar(selenium, "Adding columns to Live Report")
    check_for_butterbar(selenium, "Adding columns to Live Report", visible=False)
    # verifying columns added by checking the grid-footer
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 6)})

    # Adding columns from multiple nodes
    # Number of columns selected='7'
    select_and_add_multiple_columns_from_column_tree(
        selenium, {
            'Computational Models': {
                'Misc': ['A1 (undefined)', 'A10 (undefined)', 'A11 (undefined)', 'A12 (undefined)']
            },
            'Experimental Assays': {
                'Chembl': {
                    'A-431 (Epidermoid carcinoma cells)': [
                        'A-431 (Epidermoid carcinoma cells) (EC50)', 'A-431 (Epidermoid carcinoma cells) (IC50)',
                        'A-431 (Epidermoid carcinoma cells) (Inhibition)'
                    ]
                }
            }
        })
    check_for_butterbar(selenium, "Adding columns to Live Report")
    check_for_butterbar(selenium, "Adding columns to Live Report", visible=False)
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 13)})

    # Number of columns selected=8
    select_multiple_columns_in_column_tree(
        selenium, {
            'Multi-Parameter Optimization': ['(Global) Category', '(Global) Higher is Good', '(Global) Lower is Good'],
            'Computed Properties': {
                'Physicochemical Descriptors': ['AlogP', 'Chiral Center Count (CC)', 'Ertl PSA', 'Estate', 'HBA']
            }
        })
    # adding columns
    dom.click_element(selenium, COLUMN_TREE_ADD_COLUMNS_BUTTON)

    # verifying the dialog-box header and text
    modal_dialog_header = 'Too many Columns Selected'
    modal_dialog_body_text = 'More than 7 columns would be added to the LiveReport, please select fewer columns '
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, selector_text=modal_dialog_header, exact_selector_text_match=True)
    verify_is_visible(selenium, MODAL_DIALOG_BODY, selector_text=modal_dialog_body_text, exact_selector_text_match=True)
    # Clicking on 'OK' button to close the dialog box
    click_ok(selenium)
    # Verifying that the column value in the footer value remains same.
    verify_footer_values(selenium, {'column_all_count': '{} Columns'.format(initial_column_count + 13)})

    # ----- Verifies the added columns in LR ----- #
    expected_column_names = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Assay Name', 'Common Chemical Name', 'Compound Live Report',
        'Compound Structure Date', 'Lot Alias ID', 'Lot Amount Prepared', 'A1 (undefined)', 'A10 (undefined)',
        'A11 (undefined)', 'A12 (undefined)', 'A-431 (Epidermoid carcinoma cells) (EC50)',
        'A-431 (Epidermoid carcinoma cells) (IC50)', 'A-431 (Epidermoid carcinoma cells) (Inhibition)'
    ]
    # Verifying the columns in the Live Report tab
    verify_visible_columns_from_column_mgmt_ui(selenium, expected_column_names)
