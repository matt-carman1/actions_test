import pytest
from library import dom, actions

from helpers.verification.data_and_columns_tree import verify_grouped_columns_in_column_mgmt_ui
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.change.columns_management_ui import search_in_col_mgmt_ui, group_columns_selectively_via_column_mgmt_ui, \
    hide_columns_selectively, remove_columns_via_column_mgmt_ui
from helpers.selection.column_tree import LIVEREPORT_COLUMN_CHECKBOX_LABEL, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, \
    LIVEREPORT_COLUMN_MANAGER_BUTTON, LIVEREPORT_HIDDEN_COLUMN_LABEL, LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_basic_functions_on_filtered_col_mgmt_ui_results(selenium):
    """
    Test to verify the filtering of column names, functionality of column management buttons and drag/drop while filtering in Column Management UI

    :param selenium: Selenium Webdriver
    """
    expected_filtered_columns = ['ID', 'All IDs', 'CorpID String (CorpID String)']
    # Search via column management UI
    search_in_col_mgmt_ui(selenium, search_term='ID')
    # Retrieve the columns that were filtered
    filtered_col_elems = dom.get_elements(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, timeout=3, dont_raise=True)
    filtered_columns = [elem.text for elem in filtered_col_elems]
    assert expected_filtered_columns == filtered_columns, 'Expected filtered columns is {} but got {}'.\
        format(expected_filtered_columns, filtered_columns)

    # Unfreezing 'ID' column using Unfreeze button
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, text='ID', exact_text_match=True)
    dom.click_element(selenium, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Unfreeze')
    verify_is_not_visible(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_FROZEN, selector_text='ID')

    # Grouping two columns ('ID' column using 'Group...' button and 'All IDs' column using drag and drop into the group)
    group_columns_selectively_via_column_mgmt_ui(selenium, 'Test Grouped Column(s)', 'ID')
    dom.click_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='All IDs')
    drag_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL_SELECTED, text='All IDs')
    drop_element = dom.get_element(selenium, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text='ID', exact_text_match=True)
    actions.drag_dragover_and_drop(selenium, drag_element, drop_element)
    verify_grouped_columns_in_column_mgmt_ui(selenium, ['All IDs', 'ID'], group_name='Test Grouped Column(s)')

    # Hiding 'All IDs' column using Hide button
    hide_columns_selectively(selenium, 'All IDs')
    verify_is_visible(selenium, selector=LIVEREPORT_HIDDEN_COLUMN_LABEL, selector_text='All IDs')

    # Removing 'CorpID String (CorpID String)' column using Remove button
    remove_columns_via_column_mgmt_ui(selenium, ['CorpID String (CorpID String)'])
    verify_is_not_visible(selenium,
                          selector=LIVEREPORT_COLUMN_CHECKBOX_LABEL,
                          selector_text='CorpID String (CorpID String)')
