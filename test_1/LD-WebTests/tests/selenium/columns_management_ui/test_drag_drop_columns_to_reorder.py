import pytest

from helpers.change.actions_pane import close_add_data_panel, open_add_data_panel
from helpers.change.columns_management_ui import select_multiple_column_labels, \
    group_columns_selectively_via_column_mgmt_ui
from helpers.selection.column_tree import LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED, \
    LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, LIVEREPORT_COLUMN_CHECKBOX_LABEL, LIVEREPORT_COLUMN_LABEL_ID_, \
    COLUMNS_TREE_LIVEREPORT_TAB
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui, \
    verify_grouped_columns_in_column_mgmt_ui
from helpers.verification.element import verify_is_visible
from helpers.verification.grid import verify_frozen_columns_in_column_mgmt_ui, verify_visible_columns_in_live_report
from library import dom, actions

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_drag_drop_columns_to_reorder(selenium):
    """
    Test to reorder columns in Columns Management UI via drag and drop.
    1. Drag-drop to freeze column and verify
    2. Drag-drop to add a column to the group and verify
    3. Drag-drop to order the group and verify
    4.Drag-drop to end of column_list and verify
    :param selenium: Selenium Webdriver
    """

    # Open Column Management UI via Manage Columns… option from the Column menu option
    open_add_data_panel(selenium)
    dom.click_element(selenium, COLUMNS_TREE_LIVEREPORT_TAB)
    verify_is_visible(selenium, COLUMNS_TREE_LIVEREPORT_TAB, selector_text='LiveReport', exact_selector_text_match=True)

    # ----- Drag and Drop to freeze columns ----- #
    # Also including the hidden column tto check edge case testing of reorder hidden columns.
    select_multiple_column_labels(selenium, 'PSA (PSA)', 'Lot Date Registered')
    # Define element corresponding to the selected column labels in Column Mgmt UI(this element will be dragged)
    source_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED, text='PSA (PSA)')
    # Define element where the column label will be dragged onto
    dest_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, text='ID')
    # Perform drag and drop.
    actions.drag_dragover_and_drop(selenium, source_element, dest_element)
    # Verify the columns are dragged such that they are frozen
    expected_frozen_columns = ['Lot Date Registered', 'PSA (PSA)', 'ID']
    verify_frozen_columns_in_column_mgmt_ui(selenium, expected_frozen_columns)

    # ----- Drag and Drop to add a column to a group ----- #
    group_columns_selectively_via_column_mgmt_ui(selenium, 'Group1', 'AlogP (AlogP)')
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='Rationale')
    source_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED, text='Rationale')
    dest_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='AlogP (AlogP)')
    actions.drag_dragover_and_drop(selenium, source_element, dest_element)
    verify_grouped_columns_in_column_mgmt_ui(selenium, ['Rationale', 'AlogP (AlogP)'], group_name='Group1')
    # Dragging the group
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='Group1')
    source_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED, text='Group1')
    dest_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='All IDs')
    actions.drag_dragover_and_drop(selenium, source_element, dest_element)
    # verify the order of columns in Columns Management UI
    expected_column_order = [
        'Lot Date Registered', 'PSA (PSA)', 'ID', 'Group1', 'Rationale', 'AlogP (AlogP)', 'All IDs', 'Lot Scientist',
        'HBA (HBA)', 'HBD (HBD)'
    ]
    verify_columns_in_column_mgmt_ui(selenium, expected_column_order)

    # Show the hidden column which was reordered to check that the reordering performed is intact.
    addable_column_id_for_lot_date_registered = '29'
    dom.click_element(selenium, LIVEREPORT_COLUMN_LABEL_ID_.format(addable_column_id_for_lot_date_registered))

    # ----- Drag and Drop columns to end of column list ----- #
    select_multiple_column_labels(selenium, 'Lot Date Registered', 'PSA (PSA)')
    source_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, text='PSA (PSA)')
    dest_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='HBD (HBD)')
    actions.drag_dragover_and_drop(selenium, source_element, dest_element)
    expected_column_order_two = [
        'ID', 'Group1', 'Rationale', 'AlogP (AlogP)', 'All IDs', 'Lot Scientist', 'HBA (HBA)', 'HBD (HBD)',
        'Lot Date Registered', 'PSA (PSA)'
    ]
    verify_columns_in_column_mgmt_ui(selenium, expected_column_order_two)
    close_add_data_panel(selenium)

    # Verify the visible column order in the grid
    expected_visible_column_order = [
        'Compound Structure', 'ID', 'Group1', 'All IDs', 'Lot Scientist', 'HBA (HBA)', 'HBD (HBD)',
        'Lot Date Registered', 'PSA (PSA)'
    ]
    verify_visible_columns_in_live_report(selenium, expected_visible_column_order)
