from library import dom

from helpers.change.actions_pane import close_add_data_panel
from helpers.change.columns_management_ui import open_column_mgmt_panel, select_multiple_column_labels
from helpers.change.grid_columns import drag_and_drop_columns_in_grid
from helpers.selection.column_tree import LIVEREPORT_COLUMN_MANAGER_BUTTON
from helpers.verification.grid import verify_frozen_columns_in_grid
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


def test_drag_drop_columns_in_grid(selenium, duplicate_live_report, open_livereport):
    """
    Test to drag and drop columns in the grid and verify the order through Column Management UI

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates the live report
    :param open_livereport: a fixture which opens the live report
    """
    # Freezing two columns
    open_column_mgmt_panel(selenium)
    select_multiple_column_labels(selenium, 'Rationale', 'HBD (HBD)')
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Freeze')
    close_add_data_panel(selenium)

    # Drag and Drop within frozen columns
    drag_and_drop_columns_in_grid(selenium, source_column_name='Rationale', dest_column_name='HBD (HBD)')
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID', 'HBD (HBD)', 'Rationale'])

    # Drag and Drop a column to left of Freeze line
    """NOTE: When dragging an unfrozen column on the grid past the freeze line towards frozen columns,
             dragged unfrozen column will be dropped and takes place of the first unfrozen column"""
    drag_and_drop_columns_in_grid(selenium, source_column_name='All IDs', dest_column_name='ID')
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'ID', 'HBD (HBD)', 'Rationale'])

    # Drag and Drop a column to right of the Freeze line
    """NOTE: When dragging a frozen column on the grid past the freeze line towards unfrozen columns,
             dragged frozen column will be dropped and takes place of the last frozen column"""
    drag_and_drop_columns_in_grid(selenium, source_column_name='ID', dest_column_name='All IDs')
    verify_frozen_columns_in_grid(selenium, ['Compound Structure', 'HBD (HBD)', 'Rationale', 'ID'])

    # Drag and Drop within unfrozen columns
    drag_and_drop_columns_in_grid(selenium, source_column_name='HBA (HBA)', dest_column_name='PSA (PSA)')

    # Drag and Drop column to right end of the LR
    drag_and_drop_columns_in_grid(selenium, source_column_name='Lot Scientist', dest_column_name='AlogP (AlogP)')

    # Verify columns order in the column management UI
    open_column_mgmt_panel(selenium)
    expected_column_list = [
        'HBD (HBD)', 'Rationale', 'ID', 'All IDs', 'Lot Date Registered', 'PSA (PSA)', 'HBA (HBA)', 'AlogP (AlogP)',
        'Lot Scientist'
    ]
    verify_columns_in_column_mgmt_ui(selenium, expected_columns=expected_column_list)
