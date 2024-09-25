import pytest

from helpers.change.actions_pane import open_add_data_panel
from helpers.change.columns_action import add_column_by_name
from helpers.change.columns_management_ui import hide_columns_selectively, \
    group_columns_selectively_via_column_mgmt_ui, open_column_mgmt_panel
from helpers.selection.column_tree import LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, \
    LIVEREPORT_COLUMN_CHECKBOX_LABEL_GROUPED_COLUMNS, LIVEREPORT_COLUMN_MANAGER_BUTTON, \
    LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN_GROUP, PARTIALLY_SELECTED_COLUMN_NODE
from helpers.verification.data_and_columns_tree import verify_columns_in_column_mgmt_ui, \
    verify_grouped_columns_in_column_mgmt_ui
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.grid import verify_footer_values
from library import dom


@pytest.mark.smoke
@pytest.mark.usefixtures('open_livereport')
@pytest.mark.usefixtures('new_live_report')
def test_group_ungroup_columns_from_tree_ui(selenium):
    """
    Test Grouping and Ungrouping Columns from column mgmt ui.
    1.Group columns using the group button
    2.Hide one column from group and check for partial visibilty
    3.Freeze the group
    4.Unfreeze and check for order of grouped columns
    5.Ungroup columns using ungroup button
    :param selenium: Selenium Webdriver
    """
    # Selecting different types of columns for grouping: Assay,3D & ffc
    open_add_data_panel(selenium)
    add_column_by_name(selenium, 'PK_PO_RAT (AUC)')
    add_column_by_name(selenium, 'EGFR-TRFRET (Ki)')
    add_column_by_name(selenium, 'Number - published')

    # Navigate to the LiveReport tab in D&C Tree
    open_column_mgmt_panel(selenium)

    # ----- Check that "Ungroup" button is disabled prior any selection----- #
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON_DISABLED, selector_text="Ungroup")
    # ----- Group columns selectively----- #
    group_columns_selectively_via_column_mgmt_ui(selenium, 'test', 'PK_PO_RAT (AUC)', 'EGFR-TRFRET (Ki)',
                                                 'Number - published')
    group_header_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_GROUPED_COLUMNS)
    assert group_header_element.text == 'test', \
        "No Group with name {} was found, instead found group with name {}".format('test', group_header_element.text)
    # Verify the columns in group
    verify_grouped_columns_in_column_mgmt_ui(selenium, ['PK_PO_RAT (AUC)', 'EGFR-TRFRET (Ki)', 'Number - published'],
                                             group_name='test')

    # Check that "Ungroup" button is active after group formation
    verify_is_visible(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Ungroup")

    # ----- Check the partial visibility functionality ----- #

    # Select column using Ctrl key and hide a column using "Hide" button and verify footer values
    hide_columns_selectively(selenium, 'PK_PO_RAT (AUC)')
    verify_footer_values(selenium, {'column_all_count': '7 Columns', 'column_hidden_count': '2 Hidden'})
    # Verify partially selected parent column
    verify_is_visible(selenium, PARTIALLY_SELECTED_COLUMN_NODE)

    # show hidden columns
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Show')

    # ----- Freeze grouped columns ----- #
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_GROUPED_COLUMNS, text='test', exact_text_match=True)
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Freeze')
    verify_is_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN_GROUP, selector_text="test")
    # Unfreeze all columns
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Unfreeze')

    # ----- Ungroup columns  ----- #
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Ungroup')
    # Verify columns are not grouped
    verify_is_not_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_GROUPED_COLUMNS, selector_text='test')
    # Verifying that the order for Column labels in Columns Management UI is correct after
    # unfreezing and ungrouping columns.
    verify_columns_in_column_mgmt_ui(selenium, [
        'ID', 'PK_PO_RAT (AUC)', 'EGFR-TRFRET (Ki)', 'Number - published', 'All IDs', 'Rationale', 'Lot Scientist',
        'Lot Date Registered'
    ])
