import pytest

from helpers.change.actions_pane import close_add_data_panel
from helpers.change.columns_action import search_and_select_column_from_columns_mgmt_ui
from helpers.change.columns_management_ui import open_column_mgmt_panel, select_multiple_column_labels
from helpers.change.data_and_columns_tree import clear_column_tree_livereport_tab_search
from helpers.selection.column_tree import LIVEREPORT_VISIBLE_COLUMN_LABEL, LIVEREPORT_COLUMN_MANAGER_BUTTON
from helpers.verification.data_and_columns_tree import verify_click_column_via_col_tree
from helpers.verification.element import verify_is_visible

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.xfail(reason="QA-5793")
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_show_hide_columns_in_col_mgmt_ui(driver):
    """
    Test for verifying Show/Hide button based on the selected columns in the Columns Mgmt UI.
    search_term is columns name.
    All_columns_list_hidden_and_visible = {
    All IDs : visible
    Rationale : visible
    Lot Scientist : visible
    Lot Date Registered : hidden
    HBA (HBA) : visible
    HBD (HBD) : visible
    PSA (PSA) : visible
    AlogP (AlopP) : visible
    }
    :param driver: Selenium Webdriver
    """

    open_column_mgmt_panel(driver)
    # # Select a single visible column, 'Hide' button should be enabled and displayed
    search_and_select_column_from_columns_mgmt_ui(driver, search_term="Rationale")
    verify_is_visible(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Hide")
    clear_column_tree_livereport_tab_search(driver)

    # Select a single hidden column, 'Show' button should be enabled and displayed
    search_and_select_column_from_columns_mgmt_ui(driver, search_term='Lot Scientist')
    verify_click_column_via_col_tree(driver, "Hide")
    verify_click_column_via_col_tree(driver, "Show")
    verify_is_visible(driver, LIVEREPORT_VISIBLE_COLUMN_LABEL, selector_text='Lot Scientist')
    clear_column_tree_livereport_tab_search(driver)

    # Select multiple visible columns, 'Hide' button should be enabled and displayed
    select_multiple_column_labels(driver, 'HBA (HBA)', 'HBD (HBD)')
    verify_is_visible(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Hide")

    # Select multiple hidden columns, 'Show' button should be enabled and displayed
    select_multiple_column_labels(driver, 'HBA (HBA)', 'HBD (HBD)')
    verify_click_column_via_col_tree(driver, "Hide")
    select_multiple_column_labels(driver, 'HBA (HBA)', 'HBD (HBD)')
    verify_is_visible(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Show")

    # Select a mixture of visible & hidden columns, 'Show' button should be enabled and displayed
    select_multiple_column_labels(driver, 'Lot Scientist', 'HBA (HBA)')
    verify_is_visible(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, selector_text="Show")
    close_add_data_panel(driver)
