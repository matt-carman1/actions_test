import pytest

from helpers.change.actions_pane import open_add_data_panel
from helpers.verification.grid import verify_footer_values
from helpers.change.columns_management_ui import hide_columns_contiguously, hide_columns_selectively, \
    show_columns_selectively, show_columns_contiguously
from helpers.verification.element import verify_is_visible
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui
from helpers.selection.column_tree import COLUMNS_TREE_LIVEREPORT_TAB, LIVEREPORT_COLUMN_LABEL_ID_, \
    LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, LIVEREPORT_COLUMN_MANAGER_BUTTON
from library import dom

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_show_hide_columns_from_tree_ui(selenium):
    """
    Test for the Columns Management UI:
    1. check that all the columns in the LiveReport show up in the new Columns Management UI.
    2. Hide columns (a) By clicking on checkbox (b) Selecting using ctrl key (c) Selecting using shift key
    3. Show Columns (a) Selecting using ctrl key (b) Selecting using shift key

    :param selenium: Selenium Webdriver
    """
    # List of visible columns in the LiveReport
    expected_columns_in_live_report = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Date Registered', 'STABILITY-PB-PH 7.4 (%Rem@2hr)',
        'Clearance (undefined)', 'CYP450 2C19-LCMS (%INH)', 'Solubility (undefined)'
    ]

    # ----- CHECK ALL THE COLUMNS IN THE LR SHOW UP IN THE NEW COLUMN MANAGEMENT UI ----- #

    # Navigate to the LiveReport tab in D&C Tree
    open_add_data_panel(selenium)
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)

    # Verify the Column Management UI lists all the columns in the LR
    verify_columns_in_column_mgmt_ui(selenium, expected_columns_in_live_report)

    # Check that the "Hide" button is disabled without any selection
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, selector_text="Hide")

    # ----- HIDE COLUMNS USING DIFFERENT METHODS ----- #

    # Hide column "Lot Scientist" by clicking on the checkbox and verify footer values
    addable_column_id_for_lot_scientist = '28'
    dom.click_element(selenium, LIVEREPORT_COLUMN_LABEL_ID_.format(addable_column_id_for_lot_scientist))
    verify_footer_values(selenium, {'column_all_count': '7 Columns', 'column_hidden_count': '3 Hidden'})

    # Select using Ctrl key and hide columns using "Hide" button and verify footer values
    hide_columns_selectively(selenium, 'ID', 'Rationale')
    # Checking that the Hide button has changed to "Show". This would act as the wait before checking the grid footer.
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Show")
    verify_footer_values(selenium, {'column_all_count': '5 Columns', 'column_hidden_count': '5 Hidden'})

    # Select using shift key and hide columns using "Hide" button and verify footer values
    hide_columns_contiguously(selenium, start_column="Solubility (undefined)", end_column="Clearance (undefined)")
    # Checking that the Hide button has changed to "Show". This would act as the wait before checking the grid footer.
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Show")
    verify_footer_values(selenium, {'column_all_count': '2 Columns', 'column_hidden_count': '8 Hidden'})

    # ----- SHOWS COLUMNS USING DIFFERENT METHODS ----- #

    # Select some hidden column labels using ctrl/cmd key and click on "Show" button and verify footer values
    show_columns_selectively(selenium, 'ID', 'Solubility (undefined)')
    # Checking that the Show button has changed to "Hide". This would act as the wait before checking the grid footer.
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Hide")
    verify_footer_values(selenium, {'column_all_count': '4 Columns', 'column_hidden_count': '6 Hidden'})

    # Show column "Add IDs" by clicking on the checkbox and verify footer values
    addable_column_id_for_lot_scientist = '1227'
    dom.click_element(selenium, LIVEREPORT_COLUMN_LABEL_ID_.format(addable_column_id_for_lot_scientist))
    verify_footer_values(selenium, {'column_all_count': '5 Columns', 'column_hidden_count': '5 Hidden'})

    # Select all column labels using shift key and click on "Show" button and verify footer values
    show_columns_contiguously(selenium, start_column='Rationale', end_column='CYP450 2C19-LCMS (%INH)')
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Hide")
    verify_footer_values(selenium, {'column_all_count': '10 Columns'})
