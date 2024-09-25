import pytest

from helpers.change.columns_management_ui import open_column_mgmt_panel
from helpers.change.grid import switch_to_grid_view
from helpers.change.tile_view import switch_to_tile_view
from helpers.selection.column_tree import LIVEREPORT_NOTIFICATION_MESSAGE
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui
from helpers.verification.element import verify_is_visible

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_notification_msg_on_columnstree_livereporttab_in_tile_view(selenium):
    """
    Test to verify the notification message on LiveReport tab under D&C tree when on Tile view
    1. Duplicate a Live Report
    2. Open D&C tree and navigate to LiveReport tab
    3. Verify the Column Management UI lists all the columns in the LR
    4. Switch to Tile view
    5. Verify notification message 'Please switch to spreadsheet view'
    6. Switch back to Grid view
    7. Verify all the columns displayed

    :param selenium: Selenium Webdriver
    :return:
    """

    notification_msg = 'Please switch to spreadsheet view'

    expected_columns_in_live_report = [
        'ID', 'All IDs', 'Rationale', 'Lot Scientist', 'Lot Date Registered', 'PK_PO_RAT (AUC)',
        'PK_PO_RAT (Absorption)', 'DRC TEST ASSAY (IC50%)', 'Test RPE Formula', 'Test RPE MPO',
        'CorpID String (CorpID String)'
    ]

    # Open D&C Tree and navigate to LiveReport tab
    open_column_mgmt_panel(selenium)

    # Verify the Column Management UI lists all the columns in the LR
    verify_columns_in_column_mgmt_ui(selenium, expected_columns_in_live_report)

    # Switch to Tile view
    switch_to_tile_view(selenium)

    # Verify notification message 'Please switch to spreadsheet view'
    verify_is_visible(selenium, LIVEREPORT_NOTIFICATION_MESSAGE, notification_msg)

    # Switch back to Grid view
    switch_to_grid_view(selenium)

    # Verify all the columns displayed
    verify_columns_in_column_mgmt_ui(selenium, expected_columns_in_live_report)
