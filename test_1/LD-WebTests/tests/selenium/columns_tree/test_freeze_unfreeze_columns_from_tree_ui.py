import pytest

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_management_ui import select_multiple_column_labels
from helpers.selection.column_tree import COLUMNS_TREE_LIVEREPORT_TAB, LIVEREPORT_COLUMN_MANAGER_BUTTON, \
    LIVEREPORT_COLUMN_CHECKBOX_LABEL, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, \
    LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, LIVEREPORT_COLUMN_LIST_FREEZE_LINE
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import verify_frozen_columns_in_grid, verify_frozen_columns_in_column_mgmt_ui
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui
from library import dom

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_freeze_unfreeze_columns_from_tree_ui(selenium):
    """
    Test Freezing and Unfreezing Columns via Columns Management UI.
    1. The Unfreeze button is disabled if no column is selected.
    2. freeze hidden columns
    3. The 'freeze line' only appears once one column is frozen.
    4. When multiple selected columns are frozen, the frozen columns should move immediately above the freeze line in
       whatever order they were listed below, ignoring the gaps
    5. If you unfreeze ColumnB and then unfreeze ColumnA separately, each new click adds to the top, it looks like:
        ----------
        ColumnA
        ColumnB
    :param selenium: Selenium Webdriver
    """

    # Navigate to the LiveReport tab in D&C Tree
    open_add_data_panel(selenium)
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)

    # ----- CHECK THAT THE "UNFREEZE" BUTTON IS DISABLED WITHOUT ANY SELECTION ----- #
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, selector_text="Unfreeze")

    # ----- CHECK THAT THE "ID" COLUMN IS FROZEN BY DEFAULT AND CHECK PRESENCE OF FREEZE LINE ----- #
    verify_is_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, selector_text='ID')
    verify_is_visible(selenium, LIVEREPORT_COLUMN_LIST_FREEZE_LINE)

    # ----- FREEZE HIDDEN COLUMN "Lot Date Registered" ----- #
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='Lot Date Registered')
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Freeze')
    verify_is_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, selector_text='Lot Date Registered')

    # ----- FREEZE COLUMNS SELECTIVELY ----- #
    select_multiple_column_labels(selenium, 'HBD (HBD)', 'Rationale')
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Freeze')

    # Verify that the order of frozen columns is chronological.
    expected_frozen_columns = ['ID', 'Lot Date Registered', 'Rationale', 'HBD (HBD)']
    verify_frozen_columns_in_column_mgmt_ui(selenium, expected_frozen_columns)

    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID', 'Rationale', 'HBD (HBD)'])

    # ----- UNFREEZE SOME COLUMNS ----- #
    # As the selection stays for the last frozen columns we are taking advantage of it and unfreezing it now.
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Unfreeze')
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID'])

    # Unfreeze columns one-by-one and verify the order after unfreezing
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, text='ID', exact_text_match=True)
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Unfreeze')
    verify_is_not_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, selector_text='ID')
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, text='Lot Date Registered')
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Unfreeze')
    verify_is_not_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, selector_text='Lot Date Registered')

    # Verifying that the order for Column labels in Columns Management UI is correct after unfreezing all.
    expected_columns_order_list = [
        'Lot Date Registered', 'ID', 'Rationale', 'HBD (HBD)', 'All IDs', 'Lot Scientist', 'HBA (HBA)', 'PSA (PSA)',
        'AlogP (AlogP)'
    ]
    verify_columns_in_column_mgmt_ui(selenium, expected_columns_order_list)
    verify_frozen_columns_in_grid(selenium, ['Compound Structure'])
